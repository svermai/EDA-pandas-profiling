from flask import Flask, request, jsonify
from ydata_profiling import ProfileReport
import pandas as pd
import os
import logging

app = Flask(__name__)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
def home():
    return 'Flask app running!'

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        app.logger.debug(f"Received file: {file.filename}")

        # Process the CSV and generate the HTML report
        df = pd.read_csv(file)
        app.logger.debug(f"Dataframe shape: {df.shape}")

        profile = ProfileReport(df, title="EDA Report")
        report_path = os.path.join("static", "EDA_report.html")

        # Ensure the static directory exists
        os.makedirs("static", exist_ok=True)

        profile.to_file(report_path)
        app.logger.debug(f"Report saved to: {report_path}")
        
        # Return the path to the generated file
        return jsonify({"report_url": request.host_url + report_path})
    
    except Exception as e:
        app.logger.error(f"Error processing file: {e}")
        return jsonify({"error": "Failed to process file"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

