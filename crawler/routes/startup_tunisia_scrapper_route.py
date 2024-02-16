from flask import Flask
from models.startup import StartupTunisia

app = Flask(__name__)

# Define the route for scraping
@app.route('/scrape', methods=['GET'])
def scrape_startups():
    StartupTunisia.to_extract('https://startup.gov.tn/fr/database')
