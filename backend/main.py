from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

base_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'AMD', 'FB']
news_tables = {}
for ticker in tickers:
    url = base_url + ticker
    req = Request(url=url, headers={'User-Agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, 'html.parser')
    news_table = html.find(id="news-table")
    news_tables[ticker] = news_table
    break

print(news_tables)