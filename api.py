from cds_pdf_scraper import runPDFScraper
from flask import Flask, request, send_from_directory, render_template
import os 
import sys
import logging

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/convert', methods=['GET'])
def convert():
    url = request.args.get('url')
    response = runPDFScraper(url)
    if (response['status']) == '200 OK':
        return send_from_directory(CURRENT_DIRECTORY, response['data'], as_attachment=True)
    else:
        return "<h1>" + response['status'] + "</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user support
    app.run(threaded=True, port=5000)
