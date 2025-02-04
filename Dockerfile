FROM alpine AS base

RUN apk add --no-cache \
    bash cmake gcc g++ git make python3-dev

RUN apk add --no-cache \
    lapack-dev linux-headers openblas-dev zlib-dev

RUN apk add python3 py3-onnxruntime py3-pip --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/

COPY requirements.txt .
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

RUN mkdir /app

WORKDIR /app

COPY u2net.onnx /root/.u2net/u2net.onnx


COPY . .

EXPOSE 5050

CMD ["python", "server.py"]