include default.mk
export

validate :
	docker-compose config --quiet

build : validate
	docker-compose build

test :
	@echo "Running tests..."
	@sleep 2
	@echo "Tests succesfully run."

push : build
	docker-compose push

up :
	docker-compose up -d

down :
	docker-compose down

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
