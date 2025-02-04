FROM python:3.10-slim AS base

RUN mkdir /app

WORKDIR /app

COPY u2net.onnx /root/.u2net/u2net.onnx

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["python", "server.py"]