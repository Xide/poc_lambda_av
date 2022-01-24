FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y \
        clamav \
        clamav-daemon \
        python3 \
        python3-pip
RUN mkdir /var/run/clamav && \
    chown clamav /var/run/clamav
RUN freshclam

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY init.sh main.py /
CMD /init.sh
