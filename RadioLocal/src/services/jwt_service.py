import jwt
from fastapi import HTTPException, Depends, Header
from config import settings

def get_company_from_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        #print(payload)
        return payload.get("company_id")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or missing JWT: "+str(e)) from e