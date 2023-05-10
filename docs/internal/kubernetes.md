### Steps to update image on cloud

Build image. You can change the first tag, but the latest always be there
```
docker build -f .\backend\Dockerfile.prod -t banderosik/banderachat-backend:v1.1 -t banderosik/banderachat-backend:latest .\backend\
```

Push image
```
docker push -a banderosik/banderachat-backend
```

Restart deployment pods
```
kubectl rollout restart deployment webregi-v2-app 
```

Run alembic migration job if needs
```
kubectl apply -f .\k8s\alembic-job.yaml 
```

If alembic error, do one of those steps:
```kubectl get pods```
1. ```kubectl delete pod alembic-migrate-(name)```
2. ```kubectl delete job alembic-migrate```
