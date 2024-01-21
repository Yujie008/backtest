import finplot as fplt
import yfinance as yf
import pandas as pd
import finplot as fplt
import numpy as np
import math,copy
# data = [(instrument, yf.download(instrument, '2020-10-01')) for instrument in ('AAPL','GOOG','TSLA')]
# for i,(instrument_a,dfa) in enumerate(data):
#     for instrument_b,dfb in data[i+1:]:
#         # ax = fplt.create_plot(instrument_a+' vs. '+instrument_b+' (green/brown)', maximize=False)
#         ax = fplt.create_plot(instrument_b)
#         dfa['Open Close High Low'.split()].plot(kind='candle', ax=ax)
#         # pb = dfb['Open Close High Low'.split()].plot(kind='candle', ax=ax.overlay(scale=1.0))
#         # pb.colors['bull_body'] = '#0f0'
#         # pb.colors['bear_body'] = '#630'
# fplt.show()
stock_names = ["AAPL","TSLA","MSFT",'NVDA','META','AMD']
start_date = '2022-01-01'
PE_traced = 66 # using the last 40 working days PE
PE_low_band_percent,PE_high_band_percent = 0.2,0.8
for stock_i in stock_names:
    df_US = yf.download(stock_i,start_date,auto_adjust=True)
    # print(df_US)
    # df_US.date = pd.to_datetime(df_US.date)
    df_US.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    # df_US.set_index('Date', inplace=True)
    # df_US = df_US[start_date: ]
    # print(df_US)
    ax1, ax2, ax3, ax4 = fplt.create_plot(stock_i, rows=4)
    ax1.set_visible(xgrid=True, ygrid=True)
    # plot macd with standard colors first
    macd = df_US.Close.ewm(span=12).mean() - df_US.Close.ewm(span=26).mean()
    signal = macd.ewm(span=9).mean()
    df_US['macd_diff'] = macd - signal
    fplt.volume_ocv(df_US[[ 'Open', 'Close', 'macd_diff']], ax=ax4, colorfunc=fplt.strength_colorfilter)
    fplt.plot(macd, ax=ax4, legend='MACD')
    fplt.plot(signal, ax=ax4, legend='MACD Signal')
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
        df.rsi.plot(ax=ax, legend='RSI_'+str(band_low)+'--'+str(band_high))
        fplt.set_y_range(0, 100, ax=ax)
        fplt.add_band(band_low, band_high, ax=ax)
    fplt.candlestick_ochl(df_US[['Open', 'Close', 'High', 'Low']], ax = ax1)
    plot_rsi(df_US, ax2, 10, 25, 75)
    ax11 = ax1.overlay()
    fplt.volume_ocv(df_US[['Open', 'Close', 'Volume']], ax=ax11)
    fplt.plot(df_US.Volume.ewm(span=24).mean(), ax=ax11, color=1)
    stock_ticker = yf.Ticker(stock_i)
    earnings_dates = stock_ticker.get_earnings_dates(limit = 20)
    print(earnings_dates)
    earnings_dates.columns = ['EPS_Estimate','Reported_EPS','Surprise(%)']
    # print(df_US)
    p_length = df_US.shape[0]
    e_length = earnings_dates.shape[0]
    # PE_daily = np.zeros((1,p_length))
    PE_daily = []
    PE_sorted = np.zeros((1,PE_traced))
    # PE_low_band = np.zeros((p_length,1))
    # PE_high_band = np.zeros((p_length,1))
    ii = 0
    for date_i in df_US.index.tz_localize('America/New_York'):
    # for date_i in df_US.index:
        jj = 0
        for date_e in earnings_dates.index:
            if date_i>date_e:
                Reported_EPS = earnings_dates.Reported_EPS[jj]
                break
            jj = jj+1
        if Reported_EPS>=0 and Reported_EPS<1e-2:
            Reported_EPS_adjusted = 0.01
        elif Reported_EPS<=0 and Reported_EPS>-1e-2:
            Reported_EPS_adjusted = -0.01
        else: 
            Reported_EPS_adjusted = Reported_EPS
        PE_daily.append(df_US.Close[ii]/Reported_EPS_adjusted)
        ii = ii+1
    df_US['PE_daily'] = np.transpose(PE_daily)
    # PE_low_band,PE_high_band = np.transpose(PE_daily),np.transpose(PE_daily)
    PE_low_band,PE_high_band = PE_daily[:PE_traced],PE_daily[:PE_traced]
    for kk in range(p_length):
        if kk > PE_traced-1:
            # PE_daily_copy = copy.deepcopy(PE_daily)
            PE_rolling = PE_daily[(kk-PE_traced):kk]
            PE_sorted = sorted(PE_rolling)
            PE_low_band.append(PE_sorted[math.floor(PE_traced*PE_low_band_percent)])
            PE_high_band.append(PE_sorted[math.ceil(PE_traced*PE_high_band_percent)])
            # PE_sorted = np.zeros((1,PE_traced))
    df_US['PE_low_band'] = PE_low_band
    df_US['PE_high_band'] = PE_high_band
    fplt.plot(df_US.PE_daily, ax=ax3, legend='PE_daily')
    fplt.plot(df_US.PE_low_band, ax=ax3, legend='PE_low_band')
    fplt.plot(df_US.PE_high_band, ax=ax3, legend='PE_high_band')
fplt.show()
# apple = yf.Ticker(stock_i)
# actions = apple.actions
# splits = apple.splits
# earnings_dates = apple.get_earnings_dates(limit = 15)
# balance_sheet = apple.balance_sheet
# print(earnings_dates)
# print(balance_sheet)

# to test PE calculation only
# stock_i = 'NVDA'
# start_date = '2023-01-01'
# df_US = yf.download(stock_i,start_date,auto_adjust=True)
# stock_ticker = yf.Ticker(stock_i)
# earnings_dates = stock_ticker.get_earnings_dates(limit = 20)
# earnings_dates.columns = ['EPS_Estimate','Reported_EPS','Surprise(%)']
# print(df_US)
# p_length = df_US.shape[0]
# e_length = earnings_dates.shape[0]
# PE_daily = np.zeros((p_length,1))
# ii = 0
# for date_i in df_US.index.tz_localize('America/New_York'):
# for date_i in df_US.index:
#     jj = 0
#     for date_e in earnings_dates.index:
#         if date_i>date_e:
#             Reported_EPS = earnings_dates.Reported_EPS[jj]
#             break
#         jj = jj+1
#     if Reported_EPS>=0 and Reported_EPS<1e-2:
#         Reported_EPS_adjusted = 0.01
#     elif Reported_EPS<=0 and Reported_EPS>-1e-2:
#         Reported_EPS_adjusted = -0.01
#     else: 
#         Reported_EPS_adjusted = Reported_EPS
#     PE_daily[ii] = df_US.Close[ii]/Reported_EPS_adjusted
#     ii = ii+1
# df_US['PE_daily'] = PE_daily
# print(earnings_dates)
# print(PE_daily)