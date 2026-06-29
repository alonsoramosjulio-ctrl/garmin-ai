import os
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
print(f"Datos de hoy: {today}")

try:
    steps = client.get_steps_data(today.isoformat())
    print(f"Pasos: {steps}")
except Exception as e:
    print(f"Pasos no disponible: {e}")

try:
    hr = client.get_resting_heart_rate(today.isoformat())
    print(f"FC reposo: {hr}")
except Exception as e:
    print(f"FC no disponible: {e}")

try:
    sleep = client.get_sleep_data(today.isoformat())
    print(f"Sueno: {sleep}")
except Exception as e:
    print(f"Sueno no disponible: {e}")

print("Sync completado.")
