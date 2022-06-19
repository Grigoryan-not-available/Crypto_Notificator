import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Файл, полученный в Google Developer Console
credentials = 'crypto-340910-2368bbb4ea66.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet = '1lB5u7CIrZpA1a_aU1t83VM7lADatfAzCzJ8PLYjl05s'

# API KEY FROM COINMARKETCAP
COINMARKETCAP_API_KEY = '971f6bdb-14a6-47d6-9ea2-85a7f6b2a139'


def telegram_bot_send_text(bot_message):
    bot_token = '5132347115:AAGjvEl0fOjNB0VfXaCssmbBHs3_kQCdNjc'
    bot_chatID = '-793057983'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)


def get_data_from_google_spreadsheet(CREDENTIALS_FILE, spreadsheet_id):
    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Пример чтения файла
    range = ['D2:E3', 'I2:J3', 'A3', 'F3']

    values = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=range
    ).execute()

    BTC = float(values['valueRanges'][2]['values'][0][0].replace(',', '.'))
    ETH = float(values['valueRanges'][3]['values'][0][0].replace(',', '.'))
    BTCinUAH = abs(float(values['valueRanges'][0]['values'][0][0].replace(',', '.')))
    ETHinUAH = abs(float(values['valueRanges'][1]['values'][0][0].replace(',', '.')))
    return BTC, ETH, BTCinUAH, ETHinUAH


def get_the_current_exchange_rate(API, convert):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'BTC,ETH',
        'convert': convert
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


if __name__ == '__main__':
    try:
        BTC, ETH, BTCinUAH, ETHinUAH = get_data_from_google_spreadsheet(credentials, spreadsheet)

        jsonfromcoinmarketcap = get_the_current_exchange_rate(API=COINMARKETCAP_API_KEY, convert='UAH')
        BTCExchangeRate = float(jsonfromcoinmarketcap['data']['BTC'][0]['quote']['UAH']['price'])
        ETHExchangeRate = float(jsonfromcoinmarketcap['data']['ETH'][0]['quote']['UAH']['price'])

        CurrentValueMyBTC = BTCExchangeRate * BTC
        CurrentValueMyETH = ETHExchangeRate * ETH

        if CurrentValueMyBTC + CurrentValueMyETH >= (BTCinUAH + ETHinUAH) * 1.5:
            for i in range(20):
                telegram_bot_send_text(
                    f'*SELL ALL!!SELL ALL!!SELL ALL!!*\nSUMM *{CurrentValueMyETH + CurrentValueMyBTC}* '
                    f'MORE THEN {(BTCinUAH + ETHinUAH) * 1.5}!!!\nBTC={CurrentValueMyBTC}, ETH={CurrentValueMyETH}')
    except:
        telegram_bot_send_text("Pls, check your script on server, something went wrong!")