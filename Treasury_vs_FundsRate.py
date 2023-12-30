import json,matplotlib
import signal
import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')
start_date = "2000-01-01"
stock_code = 'ten_yr_treasury_yield_dataonly'
with open('logs_alpha/23-12-30/'+stock_code+'.txt', 'r') as file:
    data_raw = file.read()
data0 = json.loads(data_raw) # convert to dictionary
ten_yr_treasury_rate_total = data0["data"]
ten_yr_treasury_rate_sel,ten_yr_treasury_rate_date =[],[]
for i_e in range(len(ten_yr_treasury_rate_total)-1):
    try:
        ten_yr_treasury_value = float(ten_yr_treasury_rate_total[i_e]["value"])
        ten_yr_treasury_rate_sel.append(ten_yr_treasury_value)
        ten_yr_treasury_rate_date.append(ten_yr_treasury_rate_total[i_e]["date"])
    except:
        continue        
    if ten_yr_treasury_rate_total[i_e]["date"]>start_date and ten_yr_treasury_rate_total[i_e+1]["date"]<start_date:
        break
ten_yr_treasury_rate_sel.reverse(),ten_yr_treasury_rate_date.reverse()
# matplotlib.use('Agg')
plt.plot(ten_yr_treasury_rate_date,ten_yr_treasury_rate_sel)
# plt.title("Value vs Time")
plt.xlabel('Time Span')
plt.ylabel('Value')
plt.show()
# EPS_date,EPS_value = [],[]
# len_EPS = len(quarterlyEarnings)
# for i_e in range(len_EPS):
#     value = quarterlyEarnings[i_e]
#     EPS_date.append(value["fiscalDateEnding"])
#     EPS_value.append(float(value["reportedEPS"]))
# EPS_date.reverse()
# EPS_value.reverse()