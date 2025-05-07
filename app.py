from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from analyze_food import analyze_food_image  # Your working vision script
from werkzeug.utils import secure_filename

#make a change

app = Flask(__name__)
CORS(app)  # Required to allow GitHub Pages to POST to this backend

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

# Replace with your actual Google Sheet ID
sheet_id = "133ANQxHIn9HAujVT6sEYhcEXSFYyBfLscDDl2Y0_ojM"
sheet = client.open_by_key(sheet_id)
# Get worksheets by name (or index)
live_sheet = sheet.worksheet("Live")  # Change "Live" to match your real worksheet name
test_sheet = sheet.worksheet("TestSheet")  # And your test worksheet name poo

@app.route("/analyze_food", methods=["POST"])
def analyze_food():
    image = request.files["image"]
    path = "/tmp/uploaded_food.jpg"
    image.save(path)
    result = analyze_food_image(path)
    return jsonify({"result": result})


@app.route("/log_weight", methods=["POST"])
def log_weight():
    data = request.json
    weight = data.get("weight", "")
    girth = data.get("girth", "")
    mood = data.get("mood", "")
    mode = data.get("mode", "live")  # default to live


    # If a file was uploaded, save and analyze it
    if "photo" in request.files:
        photo = request.files["photo"]
        if photo.filename != "":
            filename = secure_filename(photo.filename)
            tmp_path = os.path.join("/tmp", filename)  # use /tmp for Render
            photo.save(tmp_path)
            analysis = analyze_food_image(tmp_path)
        else:
            analysis = None
    else:
        analysis = None

    date_str = datetime.now().strftime("%d/%m/%y")  # UK format

    #get worksheet and append
    worksheet = test_sheet if mode == "test" else live_sheet
    worksheet.append_row([date_str, weight, girth, mood, analysis])

    return jsonify({"message": "Entry logged successfully!"})

@app.route("/", methods=["GET"])
def health_check():
    return "Weight Logger is running"

if __name__ == "__main__":
    app.run(debug=True)
