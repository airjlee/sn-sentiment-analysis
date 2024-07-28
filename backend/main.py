from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

base_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'AMD', 'FB']
for ticker in tickers:
    url = base_url + ticker
    req = Request(url=url, headers={'User-Agent': 'my-app'})
    response = urlopen(req)
    print(response)

    html = BeautifulSoup(response, 'html')
    break