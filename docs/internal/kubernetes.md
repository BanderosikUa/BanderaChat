### Backend

Build image. You can change the first tag, but the latest always be there
```
docker build -f .\backend\Dockerfile.prod -t banderosik/banderachat-backend:v1.1 -t banderosik/banderachat-backend:latest .\backend\
```

Push images
```
docker push -a banderosik/banderachat-backend
```

Restart deployment pods
```
kubectl rollout restart deployment backend
```

Run alembic migration job if needs
```
kubectl apply -f .\k8s\alembic-job.yaml 
```

If alembic error, do one of those steps:
```kubectl get pods```
1. ```kubectl delete job alembic-migrate```

### Frontend
Build image. You can change the first tag, but the latest always be there
```
docker build -f .\frontend\Dockerfile -t banderosik/banderachat-frontend:v1.1 -t banderosik/banderachat-frontend:latest .\frontend\
```

Push image
```
docker push -a banderosik/banderachat-frontend
```

Restart deployment pods
```
kubectl rollout restart deployment frontend
```
