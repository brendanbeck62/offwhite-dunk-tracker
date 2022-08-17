import sys
# required for lambda to use locally packaged requests module
# run: pip install --target ./package requests
sys.path.append("./package")

import requests
import json

class Dunk:
    def __init__(self, lot, price, colorway, img):
        self.lot = lot
        self.price = price
        self.colorway = colorway
        self.img = img

def query_stockx(query):
    endpoint = 'https://stockx.com/api/products/' + query + '?includes=market'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
    }
    return requests.get(endpoint, headers=headers)

def get_lot(lot):
    """
    Returns: a shoe object for the given lot
    """
    product = query_stockx(f'nike-dunk-low-off-white-lot-{lot}').json()['Product']

    for attribute, child in product['children'].items():
        if child['shoeSize'] == '12':
            # Note: the media block contains a '360' array, which provides all the pictures for the 360 carousel
            # Some lots seem to not have images in the 360 block, so check if they exist if you want to use it.
            # For now, just useing the imageurl attr that is also provided

            return Dunk(lot, child['market']['lowestAsk'], product['colorway'], product['media']['imageUrl'])

def get_lots():
    ret = []
    for lot in range(1, 5):
        #print(lot)
        ret.append(get_lot(lot))
    return ret

def lambda_handler(event, context):
    dunk_list = get_lots()
    dunk_list.sort(key=lambda x: x.price)
    return {
        'statusCode' : 200,
        'body': json.dumps([dunk.__dict__ for dunk in dunk_list])
    }


#print(lambda_handler(None, None))

