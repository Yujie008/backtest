import pandas as pd
import akshare as ak
import finplot as fplt
import numpy as np
import warnings
warnings.simplefilter(action="ignore", category=Warning)
# stock_us_hist_df = ak.stock_us_hist(symbol='AAPL', start_date="19700101", end_date="22220101", adjust="qfq")
# print(stock_us_hist_df)

# df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230601", end_date='20240101', adjust="qfq")
# # stock_us_hist_df = ak.stock_us_hist(symbol='105.MTP', period="daily", start_date="19700101", end_date="22220101", adjust="qfq")
# # print(stock_us_hist_df)
# # df = ak.stock_us_daily(symbol="AAPL",  adjust="qfq")
# print(df)
# df = df.iloc[:, 0:6]
# df.日期 = pd.to_datetime(df.日期)
# # # 列名记得这样定义好
# df.columns = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
# df.set_index('Date', inplace=True)
# fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
# fplt.show()
# stock_names = ["AAPL","TSLA","SOXX",'TLT','QQQM']
stock_names = ["AAPL","TSLA","MSFT"]
start_date = "2023-01-01"
for stock_i in stock_names:
    df_US = ak.stock_us_daily(symbol=stock_i,  adjust="qfq")
    # print(df_US)
    # df_US = df_US.iloc[:, 0:6]

    df_US.date = pd.to_datetime(df_US.date)
    df_US.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df_US.set_index('Date', inplace=True)
    df_US = df_US[start_date: ]
    # print(df_US)
    ax1, ax2, ax3 = fplt.create_plot(stock_i, rows=3)
    ax1.set_visible(xgrid=True, ygrid=True)
    # plot macd with standard colors first
    macd = df_US.Close.ewm(span=12).mean() - df_US.Close.ewm(span=26).mean()
    signal = macd.ewm(span=9).mean()
    df_US['macd_diff'] = macd - signal
    fplt.volume_ocv(df_US[[ 'Open', 'Close', 'macd_diff']], ax=ax3, colorfunc=fplt.strength_colorfilter)
    fplt.plot(macd, ax=ax3, legend='MACD')
    fplt.plot(signal, ax=ax3, legend='MACD Signal')

    def plot_rsi(df, ax, length, band_low, band_high):
        diff = df.Close.diff().values
        gains = diff
        losses = -diff
        with np.errstate(invalid='ignore'):
            gains[(gains < 0) | np.isnan(gains)] = 0.0
            losses[(losses <= 0) | np.isnan(losses)] = 1e-10  # we don't want divide by zero/NaN
        n = length
        m = (n - 1) / n
        ni = 1 / n
        g = gains[n] = np.nanmean(gains[:n])
        l = losses[n] = np.nanmean(losses[:n])
        gains[:n] = losses[:n] = np.nan
        for i, v in enumerate(gains[n:], n):
            g = gains[i] = ni * v + m * g
        for i, v in enumerate(losses[n:], n):
            l = losses[i] = ni * v + m * l
        rs = gains / losses
        df['rsi'] = 100 - (100 / (1 + rs))
        df.rsi.plot(ax=ax, legend='RSI')
        fplt.set_y_range(0, 100, ax=ax)
        fplt.add_band(band_low, band_high, ax=ax)

    fplt.candlestick_ochl(df_US[['Open', 'Close', 'High', 'Low']], ax = ax1)
    plot_rsi(df_US, ax2, 10, 25, 75)
    ax11 = ax1.overlay()
    fplt.volume_ocv(df_US[['Open', 'Close', 'Volume']], ax=ax11)
    fplt.plot(df_US.Volume.ewm(span=24).mean(), ax=ax11, color=1)
    fplt.autoviewrestore()
# fplt.candlestick_ochl(df_US[['Open', 'High', 'Low', 'Close']])
fplt.show()

# df_US = ak.stock_us_daily(symbol="TSLA",  adjust="qfq")
# # print(df_US)
# # df_US = df_US.iloc[:, 0:6]

# df_US.date = pd.to_datetime(df_US.date)
# df_US.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
# df_US.set_index('Date', inplace=True)
# df_US = df_US["2015-04-01": "2020-04-29"]
# print(df_US)
# ax3, ax4 = fplt.create_plot("TSLA", rows=2)
# fplt.candlestick_ochl(df_US[['Open', 'Close', 'High', 'Low']], ax = ax3)
# fplt.volume_ocv(df_US[['Open', 'Close', 'Volume']], ax=ax4)
# # fplt.candlestick_ochl(df_US[['Open', 'High', 'Low', 'Close']])
# fplt.show()