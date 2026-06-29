import os
import garminconnect
from datetime import date

email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")

if not email or not password:
    raise ValueError("GARMIN_EMAIL y GARMIN_PASSWORD deben estar configurados")

print(f"Conectando con {email}...")
client = garminconnect.Garmin(email, password)
client.login()

today = date.today()
print(f"\n=== Datos de hoy ({today}) ===")

try:
    steps = client.get_steps_data(today.isoformat())
    print(f"Pasos: {steps}")
except Exception as e:
    print(f"Pasos: no disponible ({e})")

try:
    hr = client.get_resting_heart_rate(today.isoformat())
    print(f"FC en reposo: {hr}")
except Exception as e:
