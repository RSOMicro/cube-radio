# RadioLocal Service
This service gets JWT token and saves stations inside a MongoDB

## Running on local computer (recomended)
This was tested on NODE
rename ``.env.example`` to ``.env`` and add ur MongoDB Connection script
then run
```js
npm install
npm run
```
## Running with docker
```bash
docker build -t frontend .
docker run -p 3000:3000 --env-file .env frontend
```

## Deploying to Kubenetes
1. Install Helm
```bash
winget install Helm.Helm
```

1. Install frontend helm
```
helm install frontend ./helm/frontend
```

2. Verify if it works
```
connect to here: http://localhost:80
You should see a login prompt
```
