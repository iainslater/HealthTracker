import gspread
from google.oauth2.service_account import Credentials

from datetime import date


#SETUP GOOGLE SHEETS
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)


#GET SPECIFIC WORKSHEET
sheet_id = "133ANQxHIn9HAujVT6sEYhcEXSFYyBfLscDDl2Y0_ojM"
sheet = client.open_by_key(sheet_id)
worksheet = sheet.worksheet("TestSheet")


#GET DATE AND FORMAT
today = date.today()
formatted_date = today.strftime('%d/%m/%Y')
print(today)
print(formatted_date)


#SET UP LIST TO BE APPENDED
body=[formatted_date, 4, 9,7,5] #the values should be a list



#APPEND TO SHEET
worksheet.append_row(body, table_range="A1:A4")

#table_range should be range of columns in the sheet, example from A1 to E1 (A1:E1) other parameters are optional.

# this will append the values in body to the last row in the sheet and it will not overwrite existing data.