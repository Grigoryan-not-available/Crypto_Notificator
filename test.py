from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from time import time
from pprint import pprint


def get_the_current_exchange_rate():
    url = f'https://api.monobank.ua/personal/statement/{"lzHTmg7h6fG7atbc2r1HvA"}/{int(time()) - 3600 * 24 * 31}/{int(time())}'
    #url = f'https://api.monobank.ua/personal/client-info'

    headers = {
        'Accepts': 'application/json',
        'X-Token': 'uNqyKeMWSznyiTVNnICo28BCyAuCzVP07RlcedLJIiEc'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


if __name__ == '__main__':
    pprint(get_the_current_exchange_rate() if 'errorDescription' not in get_the_current_exchange_rate() else get_the_current_exchange_rate()['errorDescription'])
    # print(int(time()) - 3600 * 24 * 30)
