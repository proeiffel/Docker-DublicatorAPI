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

@app.route('/healthz', methods=['GET'])
def health_check():
    return "OK", 200

@app.route('/', methods=['POST'])
def handle_request():
    data = request.get_data()
    logging.info(f"📥 Gelen veri: {data}")

    # TARGET1'e gönderim
    try:
        r1 = requests.post(TARGET1, data=data, timeout=2, verify=True)
        logging.info(f"✅ TARGET1 ({TARGET1}) → Status: {r1.status_code}")
    except Exception as e:
        logging.error(f"❌ HATA - TARGET1 ({TARGET1}) → {type(e).__name__}: {e}")
        r1 = None

    # TARGET2'ye gönderim
    try:
        r2 = requests.post(TARGET2, data=data, timeout=2, verify=True)
        logging.info(f"✅ TARGET2 ({TARGET2}) → Status: {r2.status_code}")
    except Exception as e:
        logging.error(f"❌ HATA - TARGET2 ({TARGET2}) → {type(e).__name__}: {e}")

    if r1 and r1.status_code == 200:
        return (r1.content, r1.status_code, r1.headers.items())
    else:
        return "OK", 200

if __name__ == '__main__':
    listen_port = int(os.environ.get("LISTEN_PORT", "5000"))
    app.run(host="0.0.0.0", port=listen_port)
