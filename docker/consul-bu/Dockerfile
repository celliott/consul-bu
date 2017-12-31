FROM python:2.7-alpine
MAINTAINER chris elliott <ctelliott@gmail.com>

# install dependencies
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# add password
ADD ./src/consul_bu.py /opt/consul_bu.py
RUN chmod +x /opt/consul_bu.py

CMD ["/opt/consul_bu.py"]
