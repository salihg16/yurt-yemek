import json
import os
from datetime import datetime, timezone, timedelta
from requests_oauthlib import OAuth1Session

CONSUMER_KEY = os.environ["FS_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["FS_CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["FS_ACCESS_TOKEN"]
ACCESS_SECRET = os.environ["FS_ACCESS_SECRET"]

# Türkiye saati (UTC+3) ile bugünün tarihini al
tr_tz = timezone(timedelta(hours=3))
bugun = datetime.now(tr_tz).strftime("%Y-%m-%d")

with open("menu.json", "r", encoding="utf-8") as f:
    menu = json.load(f)

if bugun not in menu:
    print(f"{bugun} için menü bulunamadı.")
    exit(0)

# FatSecret tarih formatı: 1 Ocak 1970'ten itibaren geçen gün sayısı
epoch_days = (datetime.now(tr_tz).date() - datetime(1970, 1, 1).date()).days

oauth = OAuth1Session(
    CONSUMER_KEY,
    client_secret=CONSUMER_SECRET,
    resource_owner_key=ACCESS_TOKEN,
    resource_owner_secret=ACCESS_SECRET,
)

for yemek in menu[bugun]:
    params = {
        "method": "food_entry.create",
        "format": "json",
        "food_entry_name": f"Yurt - {yemek['name']}",
        "date": epoch_days,
        "meal": "dinner",  # Doğrudan Akşam Yemeği öğününe yazar
        "number_of_units": 1,
        "serving_description": "1 Porsiyon",
        "calories": yemek["calories"],
        "protein": yemek["protein"],
        "carbohydrate": yemek["carbs"],
        "fat": yemek["fat"],
    }
    r = oauth.post("https://platform.fatsecret.com/rest/server.api", params=params)
    print(yemek["name"], "->", r.status_code, r.text)
