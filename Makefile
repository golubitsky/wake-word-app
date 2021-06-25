IMAGE_NAME = $(shell ./echo_branch_based_docker_image_name.sh)
export IMAGE_NAME # for docker-compose.yml

build:
	docker build -t $(IMAGE_NAME) .

server: build
	docker-compose up

test: build
	docker-compose run --rm develop pytest -f --color=yes -p no:cacheprovider