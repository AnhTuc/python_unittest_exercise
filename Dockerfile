FROM ubuntu:20.04
FROM python:3.8-alpine
WORKDIR /app
COPY ./dev /app/dev

CMD ["python3","-m","dev.main"]                  
