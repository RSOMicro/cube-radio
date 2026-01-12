import azure.functions as func
import logging
import socket
import random
import json
import urllib.request

# ---------------- Config ----------------
USER_ID = "remote-api"

# ---------------- Radio Browser helpers ----------------
def get_radiobrowser_base_urls():
    hosts = []
    ips = socket.getaddrinfo(
        'all.api.radio-browser.info',
        80, 0, 0, socket.IPPROTO_TCP
    )

    for ip_tuple in ips:
        ip = ip_tuple[4][0]
        try:
            host_addr = socket.gethostbyaddr(ip)
            if host_addr[0] not in hosts:
                hosts.append(host_addr[0])
        except Exception:
            pass

    hosts.sort()
    return ["https://" + h for h in hosts]

def download_uri(uri, param=None):
    headers = {
        'User-Agent': 'RemoteAPI/1.0',
        'Content-Type': 'application/json'
    }
    data_bytes = None
    if param is not None:
        data_bytes = json.dumps(param).encode('utf-8')
    req = urllib.request.Request(uri, data=data_bytes, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode('utf-8')

def download_radiobrowser(path, param=None):
    servers = get_radiobrowser_base_urls()
    random.shuffle(servers)

    for server in servers:
        uri = server + path
        try:
            logging.info("RadioBrowser request: %s", uri)
            return download_uri(uri, param)
        except Exception as e:
            logging.warning("RadioBrowser failed: %s (%s)", uri, e)

    logging.error("All RadioBrowser servers failed")
    return "[]"

def get_serbia_stations():
    data = download_radiobrowser("/json/stations/bycountrycodeexact/RS")
    stations = json.loads(data)

    result = []
    for s in stations:
        result.append({
            "_id": s.get("stationuuid"),
            "description": s.get("tags") or "",
            "logo_url": s.get("favicon") or "",
            "name": s.get("name"),
            "stream_url": s.get("url_resolved") or s.get("url"),
            "user_id": USER_ID
        })
    return result

# ---------------- Azure Function App ----------------
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="radio/remote", methods=["GET", "OPTIONS"])
def radio_remote(req: func.HttpRequest) -> func.HttpResponse:
    # Handle CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=204,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, rid, st-auth-mode"
            }
        )

    try:
        stations = get_serbia_stations()
        return func.HttpResponse(
            json.dumps(stations, indent=2),
            status_code=200,
            mimetype="application/json",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, rid, st-auth-mode"
            }
        )
    except Exception as e:
        logging.exception("Error fetching stations")
        return func.HttpResponse(
            str(e),
            status_code=500,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization, rid, st-auth-mode"
            }
        )