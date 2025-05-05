from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

app = Flask(__name__)

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

# Replace with your actual Google Sheet ID
SPREADSHEET_ID = "your-google-sheet-id"
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

@app.route("/log_weight", methods=["POST"])
def log_weight():
    data = request.json
    weight = data.get("weight")

    if not weight:
        return jsonify({"error": "Weight is required"}), 400

    date_str = datetime.now().strftime("%d/%m/%y")  # UK format
    sheet.append_row([date_str, weight])

    return jsonify({"message": "Weight logged successfully!"})

@app.route("/", methods=["GET"])
def health_check():
    return "Weight Logger is running"

if __name__ == "__main__":
    app.run(debug=True)
