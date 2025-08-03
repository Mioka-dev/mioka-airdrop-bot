from flask import Flask
import threading
from bot import start_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "Mioka Airdrop Bot is Running!"

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000, debug=True)