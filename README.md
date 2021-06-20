I tried in three ways to deploy a Docker container.

Summary of deployment attempts via:

- GCP Cloud Run: succeeded to deploy service (serving Hello, World).
  - https://golubitsky-ml-model-deployment-without-cloud-buil-qvmmc7xxqa-ue.a.run.app/
- GCP Cloud Build integration for Github: permissions issue — [PROJECT_ID]@cloudbuild.gserviceaccount.com account doesn't have correct permissions to deploy
- AWS ECS: missing iam:CreateRole permissions

## Attempts via GCP

### Cloud Run

We can't use DockerHub. Therefore we must push to Google Container Registry.

```
gcloud auth login
gcloud auth configure-docker
gcloud config set project fb-mle-march-21
docker build -t gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1 .
docker push gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1
```

### The current state of the art.

I was able to use the above image in GCR to manually setup a service in GCP. It works.

```
$ curl -H  "Authorization: Bearer $(gcloud auth print-identity-token)" https://golubitsky-ml-model-deployment-without-cloud-buil-qvmmc7xxqa-ue.a.run.app
Hello, brave world!
```

This is serving the Flask app defined in `app.py`.

#### Permissions issue (and resolution)

I am unauthorized to expose the API publically — it's a permissions issue:

```
Only authenticated invocations are allowed for this service.
To allow unauthenticated invocations, add "allUsers" as a member and assign it the "Cloud Run invoker" role.
```

To solve this issue, someone with the necessary permissions needed to add allUsers (or some specific users/groups) with the “Cloud Run Invoker” role.

#### To Deploy a new version

- Manually build.

```
docker build -t gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1 .
docker push gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1
```

- Manually update.
  - Visit https://console.cloud.google.com/run/detail/us-east1/golubitsky-ml-model-deployment-without-cloud-build/revisions?project=fb-mle-march-21
  - Click `EDIT & DEPLOY NEW REVISION`.
  - Click `DEPLOY`.

### Cloud Build

Separately, I tried to get Cloud Build to work (so that pushing to this repo will cause builds).

The builds are triggered, but every build fails to actually deploy due to other permissions issues I also cannot resolve myself.

This is the error encountered for every build:

```
Step #2 - "Deploy": ERROR: (gcloud.run.services.update) PERMISSION_DENIED: Permission 'run.services.get' denied on resource 'namespaces/fb-mle-march-21/services/golubitsky-ml-model-deployment' (or resource may not exist).
```

Reading [docs/build-debug-locally](https://cloud.google.com/build/docs/build-debug-locally), I confirmed that the build is fine locally.

Then I see this quote from the docs:

- To run the build, the local builder uses your personal account, and the Cloud Build uses the cloudbuild service account [PROJECT_ID]@cloudbuild.gserviceaccount.com. If you set any permissions on your personal account for the local builder, you may need to replicate these permissions on the cloudbuild service account. For details, see Setting Service Account Permissions.

It is not that my personal account doesn't have the Cloud Run permissions, but rather the cloudbuild service account.

## Earlier attempt via AWS that also ran into permissions issues

I tried to deploy Docker container to ECS directly by following:

- https://docs.docker.com/compose/gettingstarted/
- https://docs.docker.com/docker-hub/repos/
- https://docs.docker.com/cloud/ecs-integration/

```
docker context use default
docker build -t golubitsky/ml-model-deployment:v1 .
```

```
docker login
docker push golubitsky/ml-model-deployment:v1
```

```sh
docker context use myecscontext
# NOTE: note docker-compose
docker compose up
```

I encountered the following blocking issue:

```
API: iam:CreateRole User: arn:aws:iam::681261969843:user/mike617@gmail.com is not authorized to perform: iam:CreateRole on resource: arn:aws:iam::681261969843:role/wake-word-app-WebTaskExecutionRole-15J439Q98DGFD
```
