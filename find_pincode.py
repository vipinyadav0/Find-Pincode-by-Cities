import requests
from bs4 import BeautifulSoup
import re
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from cities import places


def search_pincode(search):
    '''
    :param search: search fior the state, city, or district
    :return: list of pinocodes
    '''
    pin_codes = []
    url = 'https://www.google.com/search?q=' + search + " " + 'pincode'
    result = requests.get(url)

    if result.status_code == 200:

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(result.content, 'html.parser')
        
        # Find all div tags on the page
        links = soup.find_all('div')
        if links:
            for link in links:
                text = link.get_text('Pin Code:')
        
                match = re.search(r'Pin Code:(\d{6})', text)  # Regex to match the pin code from the text say only digits and of length 6

                if match:
                    pin_code = match.group(1)
                    if pin_code:
                        return [search ,pin_code]
    else:
        print(f"Failed to crawl {url}")

    return pin_codes


res =[]
for place in places:

    x = search_pincode(f'{place}')
    res.append(x)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# spredsheet example: https://docs.google.com/spreadsheets/d/1k9b6bUdMQ-bBUIBPAoW539VGpQtTVwr77tT24c-98Ui/edit#gid=0

SAMPLE_SPREADSHEET_ID = '' # id from example

def update_google_sheet( pin_codes):  
    '''
    :param pin_codes: list of pinocdes
    :return: None
    '''
    # Connect to Google Sheets API
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('./google_credentials.json', scopes)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                                    range="Sheet2!A2",
                                                    valueInputOption='USER_ENTERED',
                                                    insertDataOption='INSERT_ROWS',
                                                    body={"values": pin_codes}).execute()

update_google_sheet(res)
