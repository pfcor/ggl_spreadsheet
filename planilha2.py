import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# use creds to create a client to interact with the Google Drive API
scope = [
    'https://spreadsheets.google.com/feeds', 
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
print(client)
# print(dir(client))
ss = client.create('teste_ss')
print(dir(ss))
print(ss.id)
ss.insert_permission(ss.id, 'pedrocorreia.rs@gmail.com', 'user', 'owner')
print(ss.list_permissions())
ws = ss.add_worksheet('teste_ws', 30, 10)
# print(dir(ws))
# spreadsheet = client.create('teste')
# print(dir(spreadsheet))
# sheet = spreadsheet.worksheet('Sheet1')
# row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
# index = 1
# ws.insert_row(row, index)