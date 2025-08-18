FROM ubuntu:latest
LABEL authors="marc."

ENTRYPOINT ["top", "-b"]