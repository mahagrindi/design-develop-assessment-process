from flask import Flask, jsonify
from service.scrapper import Scrapper

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    try:
        scrapper = Scrapper('https://startup.gov.tn/fr/database')
        startups = scrapper.scrape()
        return jsonify({'status': 'success', 'startups': startups})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})