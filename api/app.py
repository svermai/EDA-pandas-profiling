from flask import Flask, request, jsonify
from flask_cors import CORS
from ydata_profiling import ProfileReport
import pandas as pd
import os

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set the static folder for storing the report
STATIC_DIR = os.path.join(os.getcwd(), "static")

@app.route('/', methods=['GET'])
def home():
    return 'Flask app running!'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    # Ensure static directory exists
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    # Generate the profile report from the uploaded CSV
    profile = ProfileReport(pd.read_csv(file), title="EDA Report")
    report_path = os.path.join(STATIC_DIR, "EDA_report.html")
    profile.to_file(report_path)
    
    # Return the URL for the generated report
    return jsonify({"report_url": request.host_url + "static/EDA_report.html"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

