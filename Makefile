# see https://lithic.tech/blog/2020-05/makefile-dot-env/
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

current_dir_host := $(shell pwd)
requirements_src := $(current_dir_host)/requirements.txt
requirements_dst := $(PROJECT_PATH)/requirements.txt

# see https://lithic.tech/blog/2020-05/makefile-wildcards/
guard-%:
	@if [ -z '${${*}}' ]; then echo 'ERROR: variable $* not set' && exit 1; fi

env_guard: guard-JUP_CONTAINER_NAME guard-JUP_IMAGE_NAME guard-JUP_VOLUME_NAME\
			guard-USR_NAME guard-PROJECT_PATH

docker: docker-compose.yaml Dockerfile

devcli: env_guard docker
	docker exec -it -u $(USR_NAME) $(JUP_CONTAINER_NAME) /bin/bash

dev: env_guard docker
	touch requirements.txt
	@printf 'Developing in container name: $(JUP_CONTAINER_NAME)\n***\n'
	docker-compose up --build

init:
	touch requirements.txt
	mkdir src src/main src/data src/modules

build: env_guard docker
	docker build . -t $(JUP_IMAGE_NAME)
	
install: env_guard docker
	docker run -it --rm \
		--user $(USR_NAME):$(USR_NAME) \
		--name $(JUP_CONTAINER_NAME) \
		--mount 'type=bind,src=$(requirements_src),dst=$(requirements_dst)' \
		--mount 'type=volume,src=$(JUP_VOLUME_NAME),dst=$(PROJECT_PATH)/venv/' \
		--workdir $(PROJECT_PATH) \
		$(JUP_IMAGE_NAME) \
			/bin/bash -c \
			". jupdev && pip install jupyterlab && . update"

setup: init build install

runcli: env_guard docker
	docker run -it -u $(USR_NAME) --name $(JUP_CONTAINER_NAME) $(JUP_IMAGE_NAME)

alldown: env_guard docker
	docker-compose down --rmi all --volumes --remove-orphans