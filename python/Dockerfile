FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /usr/src/app

# Installer les dépendances système nécessaires pour compiler lz4
RUN apt-get update && apt-get install -y gcc python3-dev liblz4-dev && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY clickhouse_connect_requirements.txt .
RUN pip install --no-cache-dir clickhouse_connect

COPY pandas_requirements.txt .
RUN pip install --no-cache-dir -r pandas_requirements.txt

COPY . .

CMD ["python", "script.py"]