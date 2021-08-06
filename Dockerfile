FROM python:3.9.6-slim-buster

ARG PROJECT_NAME=building-emissions USR_NAME=jup PROJECT_PATH=/home/jup/building-emissions

RUN	groupadd --gid 1000 ${USR_NAME} && \
	useradd --uid 1000 ${USR_NAME} --gid ${USR_NAME} --shell /bin/bash --create-home && \
	mkdir ${PROJECT_PATH} ${PROJECT_PATH}/src ${PROJECT_PATH}/src/data ${PROJECT_PATH}/src/modules ${PROJECT_PATH}/src/main && \
	chown -R 1000:1000 ${PROJECT_PATH}

USER ${USR_NAME}:${USR_NAME}

COPY --chown=${USR_NAME}:${USR_NAME} ./src/ ${PROJECT_PATH}/src/
COPY --chown=${USR_NAME}:${USR_NAME} ./requirements.txt ${PROJECT_PATH}/requirements.txt

RUN cd ${PROJECT_PATH} && \
	/bin/bash -c  \
	"echo 'pip freeze > /home/jup/building-emissions/requirements.txt' | tee update.sh && \
	ln -s update.sh update && \
	echo 'creating python virtual environment' && \
	python -m venv venv && \
	ln -s venv/bin/activate jupdev"

ENV PATH "/home/jup/building-emissions:$PATH"