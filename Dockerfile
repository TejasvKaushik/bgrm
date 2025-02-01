FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=10000

EXPOSE 10000

CMD ["python", "-m", "waitress", "--listen=0.0.0.0:10000", "server:app"]
