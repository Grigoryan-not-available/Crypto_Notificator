import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

#API KEY FROM COINMARKETCAP
COINMARKETCAP_API_KEY = '971f6bdb-14a6-47d6-9ea2-85a7f6b2a139'

def telegram_bot_send_text(bot_message):
   bot_token = '5132347115:AAGjvEl0fOjNB0VfXaCssmbBHs3_kQCdNjc'
   bot_chatID = '-793057983'
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)

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
        jsonfromcoinmarketcapuah = get_the_current_exchange_rate(API=COINMARKETCAP_API_KEY, convert='UAH')
        jsonfromcoinmarketcapusd = get_the_current_exchange_rate(API=COINMARKETCAP_API_KEY, convert='USD')

        BTCExchangeRateUAH = round(float(jsonfromcoinmarketcapuah['data']['BTC'][0]['quote']['UAH']['price']), 3)
        ETHExchangeRateUAH = round(float(jsonfromcoinmarketcapuah['data']['ETH'][0]['quote']['UAH']['price']), 3)

        BTCExchangeRateUSD = round(float(jsonfromcoinmarketcapusd['data']['BTC'][0]['quote']['USD']['price']), 3)
        ETHExchangeRateUSD = round(float(jsonfromcoinmarketcapusd['data']['ETH'][0]['quote']['USD']['price']), 3)

        telegram_bot_send_text(f"BTC:"
                               f"\n*{BTCExchangeRateUSD}* _USD_"
                               f"\n*{BTCExchangeRateUAH}* _UAH_"
                               f"\nETH:"
                               f"\n*{ETHExchangeRateUSD}* _USD_"
                               f"\n*{ETHExchangeRateUAH}* _UAH_")
    except Exception as e:
        telegram_bot_send_text("Pls, check your script on server, something went wrong!"
                               f"\n{e}")