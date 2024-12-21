#!.venv/bin/python3
from flask import Flask, request, jsonify
import requests
import os
import bcrypt
import json
import webbrowser as browser
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"}), 200

@app.route('/get-strats', methods=['GET'])
def get_strats():
    with open('client/strats/strats.json', 'r') as f:
        strats = json.load(f)
    return jsonify(strats), 200

@app.route('/strat', methods=['GET'])
def strat():
    strat: str = request.args.get('name')
    with open(f'client/strats/{strat.removesuffix(".js")}.js', 'r') as f:
        content = f.read()
    return content, 200

@app.route('/hash', methods=['GET'])
def hash():
    email = request.args.get('email')
    password = request.args.get('password')

    salt_url = f"https://api.sorare.com/api/v1/users/{email}"

    salt_response = requests.get(salt_url)

    salt: str = salt_response.json()["salt"]

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

    return hashed_password, 200

for root, _, paths in os.walk('client'):
    for path in paths:
        @app.route(f'/{os.path.join(root, path).removeprefix("client/")}', methods=['GET'], endpoint=os.path.join(root, path).removeprefix("client/"))
        def callback(path=os.path.join(root, path)):
            print(path)
            with open(path, "r") as f:
                content = f.read()
            return content

if __name__ == '__main__':
    browser.open(f"file://{os.path.abspath('start.html')}")
    app.run(host='0.0.0.0', port=5000)