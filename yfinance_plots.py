import finplot as fplt
import yfinance as yf

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

stock_i = yf.download('AAPL','2023-01-01',auto_adjust=True)
print(stock_i)
apple = yf.Ticker('SOXX')
actions = apple.actions
splits = apple.splits
earnings_dates = apple.get_earnings_dates(limit = 15)
balance_sheet = apple.balance_sheet
print(earnings_dates)
print(balance_sheet)