FROM python:2.7-alpine
MAINTAINER chris elliott <ctelliott@gmail.com>

ENV CONSUL_VERSION=1.0.2

# Download and install Consul
RUN apk upgrade --update --no-cache && \
    apk add --update --no-cache curl && \
    curl -sSLo /tmp/consul.zip https://releases.hashicorp.com/consul/{$CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip && \
    unzip -d /bin /tmp/consul.zip && \
    rm /tmp/consul.zip && \
    apk del curl

# install dependencies
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# add password
ADD ./src/consul_bu.py /opt/consul_bu.py
RUN chmod +x /opt/consul_bu.py

CMD ["/opt/consul_bu.py"]
