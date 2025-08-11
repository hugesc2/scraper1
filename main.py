import requests
from bs4 import BeautifulSoup
import pandas as pd
from google.cloud import storage
import os
import datetime

def scrape():
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

    df = pd.DataFrame(data)
    return df

def upload_to_gcs(bucket_name, df):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"scraped_countries_{now}.csv"
    df.to_csv(filename, index=False)

    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    print(f"Uploaded {filename} to {bucket_name}")

def main():
    df = scrape()
    upload_to_gcs("rpa-poc-files", df)

if __name__ == "__main__":
    main()
