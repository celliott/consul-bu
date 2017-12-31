FROM python:2.7-alpine
MAINTAINER chris elliott <ctelliott@gmail.com>

# install dependencies
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# add password
ADD ./src/* /opt/
RUN chmod +x /opt/*.py

CMD ["/opt/consul_bu.py"]
