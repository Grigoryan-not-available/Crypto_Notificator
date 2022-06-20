from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from pprint import pprint
from requests import Session
import json

api_key='r2Sp2YXnB9szy23PNhnNSUn7lxBC5IW231HgokwszjYMAsIGCpbrGAdRu4T4bPSW'
api_secret='4iUDISmRA4Uw6JswEdJen49y2GX9WsH8r3iwOI487OZ3DngvcKbY6kwbmEfGeW0W'

def get_data_from_binance(client):
    list_assets = []
    for i in client.get_account()['balances']:
        try:
            if float(i['free']) > 0.00000000:
                list_assets.append(i)
        except Exception as e:
            return e

    for i in list_assets:
        print(client.get_asset_balance(asset=i['asset']))
    return list_assets

if __name__ == '__main__':
    #pprint(get_data_from_binance())
    client = Client(api_key, api_secret)
    #pprint(get_data_from_binance(client))
    pprint(client.get_all_orders(symbol='ETHUAH'))
