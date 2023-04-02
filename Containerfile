FROM registry.access.redhat.com/ubi9/ubi:9.1.0-1782

ENV AUTH_TOKEN="MY_AUTH_TOKEN"

RUN dnf install -y \
        g++ \
        gcc \
        nodejs \
        openssl-devel \
        python3 \
        python3-pip \
        ruby \
        ruby-devel && \
    gem install "bundler:2.4.8" "smashing:1.3.6" && \
    dnf remove -y g++ gcc openssl-devel ruby-devel

RUN mkdir -p /var/smashing-squashes

WORKDIR /var/smashing-squashes

RUN smashing new dashboard
COPY dashboard/dashboards custom-dashboards
COPY dashboard/widgets custom-widgets
RUN rm -rf dashboard/jobs/* && \
    rm -rf dashboard/dashboards && \
    cp -r custom-dashboards dashboard/dashboards && \
    find custom-widgets -maxdepth 1 -type d -exec cp -r "{}" dashboard/widgets/ \; && \
    cd dashboard && \
    bundle
RUN chmod 777 dashboard/config.ru

COPY container_entrypoint.sh /usr/bin/container_entrypoint.sh
RUN chmod 755 /usr/bin/container_entrypoint.sh

COPY feeder feeder
RUN pip install -r feeder/requirements.txt

ENTRYPOINT ["/usr/bin/container_entrypoint.sh"]
EXPOSE 3030
