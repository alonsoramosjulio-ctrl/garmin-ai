import os
import json
import garminconnect
from datetime import date

email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")

if not email or not password:
    raise ValueError("Faltan credenciales")

print(f"Conectando con {email}...")
client = garminconnect.Garmin(email, password)
client.login()

today = date.today()
resumen = f"# Garmin {today}\n"

try:
    hr = client.get_resting_heart_rate(today.isoformat())
    resumen += f"- FC reposo: {hr.get('restingHeartRate', 'N/A')} ppm\n"
except Exception as e:
    resumen += f"- FC reposo: no disponible\n"

try:
    sleep = client.get_sleep_data(today.isoformat())
    duracion = sleep.get('dailySleepDTO', {}).get('sleepTimeSeconds', 0) // 3600
    puntuacion = sleep.get('dailySleepDTO', {}).get('sleepScores', {}).get('overall', {}).get('value', 'N/A')
    resumen += f"- Sueno: {duracion}h (puntuacion {puntuacion})\n"
except Exception as e:
    resumen += f"- Sueno: no disponible\n"

try:
    hrv = client.get_hrv_data(today.isoformat())
    hrv_val = hrv.get('hrvSummary', {}).get('lastNight', 'N/A')
    resumen += f"- VFC: {hrv_val} ms\n"
except Exception as e:
    resumen += f"- VFC: no disponible\n"

try:
    steps = client.get_steps_data(today.isoformat())
    total = sum(s.get('steps', 0) for s in steps) if steps else 0
    resumen += f"- Pasos: {total}\n"
except Exception as e:
    resumen += f"- Pasos: no disponible\n"

os.makedirs("garmin/daily", exist_ok=True)
filename = f"garmin/daily/{today}.md"
with open(filename, "w") as f:
    f.write(resumen)

print(resumen)
print(f"Guardado en {filename}")
