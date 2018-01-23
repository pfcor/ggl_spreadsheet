import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("parlamentares").sheet1
 
# Extract and print all of the values
# list_of_vals = sheet.get_all_values()
rows_as_dicts = sheet.get_all_records()
df = pd.DataFrame(rows_as_dicts)
print(df.head(3))