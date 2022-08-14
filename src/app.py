import requests
from stockxsdk import Stockx
from stockxsdk.product import StockxProduct

def search(query):
    endpoint = 'https://stockx.com/api/products/' + query + '?includes=market'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
    }
    return requests.get(endpoint, headers=headers).json()

def init_stockx():
    response = search('nike-blazer-low-off-white-university-red')
    print(response['Product']['title'])

def get_dunks():
    pass

def lambda_handler(event, context):
    result = "Hello World"
    return {
        'statusCode' : 200,
        'body': result
    }

init_stockx()
#print(lambda_handler(None, None))
