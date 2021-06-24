# In order to share IMAGE_NAME here and docker-compose.yml
include .env
export $(shell sed 's/=.*//' .env)

build:
	docker build -t $(IMAGE_NAME) .

server: build
	docker-compose up

test: build
	docker-compose run --rm develop pytest -f --color=yes -p no:cacheprovider

# This is accomplished automatically by merging to the remote `main` branch,
# using Cloud Build, which also deploys.
deploy: build
	docker push $(IMAGE_NAME)
	echo 'manually deploy at https://console.cloud.google.com/run/deploy/us-east1/golubitsky-ml-model-deployment-without-cloud-build?project=fb-mle-march-21'