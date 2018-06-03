include defaults.mk
export

validate :
	docker-compose config --quiet

build : validate
	docker-compose build

test : up
	export BRANCH_NAME=$(eval BRANCH_NAME = $(shell git rev-parse --abbrev-ref HEAD))
	until $$(curl --output /dev/null --silent --head --fail http://172.17.0.1:3000/healthz); do \
		printf '.'; \
		sleep 5; \
	done

	docker-compose down

push : build
	docker-compose push

up :
	export BRANCH_NAME=$(eval BRANCH_NAME = $(shell git rev-parse --abbrev-ref HEAD))
	docker-compose up -d

down :
	docker-compose down

tail :
	docker-compose logs -f

reset : down up

deploy :
	@if [ ! -f values.yaml ]; then \
		touch values.yaml; \
	fi
	helm init --client-only
	-kubectl create namespace vault
	helm upgrade -i $(SERVICE) helm/$(SERVICE) \
		--namespace vault \
		--set ingress.hostname=$(SERVICE).$(DOMAIN) \
		--set ingress.enabled=true \
		-f values.yaml

delete :

	helm del --purge $(SERVICE)
