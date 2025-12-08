# cube-radio

Kubernetes

Deploy our services
```
kubectl apply -f k8s/radiolocal-config.yml
kubectl apply -f k8s/radiolocal-secret.yml
kubectl apply -f k8s/radiolocal-deployment.yml
kubectl rollout restart deployment.apps/radiolocal
```

Check our pods
```
kubectl get pods
```

Check Services
```
kubectl get svc
```

See whats wrong with our service
```
kubectl describe pod -l app=radiolocal
kubectl logs -l app=radiolocal
```

Quickly test our kubernetes service from browser (without ingress controller)
```
kubectl port-forward service/radiolocal 8080:8081
```

Deploy Ingress controller
```
kubectl apply -f k8s/ingress.yaml
```

If using docker, u first need to install Ingress controller
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.12.1/deploy/static/provider/cloud/deploy.yaml
```

then u can connect to: http://127.0.0.1/api/radio/health/liveness

and everything Will work
