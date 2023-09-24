import requests
import os
import time
import webbrowser
from PIL import Image
from selenium import webdriver
from flask import Flask, request
from flask_cors import CORS
from flask_ngrok import run_with_ngrok


app = Flask(__name__)
run_with_ngrok(app)
CORS(app)


@app.route('/', methods=['POST'])
def generate_qr_code():
    apiSecret = request.form['apiSecret']
    botNumber = request.form['botNumber']
    botLanguage = request.form['botLanguage']
    botSpeaker = request.form['botSpeaker']
    max_Users = request.form['maxUsers']

    create = {
    "secret": apiSecret
    }

    r = requests.post(url = "https://sendify.app/api/create/whatsapp", params = create)

    if r.status_code == 200:
        result = r.json()
        qrimagelink = result['data']['qrimagelink']
        driver = webdriver.Chrome()
        driver.get(qrimagelink)
        # Countdown for 12 seconds
        for i in range(12, 0, -1):
            print(f"Closing the browser in {i} seconds...")
            time.sleep(1)
        driver.close()
    
        accounts = requests.get('https://sendify.app/api/get/wa.accounts', params = create)
        accounts = accounts.json()
        id = accounts['data'][0]['id']
        phone = accounts['data'][0]['phone']
        print(f"id : {id}, phone: {phone}")

        # Insert these to the db, botNumber, botLanguage, botSpeaker, max_Users, id, phone (id and phone are generated from QR code)
        # add here the post to db code

        # end of post to db code
        return 'Bot Created Successfully.', 200
    else:
        return 'Error', 500

if __name__ == "__main__":
    app.run()