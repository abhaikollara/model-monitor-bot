from flask import Flask
from flask import request
from bot import MonitorBot
import json

token = "<Your Telegram API Token here>"
monitorbot = MonitorBot(token)
monitorbot.start()

app = Flask(__name__)

url = "/model_monitor"
@app.route(url, methods=["GET", "POST"])
def update():
    data = request.get_json()
    monitorbot.send_update(data)
    return "Update recieved"

if __name__ == '__main__':
    app.run(debug=True)
