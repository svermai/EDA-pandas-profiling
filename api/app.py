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
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)
        report_path = '/tmp/report.html'
        profile.to_file(report_path)
        
        return jsonify({'message': 'Report generated successfully!', 'report_path': report_path}), 200
    else:
        return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

