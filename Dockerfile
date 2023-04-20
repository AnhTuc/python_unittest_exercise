FROM python:3.8-alpine
WORKDIR /app
COPY ./dev /app/dev

CMD ["python3","-m","dev.main"]               


# FROM ubuntu:20.04
# WORKDIR /app
# COPY ./dev /app/dev
# RUN apt-get update && apt-get install -y python3

# CMD ["python3","-m","dev.main"]

# FROM alpine:latest
# WORKDIR /app
# COPY ./dev /app/dev

# RUN apk add python3

# CMD ["python3","-m","dev.main"]
#https://wiki.alpinelinux.org/wiki/Comparison_with_other_distros