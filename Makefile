# In order to share IMAGE_NAME here and docker-compose.yml
include .env
export $(shell sed 's/=.*//' .env)

build:
	docker build -t $(IMAGE_NAME) .

server: build
	docker-compose up

test: build
	docker-compose run --rm develop pytest -f --color=yes -p no:cacheprovider

deploy: build
	docker push $(IMAGE_NAME)
	echo 'Builds are deployed using CI/CD via Cloud Build by merging to main, but you can manually deploy at:'
	echo 'https://console.cloud.google.com/run/deploy/us-east1/golubitsky-ml-model?project=fb-mle-march-21'