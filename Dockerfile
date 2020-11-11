# We're using Ubuntu (cause heroku shit)
FROM ubuntu:latest

ENV PIP_NO_CACHE_DIR 1

ARG DEBIAN_FRONTEND=noninteractive

RUN sed -i.bak 's/us-west-2\.ec2\.//' /etc/apt/sources.list

# Installing Required Packages
RUN apt update && apt upgrade -y && \
    apt install --no-install-recommends -y \
    curl \
    git \
    libffi-dev \
    libjpeg-dev \
    libjpeg-turbo8-dev \
    libwebp-dev \
    python3-lxml \
    postgresql \
    postgresql-client \
    python3-psycopg2 \
    libpq-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libxslt1-dev \
    python3-pip \
    python3-sqlalchemy \
    openssl \
    wget \
    python3 \
    python3-dev \
    libreadline-dev \
    libyaml-dev \
    gcc \
    zlib1g \
    ffmpeg \
    libssl-dev \
    libgconf-2-4 \
    libxi6 \
    unzip \
    libopus0 \
    libopus-dev \
    && rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

RUN git clone https://git.mannu.me/pokurt/Nana-Remix.git /root/nana

WORKDIR /root/nana

# install dependencies
RUN pip3 install -U -r requirements.txt

RUN rm -rf README.md

ENV PATH="/home/userbot/bin:$PATH"


# Starting Worker
CMD ["python3","-m","nana"]
