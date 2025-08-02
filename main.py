
import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Mioka Airdrop Bot is running."

if __name__ == "__main__":
    app.run(debug=True)
