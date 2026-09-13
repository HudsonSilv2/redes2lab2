import json
import time
import xml.etree.ElementTree as ET

import requests

# ──────────────────────────────────────────────
#  Dados base (mesmo objeto para JSON e XML)
# ──────────────────────────────────────────────
user_data = {
    "name": "Hudson Silva",
    "email": "hudson@university.edu",
    "id": 2026001,
    "ip_address": "192.168.1.25",
    "device_name": "hudson-notebook",
    "operating_system": "Ubuntu Linux",
    "start_connection": "2026-09-12 14:00:00",
    "end_connection": "2026-09-12 16:00:00",
    "errors": [
        {
            "date_time": "2026-09-12 15:15:00",
            "message": "Connection timeout",
            "priority_level": "Medium",
        }
    ],
}

SERVER_URL = "http://server:5000"

# Aguardar o servidor estar pronto
print("=" * 60)
print("  CLIENTE DE SERIALIZAÇÃO – Atividade 1")
print("=" * 60)
print("\nAguardando servidor ficar disponível...")

for attempt in range(1, 11):
    try:
        r = requests.get(SERVER_URL, timeout=2)
        if r.status_code == 200:
            print(f"  Servidor respondeu na tentativa {attempt}.\n")
            break
    except requests.exceptions.ConnectionError:
        pass
    time.sleep(1)
else:
    print("  ERRO: Servidor não respondeu após 10 tentativas.")
    exit(1)

# ──────────────────────────────────────────────
#  1. Serialização JSON
# ──────────────────────────────────────────────
print("-" * 60)
print("  1) SERIALIZAÇÃO JSON")
print("-" * 60)

json_payload = json.dumps(user_data, indent=4)
json_size = len(json_payload.encode("utf-8"))

print(json_payload)
print(f"\n  Tamanho do payload JSON: {json_size} bytes")

response = requests.post(
    f"{SERVER_URL}/json",
    data=json_payload,
    headers={"Content-Type": "application/json"},
)

print(f"  Resposta do servidor: {response.text.strip()}")

# ──────────────────────────────────────────────
#  2. Serialização XML
# ──────────────────────────────────────────────
print()
print("-" * 60)
print("  2) SERIALIZAÇÃO XML")
print("-" * 60)

root = ET.Element("userConnection")

for key, value in user_data.items():

    if key == "errors":
        errors_element = ET.SubElement(root, "errors")

        for error in value:
            error_element = ET.SubElement(errors_element, "error")

            for error_key, error_value in error.items():
                child = ET.SubElement(error_element, error_key)
                child.text = str(error_value)

    else:
        child = ET.SubElement(root, key)
        child.text = str(value)

xml_payload = ET.tostring(root, encoding="utf-8", xml_declaration=True)
xml_size = len(xml_payload)

print(xml_payload.decode("utf-8"))
print(f"\n  Tamanho do payload XML: {xml_size} bytes")

response = requests.post(
    f"{SERVER_URL}/xml",
    data=xml_payload,
    headers={"Content-Type": "application/xml"},
)

print(f"  Resposta do servidor: {response.text.strip()}")

# ──────────────────────────────────────────────
#  3. Comparativo de tamanho
# ──────────────────────────────────────────────
print()
print("=" * 60)
print("  COMPARATIVO DE TAMANHO")
print("=" * 60)
print(f"  JSON: {json_size} bytes")
print(f"  XML:  {xml_size} bytes")

diff = xml_size - json_size
pct = (diff / json_size) * 100 if json_size > 0 else 0

print(f"  Diferença: XML é {diff} bytes maior ({pct:.1f}% a mais)")
print("=" * 60)
print("\nCliente finalizado com sucesso.")
