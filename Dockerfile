FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# GCS needs GOOGLE_APPLICATION_CREDENTIALS set
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/key.json"

CMD ["python", "main.py"]
