from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

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

parsed_data = []
for ticker, news_table in news_tables.items():
    if news_table:  # Check if news_table is not None
        for row in news_table.findAll('tr'):
            link = row.find('a')
            date_td = row.find('td')
            if link and date_td:
                title = link.text
                date_data = date_td.text.strip().split(' ')

                if len(date_data) == 1:
                    date = ''
                    time = date_data[0]
                else:
                    date = date_data[0]
                    if date == "Today":
                        date = datetime.today().strftime('%b-%d-%y')
                    time = date_data[1]

                parsed_data.append([ticker, date, time, title])

df = pd.DataFrame(parsed_data, columns=['Ticker', 'Date', 'Time', 'Title'])
