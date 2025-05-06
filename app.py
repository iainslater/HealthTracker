from flask import Flask, request, jsonify
import gspread
from datetime import datetime
import os
import json
from google.oauth2.service_account import Credentials



app = Flask(__name__)

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

# Replace with your actual Google Sheet ID
sheet_id = "133ANQxHIn9HAujVT6sEYhcEXSFYyBfLscDDl2Y0_ojM"
sheet = client.open_by_key(sheet_id)
worksheet = sheet.worksheet("TestSheet")

@app.route("/log_weight", methods=["POST"])
def log_weight():
    data = request.json
    weight = data.get("weight")

    if not weight:
        return jsonify({"error": "Weight is required"}), 400

    date_str = datetime.now().strftime("%d/%m/%y")  # UK format
    worksheet.append_row([date_str, weight])

    return jsonify({"message": "Weight logged successfully!"})

@app.route("/", methods=["GET"])
def health_check():
    return "Weight Logger is running"

if __name__ == "__main__":
    app.run(debug=True)
