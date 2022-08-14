import requests
from stockxsdk import Stockx


def init_stockx():
    stockx = Stockx()
    product_id = stockx.get_first_product_id('BB1234')
    print(product_id)

def get_dunks():
    pass

def lambda_handler(event, context):
    result = "Hello World"
    return {
        'statusCode' : 200,
        'body': result
    }

init_stockx()
print(lambda_handler(None, None))
