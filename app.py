from flask import Flask, request
from flask_cors import CORS
from Controllers.extractData import MarketDataScraper, NLP
# from Controllers.chatController import NLP

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods = ['POST'])
def upload():
    scraper = MarketDataScraper(request.json['url'])
    print("======1",scraper.data)
    market_data = scraper.scrape_market_data()
    print("=======2",scraper.data)
    return "fetched"

@app.route('/chat', methods = ['POST'])
def chat():
    return NLP(request.json['question'])



if __name__ == "__main__":
    app.run(debug=True)
