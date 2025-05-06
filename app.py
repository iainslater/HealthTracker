from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials



app = Flask(__name__)
CORS(app)  # Required to allow GitHub Pages to POST to this backend

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
    weight = data.get("weight", "").strip()
    girth = data.get("girth", "").strip()

    date_str = datetime.now().strftime("%d/%m/%y")  # UK format

    # Append all three columns: date, weight (or ""), girth (or "")
    worksheet.append_row([date_str, weight, girth])

    return jsonify({"message": "Weight and girth logged successfully!"})

@app.route("/", methods=["GET"])
def health_check():
    return "Weight Logger is running"

if __name__ == "__main__":
    app.run(debug=True)
