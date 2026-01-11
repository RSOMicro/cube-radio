## Running on local computer (recomended)
This was tested on Python 3.10
rename ``.env.example`` to ``.env`` and add ur MySQL Connection details
then run
```python
pip install -r requirements.txt
python3 src/main.py
```
## Running with docker
```bash
docker compose up --build
```

## Deploying to Kubenetes
1. Install Helm
```bash
winget install Helm.Helm
```
2. Install MySQL DB with Helm
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install userservice-db bitnami/mariadb -f helm/values-mariadb.yaml
```
If u want to uninstall for some reason
```
helm uninstall userservice-db
kubectl delete pvc -l app.kubernetes.io/name=mariadb
```

3. Verify mysql is working
```
kubectl run userservice-db-mariadb-client --rm --tty -i --restart='Never' --image  registry-1.docker.io/bitnami/mariadb:latest --namespace default --command -- bash
mysql -h userservice-db-mariadb.default.svc.cluster.local -uroot -p user_service
```

4. Install UserService helm
```
helm install userservice ./helm/userservice
```

5. Verify if it works
```
connect to here: http://localhost:80/api/user/health/liveness
You should get 200 OK
```
