from flask import Flask, request, jsonify
import json
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

DATA_DIR = "/app/data"


@app.route("/json", methods=["POST"])
def receive_json():
    data = request.get_json()

    print("\nJSON recebido:")
    print(json.dumps(data, indent=4))

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(f"{DATA_DIR}/json_received.json", "w") as file:
        json.dump(data, file, indent=4)

    return jsonify({
        "message": "JSON recebido com sucesso"
    }), 200


@app.route("/xml", methods=["POST"])
def receive_xml():
    xml_data = request.data

    root = ET.fromstring(xml_data)

    print("\nXML recebido:")
    print(xml_data.decode("utf-8"))

    os.makedirs(DATA_DIR, exist_ok=True)

    with open(f"{DATA_DIR}/xml_received.xml", "wb") as file:
        file.write(xml_data)

    return jsonify({
        "message": "XML recebido com sucesso"
    }), 200


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Servidor funcionando"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
