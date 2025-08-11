FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/key.json"
ENV PORT=8080

CMD ["python", "main.py"]
