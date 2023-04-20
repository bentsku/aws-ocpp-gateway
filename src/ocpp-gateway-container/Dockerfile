FROM amazonlinux:2022

RUN yum update -y
RUN yum groupinstall "Development Tools" -y
RUN yum install openssl-libs -y
RUN yum install python3.10 python3.10-devel -y

# this order allows better caching of layers, it would always run pip install even if requirements.txt didn't change
RUN mkdir -p /opt/ocpp-gateway
RUN python3.10 -m venv /opt/ocpp-gateway/

COPY requirements.txt /opt/ocpp-gateway/requirements.txt

RUN . /opt/ocpp-gateway/bin/activate && pip install --no-cache-dir -r /opt/ocpp-gateway/requirements.txt

COPY ./ /opt/ocpp-gateway/

EXPOSE 80

ENTRYPOINT /opt/ocpp-gateway/run-server.sh
CMD /opt/ocpp-gateway/run-server.sh
