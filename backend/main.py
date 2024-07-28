from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

base_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'GOOG', 'SPY', 'NVDA']
news_tables = {}

for ticker in tickers:
    url = base_url + ticker
    req = Request(url=url, headers={'User-Agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, 'html.parser')
    news_table = html.find(id="news-table")
    news_tables[ticker] = news_table

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
vader = SentimentIntensityAnalyzer()
df['compound'] = df['Title'].apply(lambda title: vader.polarity_scores(title)['compound'])
df['Date'] = pd.to_datetime(df['Date'], format='%b-%d-%y', errors='coerce')
df['date'] = df['Date'].dt.date


mean_df = df.groupby(['Ticker', 'date'])['compound'].mean().reset_index()
mean_df = mean_df.sort_values('date')

mean_df = mean_df[mean_df['date'].isin(mean_df['date'].unique()[-20:])] # specify how many dates it goes back


plt.figure(figsize=(12, 6))

# make sure tickers and dates are unique
tickers = mean_df['Ticker'].unique()
dates = mean_df['date'].unique()


bar_width = 0.8 / len(tickers)
r = np.arange(len(dates))


for i, ticker in enumerate(tickers):
    data = mean_df[mean_df['Ticker'] == ticker]

    # mask for the dates
    mask = np.isin(dates, data['date'])

    plt.bar(r[mask] + i * bar_width, data['compound'],
            width=bar_width, label=ticker, align='edge')

plt.ylabel('Compound Sentiment Score')
plt.title('Sentiment Analysis of Recent Stock News')
plt.xticks(r + bar_width * (len(tickers) - 1) / 2, [date.strftime('%Y-%m-%d') for date in dates], rotation=45)
plt.legend()

plt.tight_layout()
plt.show()

print(mean_df)