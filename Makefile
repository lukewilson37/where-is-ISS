NAME ?= lukewilson37

test: py_test build run clean

init: build run gather

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

py_test:
	pytest

clean:
	docker stop "${NAME}-flask"
	docker rm "${NAME}-flask"

build:
	 docker build -t ${NAME}/whereisiss-flask:latest .

run_flask:
	 docker run --name "${NAME}-flask" -d -p 5037:5000 ${NAME}/whereisiss-flask:latest
	
push:
	docker push ${NAME}/whereisiss-flask:latest

gather:
	curl -X POST localhost:5037/init



