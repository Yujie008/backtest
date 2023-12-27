import requests
import time
from datetime import datetime
import random
import re
import math
import signal
my_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
# proxy = {
#      "http":"http://10.0.0.6:7890"
# }
def main():
     ### Nasdaq info ###
     url_NDX_PE = "https://danjuanfunds.com/djapi/index_eva/pe_history/NDX?day=all"
     url_NDX_PB = "https://danjuanfunds.com/djapi/index_eva/pb_history/NDX?day=all"
     url_NDX_PRICE = "https://danjuanfunds.com/djapi/fundx/base/index/nav/growth?symbol=GINDX&day=10y" #actually 20yrs
     ## PE
     #    r_NDX_PE = requests.get(url_NDX_PE,headers=my_headers,proxies=proxy,verify=False)
     r_NDX_PE = requests.get(url_NDX_PE,headers=my_headers)
     NDX_PEstr_s = re.findall('"pe":(.*?),"ts"',r_NDX_PE.text)
     NDX_PEnum_s = [float(x) for x in NDX_PEstr_s]
     PE_TSstr_s = re.findall('"ts":(.*?)}',r_NDX_PE.text)
     PE_TSnum_s = [int(x) for x in PE_TSstr_s]
     ## PB
     r_NDX_PB = requests.get(url_NDX_PB,headers=my_headers)
     NDX_PBstr_s = re.findall('"pb":(.*?),"ts"',r_NDX_PB.text)
     NDX_PBnum_s = [float(x) for x in NDX_PBstr_s]
     ## PRICE
     r_NDX_PRICE = requests.get(url_NDX_PRICE,headers=my_headers)
     NDX_PRICEstr_s = re.findall('"gr_nav":"(.*?)","gr_per"',r_NDX_PRICE.text)
     NDX_PRICE_DATE_str_s = re.findall('"date":"(.*?)","gr_nav"',r_NDX_PRICE.text)
     NDX_PRICEnum_s = [float(x) for x in NDX_PRICEstr_s]

     start_yr = 4 # start year of evaluation: from 1 - 10
     trace_yr = 0.05 # tracing back years from selected start year: from 1 - 9
     # strategy for NDX parameter
     PE_buy_thresh1,PE_buy_thresh2,PE_buy_thresh3 = 0.3,0.2,0.1
     PB_buy_thresh1,PB_buy_thresh2,PB_buy_thresh3 = 1.0,1.0,1.0
     PE_sell_thresh1,PE_sell_thresh2,PE_sell_thresh3 = 0.7,0.9,1.0
     PB_sell_thresh1,PB_sell_thresh2,PB_sell_thresh3 = 0.3,0.3,0.6
     # account input: 
     account_money = 100000.0
     buy_shares_1 = 30
     buy_shares_2 = 100
     buy_shares_3 = 100
     sell_shares_1 = 0
     sell_shares_2 = 30
     sell_shares_3 = 30
     account_shares = 0
     # use strategy1 on Nasdaq QQQM
     NDX2QQQM_ratio = 100
     print("initial QQQM account shares: ",account_shares,"\ninitial QQQM account money: ",account_money)
     NDX_account_shares,NDX_account_money,NDX_PRICEcurrent,NDX_long_hold_shares,NDX_long_hold_value,NDX_buy_price_list,NDX_sell_price_list,NDX_buy_date_list,NDX_sell_date_list,NDX_actual_buy_price_list,NDX_actual_buy_date_list,NDX_actual_sell_price_list,NDX_actual_sell_date_list\
            = strategy1(NDX_PEnum_s,PE_TSnum_s,NDX_PBnum_s,NDX_PRICEnum_s,NDX_PRICE_DATE_str_s,PE_buy_thresh1,PE_buy_thresh2,PE_buy_thresh3,PB_buy_thresh1,PB_buy_thresh2,PB_buy_thresh3,\
               PE_sell_thresh1,PE_sell_thresh2,PE_sell_thresh3,PB_sell_thresh1,PB_sell_thresh2,PB_sell_thresh3,\
                    account_money,account_shares,buy_shares_1,buy_shares_2,buy_shares_3,sell_shares_1,sell_shares_2,sell_shares_3,NDX2QQQM_ratio,start_yr,trace_yr)
     print("final QQQM account shares: ",NDX_account_shares,"\nfinal QQQM account money: ",NDX_account_money,"\nfinal QQQM shares and money combined: ",NDX_account_money+NDX_account_shares*NDX_PRICEcurrent/NDX2QQQM_ratio)
     print("QQQM shares if buy from start: ",NDX_long_hold_shares,"\nQQQM value if buy from start:",NDX_long_hold_value,"\n")
     ### SP500 info ###
     url_SP500_PE = "https://danjuanfunds.com/djapi/index_eva/pe_history/SP500?day=all"
     url_SP500_PB = "https://danjuanfunds.com/djapi/index_eva/pb_history/SP500?day=all"
     url_SP500_PRICE = "https://danjuanfunds.com/djapi/fundx/base/index/nav/growth?symbol=SPISP500&day=10y"
     # url_pb = "https://danjuanfunds.com/djapi/index_eva/pb_history/SP500?day=5y"

     ## PE
     r_SP500_PE = requests.get(url_SP500_PE,headers=my_headers)
     SP500_PEstr_s = re.findall('"pe":(.*?),"ts"',r_SP500_PE.text)
     SP500_PEnum_s = [float(x) for x in SP500_PEstr_s]
     PE_TSstr_s = re.findall('"ts":(.*?)}',r_SP500_PE.text)
     PE_TSnum_s = [int(x) for x in PE_TSstr_s]
     ## PB
     r_SP500_PB = requests.get(url_SP500_PB,headers=my_headers)
     SP500_PBstr_s = re.findall('"pb":(.*?),"ts"',r_SP500_PB.text)
     SP500_PBnum_s = [float(x) for x in SP500_PBstr_s]
     ## PRICE
     r_SP500_PRICE = requests.get(url_SP500_PRICE,headers=my_headers)
     SP500_PRICEstr_s = re.findall('"gr_nav":"(.*?)","gr_per"',r_SP500_PRICE.text)
     SP500_PRICE_DATE_str_s = re.findall('"date":"(.*?)","gr_nav"',r_SP500_PRICE.text)
     SP500_PRICEnum_s = [float(x) for x in SP500_PRICEstr_s]
     # strategy for SP500 parameter
     PE_buy_thresh1,PE_buy_thresh2,PE_buy_thresh3 = 0.3,0.2,0.1
     PB_buy_thresh1,PB_buy_thresh2,PB_buy_thresh3 = 1.0,1.0,1.0
     PE_sell_thresh1,PE_sell_thresh2,PE_sell_thresh3 = 0.7,0.9,1.0
     PB_sell_thresh1,PB_sell_thresh2,PB_sell_thresh3 = 0.3,0.3,1.0
     # account input: 
     account_money = 200000.0
     buy_shares_1 = 10
     buy_shares_2 = 20
     buy_shares_3 = 30
     sell_shares_1 = 0
     sell_shares_2 = 10
     sell_shares_3 = 30
     account_shares = 0
     # use strategy1 on SP500
     SPX2IVV_ratio = 10
     print("initial IVV account shares: ",account_shares,"\ninitial IVV account money: ",account_money)
     SP500_account_shares,SP500_account_money,SP500_PRICEcurrent,SP500_long_hold_shares,SP500_long_hold_value,SP500_buy_price_list,SP500_sell_price_list,SP500_buy_date_list,SP500_sell_date_list,SP500_actual_buy_price_list,SP500_actual_buy_date_list,SP500_actual_sell_price_list,SP500_actual_sell_date_list\
            = strategy1(SP500_PEnum_s,PE_TSnum_s,SP500_PBnum_s,SP500_PRICEnum_s,SP500_PRICE_DATE_str_s,PE_buy_thresh1,PE_buy_thresh2,PE_buy_thresh3,PB_buy_thresh1,PB_buy_thresh2,PB_buy_thresh3,\
               PE_sell_thresh1,PE_sell_thresh2,PE_sell_thresh3,PB_sell_thresh1,PB_sell_thresh2,PB_sell_thresh3,\
                    account_money,account_shares,buy_shares_1,buy_shares_2,buy_shares_3,sell_shares_1,sell_shares_2,sell_shares_3,SPX2IVV_ratio,start_yr,trace_yr)
     print("final IVV account shares: ",SP500_account_shares,"\nfinal IVV account money: ",SP500_account_money,"\nfinal IVV shares and money combined: ",SP500_account_money+SP500_account_shares*SP500_PRICEcurrent/SPX2IVV_ratio)
     print("SP500 shares if buy from start: ",SP500_long_hold_shares,"\nSP500 value if buy from start:",SP500_long_hold_value,"\n")
     signal.pause()

def strategy1(NDX_PEnum_s,PE_TSnum_s,NDX_PBnum_s,NDX_PRICEnum_s,NDX_PRICE_DATE_str_s,PE_buy_thresh1,PE_buy_thresh2,PE_buy_thresh3,PB_buy_thresh1,PB_buy_thresh2,PB_buy_thresh3,\
              PE_sell_thresh1,PE_sell_thresh2,PE_sell_thresh3,PB_sell_thresh1,PB_sell_thresh2,PB_sell_thresh3,\
               account_money,account_shares,buy_shares_1,buy_shares_2,buy_shares_3,sell_shares_1,sell_shares_2,sell_shares_3,index2fund_ratio,start_yr,trace_yr):
     # PE
     NDX_PEsorted_s = sorted(NDX_PEnum_s)
     NDX_PElen = len(NDX_PEsorted_s)
     NDX_PE10 = NDX_PEsorted_s[math.floor(PE_buy_thresh3*NDX_PElen)-1]
     NDX_PE20 = NDX_PEsorted_s[math.floor(PE_buy_thresh2*NDX_PElen)-1]
     NDX_PE30 = NDX_PEsorted_s[math.floor(PE_buy_thresh1*NDX_PElen)-1]
     NDX_PE70 = NDX_PEsorted_s[math.ceil(PE_sell_thresh1*NDX_PElen)-1]
     NDX_PE80 = NDX_PEsorted_s[math.ceil(PE_sell_thresh2*NDX_PElen)-1]
     NDX_PE90 = NDX_PEsorted_s[math.floor(PE_sell_thresh3*NDX_PElen)-1]
     NDX_PEcurrent = NDX_PEnum_s[NDX_PElen-1]
     # PE timing
     PE_TSs = [timeStamp(x) for x in PE_TSnum_s]
     # PB
     NDX_PBsorted_s = sorted(NDX_PBnum_s)
     NDX_PBlen = len(NDX_PBsorted_s)
     NDX_PB10 = NDX_PBsorted_s[math.floor(PB_buy_thresh3*NDX_PBlen)-1]
     NDX_PB20 = NDX_PBsorted_s[math.floor(PB_buy_thresh2*NDX_PBlen)-1]
     NDX_PB30 = NDX_PBsorted_s[math.floor(PB_buy_thresh1*NDX_PBlen)-1]
     NDX_PB70 = NDX_PBsorted_s[math.ceil(PB_sell_thresh1*NDX_PBlen)-1]
     NDX_PB80 = NDX_PBsorted_s[math.ceil(PB_sell_thresh2*NDX_PBlen)-1]
     NDX_PB90 = NDX_PBsorted_s[math.ceil(PB_sell_thresh3*NDX_PBlen)-1]
     NDX_PBcurrent = NDX_PBnum_s[NDX_PBlen-1]
     ## PRICE
     NDX_PRICEsorted_s = sorted(NDX_PRICEnum_s)
     NDX_PRICElen = len(NDX_PRICEsorted_s)
     NDX_PRICE20 = NDX_PRICEsorted_s[math.floor(0.2*NDX_PRICElen)-1]
     NDX_PRICE30 = NDX_PRICEsorted_s[math.floor(0.3*NDX_PRICElen)-1]
     NDX_PRICE70 = NDX_PRICEsorted_s[math.ceil(0.7*NDX_PRICElen)-1]
     NDX_PRICE80 = NDX_PRICEsorted_s[math.ceil(0.8*NDX_PRICElen)-1]
     NDX_PRICEcurrent = NDX_PRICEnum_s[NDX_PRICElen-1]
     long_hold_shares = math.floor(account_money/NDX_PRICEnum_s[math.ceil(NDX_PRICElen/20*(start_yr+10))]*index2fund_ratio)
     long_hold_value =  long_hold_shares * NDX_PRICEnum_s[-1]/index2fund_ratio
     #    if  NDX_PEcurrent > NDX_PE80 and NDX_PBcurrent > NDX_PB80:
     #         sell_NDX = 1
     #    else:
     #         sell_NDX = 0
     #    if NDX_PEcurrent < NDX_PE20 and NDX_PBcurrent < NDX_PB20:
     #         buy_NDX = 1
     #    else:
     #         buy_NDX = 0

     # date1 = datetime.strptime(NDX_PRICE_DATE_str_s[1],"%Y-%m-%d")
     # date2 = datetime.strptime(PE_TSs[0],"%Y-%m-%d")
     # duration = date1 - date2
     # date_diff = duration.days

     # account input: 
     # account_money = 100000.0
     # buy_shares_1 = 30
     # buy_shares_2 = 100
     # buy_shares_3 = 100
     # sell_shares_1 = 10
     # sell_shares_2 = 100
     # sell_shares_3 = 100
     # account_shares = 0
     #    account_shares_USD = 0
     # buy_price = 0
     buy_price_list = []
     buy_date_list = []
     sell_date_list = []
     sell_price_list = []
     actual_buy_price_list = []
     actual_buy_date_list = []
     actual_sell_date_list = []
     actual_sell_price_list = []
     start_idx = math.ceil(NDX_PElen/10*start_yr)
     trace_len_idx = math.ceil(NDX_PElen/10*trace_yr)
     # eval_start = math.ceil(NDX_PElen/2) # start the evaluation from the 6th yr, using the first 5 yrs as index
     for i in range(start_idx,NDX_PElen):
          # PE
          PEsorted_s = sorted(NDX_PEnum_s[i-trace_len_idx:i])
          PElen = len(PEsorted_s)
          PE10 = PEsorted_s[math.floor(PE_buy_thresh3*PElen)-1]
          PE20 = PEsorted_s[math.floor(PE_buy_thresh2*PElen)-1]
          PE30 = PEsorted_s[math.floor(PE_buy_thresh1*PElen)-1]
          PE70 = PEsorted_s[math.ceil(PE_sell_thresh1*PElen)-1]
          PE80 = PEsorted_s[math.ceil(PE_sell_thresh2*PElen)-1]
          PE90 = PEsorted_s[math.ceil(PE_sell_thresh3*PElen)-1]
          # PB
          PBsorted_s = sorted(NDX_PBnum_s[i-trace_len_idx:i])
          PBlen = len(PBsorted_s)
          PB10 = PBsorted_s[math.floor(PB_buy_thresh3*PBlen)-1]
          PB20 = PBsorted_s[math.floor(PB_buy_thresh2*PBlen)-1]
          PB30 = PBsorted_s[math.floor(PB_buy_thresh1*PBlen)-1]
          PB70 = PBsorted_s[math.ceil(PB_sell_thresh1*PBlen)-1]
          PB80 = PBsorted_s[math.ceil(PB_sell_thresh2*PBlen)-1]
          PB90 = PBsorted_s[math.ceil(PB_sell_thresh3*PBlen)-1]
          #    buy strategy 1 satisfied
          if NDX_PBnum_s[i] < PB30 and NDX_PEnum_s[i] < PE30:
               for j in range(NDX_PRICElen):
               #    find the corresponding price, using time
                    if i == NDX_PElen-1:
                         if NDX_PRICE_DATE_str_s[j] >= PE_TSs[i]:
                              #    buy price at QQQM
                              buy_price = NDX_PRICEnum_s[j]/index2fund_ratio
                              buy_price_list.append(buy_price)
                              buy_date = NDX_PRICE_DATE_str_s[j]
                              buy_date_list.append(buy_date)
                    elif NDX_PRICE_DATE_str_s[j] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                         #    buy price at QQQM
                         buy_price = NDX_PRICEnum_s[j]/index2fund_ratio
                         buy_price_list.append(buy_price)
                         buy_date = NDX_PRICE_DATE_str_s[j]
                         buy_date_list.append(buy_date)
                    else:
                         continue
               #    enough money
               if account_money >= buy_shares_1*buy_price and buy_shares_1>0:
                    account_shares = account_shares + buy_shares_1
                    account_money = account_money - buy_shares_1*buy_price
                    actual_buy_price_list.append(buy_price)
                    actual_buy_date_list.append(buy_date)
          #    buy strategy 2 satisfied
          if NDX_PBnum_s[i] < PB20 and NDX_PEnum_s[i] < PE20:
               for j in range(NDX_PRICElen):
               #    find the corresponding price, using time
                    if i == NDX_PElen-1:
                         if NDX_PRICE_DATE_str_s[j] >= PE_TSs[i]:
                              #    buy price at QQQM
                              buy_price = NDX_PRICEnum_s[j]/index2fund_ratio
                              buy_price_list.append(buy_price)
                              buy_date = NDX_PRICE_DATE_str_s[j]
                              buy_date_list.append(buy_date)
                    elif NDX_PRICE_DATE_str_s[j] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                         #    buy price at QQQM
                         buy_price = NDX_PRICEnum_s[j]/index2fund_ratio
                         buy_price_list.append(buy_price)
                         buy_date = NDX_PRICE_DATE_str_s[j]
                         buy_date_list.append(buy_date)
                    else:
                         continue
               #    enough money
               if account_money >= buy_shares_2*buy_price and buy_shares_2>0:
                    account_shares = account_shares + buy_shares_2
                    account_money = account_money - buy_shares_2*buy_price
                    actual_buy_price_list.append(buy_price)
                    actual_buy_date_list.append(buy_date)
          #    buy strategy 3 satisfied
          if NDX_PBnum_s[i] < PB10 and NDX_PEnum_s[i] < PE10:
               for j in range(NDX_PRICElen):
               #    find the corresponding price, using time
                    if i == NDX_PElen-1:
                         if NDX_PRICE_DATE_str_s[j] >= PE_TSs[i]:
                              #    buy price at QQQM
                              buy_price = NDX_PRICEnum_s[j]/index2fund_ratio
                              buy_price_list.append(buy_price)
                              buy_date = NDX_PRICE_DATE_str_s[j]
                              buy_date_list.append(buy_date)
                    elif NDX_PRICE_DATE_str_s[j] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                         #    buy price at QQQM
                         buy_price = NDX_PRICEnum_s[j]/index2fund_ratio
                         buy_price_list.append(buy_price)
                         buy_date = NDX_PRICE_DATE_str_s[j]
                         buy_date_list.append(buy_date)
                    else:
                         continue
               #    enough money
               if account_money >= buy_shares_3*buy_price and buy_shares_3>0:
                    account_shares = account_shares + buy_shares_3
                    account_money = account_money - buy_shares_3*buy_price
                    actual_buy_price_list.append(buy_price)
                    actual_buy_date_list.append(buy_date)

          #    sell strategy 1 satisfied
          if NDX_PBnum_s[i] > PB70 and NDX_PEnum_s[i] > PE70:
               for k in range(NDX_PRICElen):
               #    find the corresponding price, using time
                    if i == NDX_PElen-1:
                         if NDX_PRICE_DATE_str_s[k] >= PE_TSs[i]:
                              #    sell price at QQQM
                              sell_price = NDX_PRICEnum_s[k]/index2fund_ratio
                              sell_price_list.append(sell_price)
                              sell_date = NDX_PRICE_DATE_str_s[k]
                              sell_date_list.append(sell_date)
                    elif NDX_PRICE_DATE_str_s[k] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                         #    sell price at QQQM
                         sell_price = NDX_PRICEnum_s[k]/index2fund_ratio
                         sell_price_list.append(sell_price)
                         sell_date = NDX_PRICE_DATE_str_s[k]
                         sell_date_list.append(sell_date)
                    else:
                         continue
               #    enough shares
               if sell_shares_1 <= account_shares and sell_shares_1 > 0:
                    account_shares = account_shares - sell_shares_1
                    account_money = account_money + sell_shares_1*sell_price
                    actual_sell_price_list.append(sell_price)
                    actual_sell_date_list.append(sell_date)
                    
               #    sell strategy 2 satisfied
          if NDX_PBnum_s[i] > PB80 and NDX_PEnum_s[i] > PE80:
               for k in range(NDX_PRICElen):
               #    find the corresponding price, using time
                    if i == NDX_PElen-1:
                         if NDX_PRICE_DATE_str_s[k] >= PE_TSs[i]:
                              #    sell price at QQQM
                              sell_price = NDX_PRICEnum_s[k]/index2fund_ratio
                              sell_price_list.append(sell_price)
                              sell_date = NDX_PRICE_DATE_str_s[k]
                              sell_date_list.append(sell_date)
                    elif NDX_PRICE_DATE_str_s[k] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                         #    sell price at QQQM
                         sell_price = NDX_PRICEnum_s[k]/index2fund_ratio
                         sell_price_list.append(sell_price)
                         sell_date = NDX_PRICE_DATE_str_s[k]
                         sell_date_list.append(sell_date)
                    else:
                         continue
               #    enough shares
               if sell_shares_2 <= account_shares and sell_shares_2 > 0:
                    account_shares = account_shares - sell_shares_2
                    account_money = account_money + sell_shares_2*sell_price
                    actual_sell_price_list.append(sell_price)
                    actual_sell_date_list.append(sell_date)
               #    sell strategy 3 satisfied
          if NDX_PBnum_s[i] > PB90 and NDX_PEnum_s[i] > PE90:
               for k in range(NDX_PRICElen):
               #    find the corresponding price, using time
                    if i == NDX_PElen-1:
                         if NDX_PRICE_DATE_str_s[k] >= PE_TSs[i]:
                              #    sell price at QQQM
                              sell_price = NDX_PRICEnum_s[k]/index2fund_ratio
                              sell_price_list.append(sell_price)
                              sell_date = NDX_PRICE_DATE_str_s[k]
                              sell_date_list.append(sell_date)
                    elif NDX_PRICE_DATE_str_s[k] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                         #    sell price at QQQM
                         sell_price = NDX_PRICEnum_s[k]/index2fund_ratio
                         sell_price_list.append(sell_price)
                         sell_date = NDX_PRICE_DATE_str_s[k]
                         sell_date_list.append(sell_date)
                    else:
                         continue
               #    enough shares
               if sell_shares_3 <= account_shares and sell_shares_3 > 0:
                    account_shares = account_shares - sell_shares_3
                    account_money = account_money + sell_shares_3*sell_price
                    actual_sell_price_list.append(sell_price)
                    actual_sell_date_list.append(sell_date)
     return account_shares,account_money,NDX_PRICEcurrent,long_hold_shares,long_hold_value,buy_price_list,sell_price_list,buy_date_list,sell_date_list,\
          actual_buy_price_list,actual_buy_date_list,actual_sell_price_list,actual_sell_date_list


     # ### SP500 strategy ###
     # url_SP500_PE = "https://danjuanfunds.com/djapi/index_eva/pe_history/SP500?day=all"
     # url_SP500_PB = "https://danjuanfunds.com/djapi/index_eva/pb_history/SP500?day=all"
     # # url_pb = "https://danjuanfunds.com/djapi/index_eva/pb_history/SP500?day=5y"

     # ## PE
     # r_SP500_PE = requests.get(url_SP500_PE,headers=my_headers)
     # SP500_PEstr_s = re.findall('"pe":(.*?),"ts"',r_SP500_PE.text)
     # SP500_PEnum_s = [float(x) for x in SP500_PEstr_s]
     # SP500_PEsorted_s = sorted(SP500_PEnum_s)
     # SP500_PElen = len(SP500_PEsorted_s)
     # SP500_PE20 = SP500_PEsorted_s[math.floor(0.2*SP500_PElen)-1]
     # SP500_PE30 = SP500_PEsorted_s[math.floor(0.3*SP500_PElen)-1]
     # SP500_PE70 = SP500_PEsorted_s[math.ceil(0.7*SP500_PElen)-1]
     # SP500_PE80 = SP500_PEsorted_s[math.ceil(0.8*SP500_PElen)-1]
     # SP500_PEcurrent = SP500_PEnum_s[SP500_PElen-1]
     # ## PB
     # r_SP500_PB = requests.get(url_SP500_PB,headers=my_headers)
     # SP500_PBstr_s = re.findall('"pb":(.*?),"ts"',r_SP500_PB.text)
     # SP500_PBnum_s = [float(x) for x in SP500_PBstr_s]
     # SP500_PBsorted_s = sorted(SP500_PBnum_s)
     # SP500_PBlen = len(SP500_PBsorted_s)
     # SP500_PB20 = SP500_PBsorted_s[math.floor(0.2*SP500_PBlen)-1]
     # SP500_PB30 = SP500_PBsorted_s[math.floor(0.3*SP500_PBlen)-1]
     # SP500_PB70 = SP500_PBsorted_s[math.ceil(0.7*SP500_PBlen)-1]
     # SP500_PB80 = SP500_PBsorted_s[math.ceil(0.8*SP500_PBlen)-1]
     # SP500_PBcurrent = SP500_PBnum_s[SP500_PBlen-1]
     # if  SP500_PEcurrent > SP500_PE80 and SP500_PBcurrent > SP500_PB80:
     #      sell_SP500 = 1
     # else:
     #      sell_SP500 = 0
     # if SP500_PEcurrent < SP500_PE20 and SP500_PBcurrent < SP500_PB20:
     #      buy_SP500 = 1
     # else:
     #      buy_SP500 = 0

     # time.sleep(2)

# 输入毫秒级的时间，转出正常格式的时间
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray) # complex form with hour min sec
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray) # simple form wo hour min sec
    # print (otherStyleTime)
    return otherStyleTime

if __name__ == "__main__":
    main()
