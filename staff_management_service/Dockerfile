FROM python:3.9
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

EXPOSE 8000

CMD ["sh", "/wait-for-db.sh", "staff_management", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

