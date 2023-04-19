# FROM python:3.8-alpine
# WORKDIR /app
# COPY ./dev /app/dev

# CMD ["python3","-m","dev.main"]               


FROM ubuntu:20.04
WORKDIR /app
COPY ./dev /app/dev
RUN apt-get update && apt-get install -y python3

CMD ["python3","-m","dev.main"]               