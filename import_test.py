import pandas as pd
import akshare as ak
import finplot as fplt

df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230601", end_date='20240101', adjust="qfq")
# stock_us_hist_df = ak.stock_us_hist(symbol='105.MTP', period="daily", start_date="19700101", end_date="22220101", adjust="qfq")
# print(stock_us_hist_df)
# df = ak.stock_us_hist(symbol="105.MTP", period="daily", start_date="20230601", end_date='20231101', adjust="qfq")
print(df)
df = df.iloc[:, 0:6]
df.日期 = pd.to_datetime(df.日期)
# # 列名记得这样定义好
df.columns = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
df.set_index('Date', inplace=True)

fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
fplt.show()