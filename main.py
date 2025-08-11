import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import storage
from flask import Flask, jsonify
import os
import datetime

app = Flask(__name__)

def scrape_data():
    url = "https://www.scrapethissite.com/pages/simple/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    countries = soup.select(".country")
    data = []
    for country in countries:
        name = country.select_one(".country-name").text.strip()
        capital = country.select_one(".country-capital").text.strip()
        population = country.select_one(".country-population").text.strip().replace(',', '')
        area = country.select_one(".country-area").text.strip().replace(',', '')

        data.append({
            "Name": name,
            "Capital": capital,
            "Population": int(population),
            "Area": float(area)
        })

    return pd.DataFrame(data)

def upload_to_gcs(bucket_name, df):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    now = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"scraped_countries_{now}.csv"
    temp_path = f"/tmp/{filename}"

    df.to_csv(temp_path, index=False)

    blob = bucket.blob(filename)
    blob.upload_from_filename(temp_path)

    return filename

@app.route("/scrape", methods=["GET"])
def run_scraper():
    try:
        df = scrape_data()
        filename = upload_to_gcs("rpa-poc-files", df)
        return jsonify({"status": "success", "file_uploaded": filename}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "Scraper service is running. Use /scrape to trigger scraping.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
