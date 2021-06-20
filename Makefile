build:
	docker build -t gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1 .

server: build
	docker-compose up

test: build
	docker-compose run --rm develop pytest -f --color=yes -p no:cacheprovider

deploy: build
	docker push gcr.io/fb-mle-march-21/golubitsky/ml-model-deployment:v1
	echo 'manually deploy at https://console.cloud.google.com/run/deploy/us-east1/golubitsky-ml-model-deployment-without-cloud-build?project=fb-mle-march-21'