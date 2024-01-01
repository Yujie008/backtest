import json
import signal
import strategy2 as st2
# import alpha_api
# api_key = alpha_api.api_key
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url_eps = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=AAPL&apikey=' + api_key
# url_price_w = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=AAPL&apikey=' + api_key
# r = requests.get(url_eps)
stock_code = 'META'
with open('logs_alpha/23-12-30/'+stock_code+'_EPS.json', 'r') as file:
    data_raw = file.read()
data = json.loads(data_raw) # convert to dictionary
quarterlyEarnings = data["quarterlyEarnings"]
EPS_date,EPS_value = [],[]
len_EPS = len(quarterlyEarnings)
for i_e in range(len_EPS):
    value = quarterlyEarnings[i_e]
    EPS_date.append(value["fiscalDateEnding"])
    EPS_value.append(float(value["reportedEPS"]))
EPS_date.reverse()
EPS_value.reverse()
with open('logs_alpha/23-12-30/'+stock_code+'_adjusted_w.json', 'r') as file:
    data_raw = file.read()
data = json.loads(data_raw) # convert to dictionary
weekly_adjusted_timeseries = data["Weekly Adjusted Time Series"]
price_weekly_date,price_weekly_close,price_weekly_adj_close = [],[],[]
price_weekly_date = list(weekly_adjusted_timeseries.keys())
len_price_weekly = len(price_weekly_date)
for i_p in range(len_price_weekly):
    price_weekly_value = weekly_adjusted_timeseries[price_weekly_date[i_p]]
    price_weekly_close.append(float(price_weekly_value['4. close']))
    price_weekly_adj_close.append(float(price_weekly_value['5. adjusted close']))
price_weekly_date.reverse()
price_weekly_close.reverse()
price_weekly_adj_close.reverse()
PE_weekly_value = []
for i in range(len_price_weekly):
    for j in range(len_EPS-1):
        if price_weekly_date[i]>EPS_date[j] and price_weekly_date[i]<=EPS_date[j+1]:
            # if i == 201:# for test
            #     a = 1
            EPS_date_sel = EPS_value[j]
            break
        else:
            EPS_date_sel = EPS_value[-1]
    PE_weekly_value.append(price_weekly_adj_close[i]/EPS_date_sel)
# strategy for SP500 parameter
PE_buy_thresh1,PE_buy_thresh2,PE_buy_thresh3 = 0.3,0.2,0.1
# PB_buy_thresh1,PB_buy_thresh2,PB_buy_thresh3 = 1.0,1.0,1.0
PE_sell_thresh1,PE_sell_thresh2,PE_sell_thresh3 = 0.7,0.9,1.0
# PB_sell_thresh1,PB_sell_thresh2,PB_sell_thresh3 = 0.3,0.3,1.0
# account input: 
account_money = 200000.0
buy_shares_1 = 10
buy_shares_2 = 30
buy_shares_3 = 50
sell_shares_1 = 0
sell_shares_2 = 10
sell_shares_3 = 30
account_shares = 0
# use strategy2 on TSLA
index2fund_ratio = 1
start_yr,trace_wks = 7,12
account_shares,account_money,PRICEcurrent,long_hold_shares,long_hold_value,buy_price_list,sell_price_list,buy_date_list,sell_date_list,\
          actual_buy_price_list,actual_buy_date_list,actual_sell_price_list,actual_sell_date_list\
= st2.strategy2(PE_weekly_value,stock_code,price_weekly_adj_close,price_weekly_date,PE_buy_thresh1,PE_buy_thresh2,PE_buy_thresh3,\
              PE_sell_thresh1,PE_sell_thresh2,PE_sell_thresh3,\
               account_money,account_shares,buy_shares_1,buy_shares_2,buy_shares_3,sell_shares_1,sell_shares_2,sell_shares_3,index2fund_ratio,start_yr,trace_wks)
signal.pause()
# print(data)

# https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=AAPL&apikey=TGO4S15TZKGFJDIF
# https://www.alphavantage.co/query?function=SMA&symbol=AAPL&interval=daily&time_period=1&series_type=close&apikey=TGO4S15TZKGFJDIF
# https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=AAPL&apikey=TGO4S15TZKGFJDIF
# https://www.alphavantage.co/query?function=EARNINGS&symbol=AAPL&apikey=TGO4S15TZKGFJDIF
# https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=MSFT&apikey=TGO4S15TZKGFJDIF
# https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=GOOGL&apikey=TGO4S15TZKGFJDIF
# https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=NVDA&apikey=TGO4S15TZKGFJDIF
# https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=daily&maturity=10year&apikey=TGO4S15TZKGFJDIF
# https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=daily&apikey=TGO4S15TZKGFJDIF