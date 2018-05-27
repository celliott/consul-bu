include default.mk
export

validate :
	docker-compose config --quiet

build : validate
	docker-compose build

test : up
	@url=http://127.0.0.1:3000
	@curl --output /dev/null --silent --head --fail --max-time 10 --connect-timeout 3 "$url"

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
