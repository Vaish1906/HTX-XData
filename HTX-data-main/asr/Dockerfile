FROM python:3.12-slim
RUN apt update -y && apt install -y make
WORKDIR /app
COPY Makefile .
COPY requirements.txt .
RUN make install
COPY ./asr ./asr
ENTRYPOINT [ "make", "api" ]
