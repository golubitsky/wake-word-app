https://docs.docker.com/compose/gettingstarted/

https://docs.docker.com/docker-hub/repos/

https://docs.docker.com/cloud/ecs-integration/

```
docker context use default
docker build -t golubitsky/ml-model-deployment:v1 .
```

```
docker login
docker push golubitsky/ml-model-deployment:v1
```


### Develop


### Deploy

```sh
docker context use myecscontext
# NOTE: note docker-compose
docker compose up
```

### Cloud Run

We can't use DockerHub. Therefore we must push to Google Container Registry.


```
gcloud auth login
gcloud auth configure-docker
gcloud config set project fb-mle-march-21
docker build -t gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1 .
docker push gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1
```

<remove me, added to test build 3>