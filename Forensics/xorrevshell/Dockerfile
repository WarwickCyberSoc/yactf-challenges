FROM python:3.9

# This is just for my convenience :-)
RUN apt update && apt install -y curl tcpdump iproute2 iputils-ping ncat
RUN pip3 install flask

RUN cp /bin/ping /usr/bin/ping

CMD ["/bin/bash"]