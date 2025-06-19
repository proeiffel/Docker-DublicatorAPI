from flask import Flask, request
import requests
import os
import logging

app = Flask(__name__)

log_dir = os.environ.get("LOG_DIR", "/logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=f"{log_dir}/duplicator.log", level=logging.INFO)

TARGET1 = os.environ.get("TARGET1")
TARGET2 = os.environ.get("TARGET2")
FORWARD_IF_RESP_TARGET = os.environ.get("FORWARD_IF_RESP_TARGET")

@app.route('/healthz', methods=['GET'])
def health_check():
    return "OK", 200

@app.route('/', methods=['POST'])
def handle_request():
    data = request.get_data()
    logging.info(f"📥 Gelen veri: {data}")

    responses = []

    for idx, target in enumerate([TARGET1, TARGET2], start=1):
        try:
            r = requests.post(f"http://{target}", data=data, timeout=2)
            responses.append((target, r.status_code))
            logging.info(f"➡️ {target} → Status: {r.status_code}")
            if idx == 1 and r.status_code == 200 and FORWARD_IF_RESP_TARGET:
                try:
                    fwd = requests.post(f"http://{FORWARD_IF_RESP_TARGET}", data=r.content, timeout=2)
                    logging.info(f"🔁 Yanıt {FORWARD_IF_RESP_TARGET}'ye gönderildi → {fwd.status_code}")
                except Exception as e:
                    logging.error(f"🚨 {FORWARD_IF_RESP_TARGET}'ye gönderim hatası: {e}")
        except Exception as e:
            logging.error(f"🚨 {target} gönderim hatası: {e}")

    return "OK", 200

if __name__ == '__main__':
    listen_port = int(os.environ.get("LISTEN_PORT", "5000"))
    app.run(host="0.0.0.0", port=listen_port)
