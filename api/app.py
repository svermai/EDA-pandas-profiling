# api/app.py
from flask import Flask, request, jsonify
from ydata_profiling import ProfileReport
import pandas as pd
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Flask app running!'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Process the CSV and generate the HTML report
    profile = ProfileReport(pd.read_csv(file), title="EDA Report")
    report_path = "static/EDA_report.html"
    profile.to_file(report_path)
    
    # Return the path to the generated file
    return jsonify({"report_url": request.host_url + report_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

