import quandl
import time
quandl.ApiConfig.api_key = 'LiFY28cshQ6ayGphjUad'
sp500_div_yield_month = quandl.get('MULTPL/SP500_DIV_YIELD_MONTH',start_date='2020-12-31',end_date='2023-12-31')
sp500_div_yield_month_head = sp500_div_yield_month.head()
goog_pr = quandl.get('WIKI/GOOGL',start_date='2020-10-1',end_date='2023-11-30')
# tsla_pr = quandl.get('WIKI/TSLA',start_date='2020-12-31',end_date='2023-11-31')
aapl_pr = quandl.get('WIKI/AAPL',start_date='2020-12-31',end_date='2023-11-30')
time.pause()