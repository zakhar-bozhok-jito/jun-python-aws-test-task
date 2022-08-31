FROM alpine:latest
RUN apk update && apk add python3 py3-pip
RUN python3 -m pip install pika requests
COPY . /app
WORKDIR /app