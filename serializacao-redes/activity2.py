import json
import hashlib
import msgpack
import xml.etree.ElementTree as ET

student = {
    "first_name": "Hudson",
    "last_name": "Silva",
    "grade": 9.0,
    "id": 2026001,
    "age": 25,
    "address": {
        "country": "Brazil",
        "state": "Rio Grande do Norte",
        "city": "Natal",
        "street": "Rua Exemplo",
        "number": 100
    },
    "phone": "84999999999"
}

json_data = json.dumps(
    student,
    ensure_ascii=False,
    separators=(",", ":")
).encode("utf-8")

def dict_to_xml(parent, data):
    for key, value in data.items():
        element = ET.SubElement(parent, key)
        if isinstance(value, dict):
            dict_to_xml(element, value)
        else:
            element.text = str(value)

root = ET.Element("student")
dict_to_xml(root, student)
xml_data = ET.tostring(root, encoding="utf-8")

msgpack_data = msgpack.packb(
    student,
    use_bin_type=True
)

print("\n===== JSON =====")
print(json_data.decode("utf-8"))

print("\n===== XML =====")
print(xml_data.decode("utf-8"))

print("\n===== MESSAGEPACK =====")
print(msgpack_data)

student_deserialized = msgpack.unpackb(
    msgpack_data,
    raw=False
)

print("\n===== MESSAGEPACK DESSERIALIZADO =====")
print(student_deserialized)

print("\n===== TAMANHO DOS PAYLOADS =====")
print(f"JSON: {len(json_data)} bytes")
print(f"XML: {len(xml_data)} bytes")
print(f"MessagePack: {len(msgpack_data)} bytes")

json_md5 = hashlib.md5(json_data).hexdigest()
xml_md5 = hashlib.md5(xml_data).hexdigest()
msgpack_md5 = hashlib.md5(msgpack_data).hexdigest()

print("\n===== HASH MD5 =====")
print(f"JSON:        {json_md5}")
print(f"XML:         {xml_md5}")
print(f"MessagePack: {msgpack_md5}")
