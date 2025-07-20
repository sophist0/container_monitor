FROM ubuntu
RUN apt-get update && apt-get -y install sudo
RUN apt-get update -qq && apt-get install -qqy \
    apt-transport-https \
    ca-certificates \
    curl \
    lxc \
    iptables

# Install Docker from Docker Inc. repositories.
RUN curl -sSL https://get.docker.com/ | sh

RUN apt-get install -y python3
RUN apt update && apt -y install python3-pip
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor

RUN mkdir "delete_bot_private_montitor"
WORKDIR delete_bot_private_montitor

ADD requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages


COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY monitor.py .
COPY config.txt .
COPY tests/ .

CMD ["sh", "-c", "${DOCKER_CMD}"]
