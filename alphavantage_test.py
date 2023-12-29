import requests
import time,re
import alpha_api
api_key = alpha_api.api_key
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url_eps = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=AAPL&apikey=' + api_key
url_price_w = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=AAPL&apikey=' + api_key
r = requests.get(url_eps)
data = r.json()
quarterlyEarnings = data["quarterlyEarnings"]
EPS_date,EPS_value = [],[]
for i in range(len(quarterlyEarnings)):
    value = quarterlyEarnings[i]
    EPS_date.append(value["fiscalDateEnding"])
    EPS_value.append(value["reportedEPS"])

r = requests.get(url_price_w)
data = r.json()
weekly_adjusted_timeseries = data["Weekly Adjusted Time Series"]
price_weekly_date,price_weekly_value = [],[]
for i in range(len(weekly_adjusted_timeseries)):
    a = weekly_adjusted_timeseries[i]
    b = a.keys()
    price_weekly_date_key = weekly_adjusted_timeseries[i].keys()
    price_weekly_date.append(price_weekly_date_key)
    value = weekly_adjusted_timeseries[i]
    price_weekly_value.append(value[price_weekly_date_key])
time.pause()
# print(data)