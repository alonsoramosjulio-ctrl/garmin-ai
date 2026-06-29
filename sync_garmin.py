import os
import requests
import garminconnect
from datetime import date

email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")
token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

print(f"Token: {token[:10] if token else 'VACIO'}")
print(f"Chat ID: {chat_id}")

client = garminconnect.Garmin(email, password)
client.login()

today = date.today()
msg = f"Garmin {today}\n"

try:
    sleep = client.get_sleep_data(today.isoformat())
    h = sleep.get('dailySleepDTO', {}).get('sleepTimeSeconds', 0) // 3600
    msg += f"Sueno: {h}h\n"
except:
    msg += "Sueno: no disponible\n"

try:
    acts = client.get_activities(0, 3)
    for a in acts:
        msg += f"- {a.get('startTimeLocal','')[:10]} {a.get('activityName','')} {int(a.get('duration',0))//60}min\n"
except:
    msg += "Entrenamientos: no disponible\n"

print(msg)

if token and chat_id:
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": msg})
    print(f"Status: {r.status_code}")
    print(f"Respuesta: {r.text}")
else:
    print("ERROR: token o chat_id vacios")
