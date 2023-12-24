import requests
import time
from datetime import datetime
import random
import re
import math
my_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
# proxy = {
#      "http":"http://10.0.0.6:7890"
# }
def main():
    #while (True):
        ### Nasdaq strategy ###
        url_NDX_PE = "https://danjuanfunds.com/djapi/index_eva/pe_history/NDX?day=5y"
        url_NDX_PB = "https://danjuanfunds.com/djapi/index_eva/pb_history/NDX?day=5y"
        url_NDX_PRICE = "https://danjuanfunds.com/djapi/fundx/base/index/nav/growth?symbol=GINDX&day=5y"

        ## PE
     #    r_NDX_PE = requests.get(url_NDX_PE,headers=my_headers,proxies=proxy,verify=False)
        r_NDX_PE = requests.get(url_NDX_PE,headers=my_headers)
        NDX_PEstr_s = re.findall('"pe":(.*?),"ts"',r_NDX_PE.text)
        NDX_PEnum_s = [float(x) for x in NDX_PEstr_s]
        NDX_PEsorted_s = sorted(NDX_PEnum_s)
        NDX_PElen = len(NDX_PEsorted_s)
        NDX_PE10 = NDX_PEsorted_s[math.floor(0.1*NDX_PElen)-1]
        NDX_PE20 = NDX_PEsorted_s[math.floor(0.2*NDX_PElen)-1]
        NDX_PE30 = NDX_PEsorted_s[math.floor(0.3*NDX_PElen)-1]
        NDX_PE70 = NDX_PEsorted_s[math.ceil(0.7*NDX_PElen)-1]
        NDX_PE80 = NDX_PEsorted_s[math.ceil(0.8*NDX_PElen)-1]
        NDX_PE90 = NDX_PEsorted_s[math.floor(0.9*NDX_PElen)-1]
        NDX_PEcurrent = NDX_PEnum_s[NDX_PElen-1]
        ## PB
        r_NDX_PB = requests.get(url_NDX_PB,headers=my_headers)
        NDX_PBstr_s = re.findall('"pb":(.*?),"ts"',r_NDX_PB.text)
        NDX_PBnum_s = [float(x) for x in NDX_PBstr_s]
        NDX_PBsorted_s = sorted(NDX_PBnum_s)
        NDX_PBlen = len(NDX_PBsorted_s)
        NDX_PB10 = NDX_PBsorted_s[math.floor(0.1*NDX_PBlen)-1]
        NDX_PB20 = NDX_PBsorted_s[math.floor(0.2*NDX_PBlen)-1]
        NDX_PB30 = NDX_PBsorted_s[math.floor(0.3*NDX_PBlen)-1]
        NDX_PB70 = NDX_PBsorted_s[math.ceil(0.7*NDX_PBlen)-1]
        NDX_PB80 = NDX_PBsorted_s[math.ceil(0.8*NDX_PBlen)-1]
        NDX_PB90 = NDX_PBsorted_s[math.ceil(0.9*NDX_PBlen)-1]
        NDX_PBcurrent = NDX_PBnum_s[NDX_PBlen-1]
        ## PRICE
        r_NDX_PRICE = requests.get(url_NDX_PRICE,headers=my_headers)
        NDX_PRICEstr_s = re.findall('"gr_nav":"(.*?)","gr_per"',r_NDX_PRICE.text)
        NDX_PRICE_DATE_str_s = re.findall('"date":"(.*?)","gr_nav"',r_NDX_PRICE.text)
        NDX_PRICEnum_s = [float(x) for x in NDX_PRICEstr_s]
        NDX_PRICEsorted_s = sorted(NDX_PRICEnum_s)
        NDX_PRICElen = len(NDX_PRICEsorted_s)
        NDX_PRICE20 = NDX_PRICEsorted_s[math.floor(0.2*NDX_PRICElen)-1]
        NDX_PRICE30 = NDX_PRICEsorted_s[math.floor(0.3*NDX_PRICElen)-1]
        NDX_PRICE70 = NDX_PRICEsorted_s[math.ceil(0.7*NDX_PRICElen)-1]
        NDX_PRICE80 = NDX_PRICEsorted_s[math.ceil(0.8*NDX_PRICElen)-1]
        NDX_PRICEcurrent = NDX_PRICEnum_s[NDX_PRICElen-1]
     #    if  NDX_PEcurrent > NDX_PE80 and NDX_PBcurrent > NDX_PB80:
     #         sell_NDX = 1
     #    else:
     #         sell_NDX = 0
     #    if NDX_PEcurrent < NDX_PE20 and NDX_PBcurrent < NDX_PB20:
     #         buy_NDX = 1
     #    else:
     #         buy_NDX = 0
        PE_TSstr_s = re.findall('"ts":(.*?)}',r_NDX_PE.text)
        PE_TSnum_s = [int(x) for x in PE_TSstr_s]
        PE_TSs = [timeStamp(x) for x in PE_TSnum_s]

        date1 = datetime.strptime(NDX_PRICE_DATE_str_s[1],"%Y-%m-%d")
        date2 = datetime.strptime(PE_TSs[0],"%Y-%m-%d")
        duration = date1 - date2
        date_diff = duration.days
     #    to match date between price and PE
        if NDX_PRICE_DATE_str_s[1] < PE_TSs[0]:
             price_early = 1
        else:
             price_early = 0
# account input: 
        account_money = 100000.0
        buy_shares_1 = 30
        buy_shares_2 = 100
        buy_shares_3 = 100
        sell_shares_1 = 10
        sell_shares_2 = 100
        sell_shares_3 = 100
        account_shares = 0
     #    account_shares_USD = 0
        buy_price = 0
        buy_price_list = []
        buy_date = []
        sell_date = []
        sell_price_list = []
        for i in range(NDX_PElen):
             #    buy strategy 1 satisfied
             if NDX_PBnum_s[i] < NDX_PB30 and NDX_PEnum_s[i] < NDX_PE30:
                  for j in range(NDX_PRICElen):
                    #    find the corresponding price, using time
                       if i == NDX_PElen-1:
                            if NDX_PRICE_DATE_str_s[j] >= PE_TSs[i]:
                                 #    buy price at QQQM
                                   buy_price = NDX_PRICEnum_s[j]/100
                                   buy_price_list.append(buy_price)
                                   buy_date.append(NDX_PRICE_DATE_str_s[j])
                       elif NDX_PRICE_DATE_str_s[j] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                            #    buy price at QQQM
                            buy_price = NDX_PRICEnum_s[j]/100
                            buy_price_list.append(buy_price)
                            buy_date.append(NDX_PRICE_DATE_str_s[j])
                       else:
                            continue
                  #    enough money
                  if account_money >= buy_shares_1*buy_price:
                    account_shares = account_shares + buy_shares_1
                    account_money = account_money - buy_shares_1*buy_price
             #    buy strategy 2 satisfied
             if NDX_PBnum_s[i] < NDX_PB20 and NDX_PEnum_s[i] < NDX_PE20:
                  for j in range(NDX_PRICElen):
                    #    find the corresponding price, using time
                       if i == NDX_PElen-1:
                            if NDX_PRICE_DATE_str_s[j] >= PE_TSs[i]:
                                 #    buy price at QQQM
                                   buy_price = NDX_PRICEnum_s[j]/100
                                   buy_price_list.append(buy_price)
                                   buy_date.append(NDX_PRICE_DATE_str_s[j])
                       elif NDX_PRICE_DATE_str_s[j] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                            #    buy price at QQQM
                            buy_price = NDX_PRICEnum_s[j]/100
                            buy_price_list.append(buy_price)
                            buy_date.append(NDX_PRICE_DATE_str_s[j])
                       else:
                            continue
                  #    enough money
                  if account_money >= buy_shares_2*buy_price:
                    account_shares = account_shares + buy_shares_2
                    account_money = account_money - buy_shares_2*buy_price
             #    buy strategy 3 satisfied
             if NDX_PBnum_s[i] < NDX_PB10 and NDX_PEnum_s[i] < NDX_PE10:
                  for j in range(NDX_PRICElen):
                    #    find the corresponding price, using time
                       if i == NDX_PElen-1:
                            if NDX_PRICE_DATE_str_s[j] >= PE_TSs[i]:
                                 #    buy price at QQQM
                                   buy_price = NDX_PRICEnum_s[j]/100
                                   buy_price_list.append(buy_price)
                                   buy_date.append(NDX_PRICE_DATE_str_s[j])
                       elif NDX_PRICE_DATE_str_s[j] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                            #    buy price at QQQM
                            buy_price = NDX_PRICEnum_s[j]/100
                            buy_price_list.append(buy_price)
                            buy_date.append(NDX_PRICE_DATE_str_s[j])
                       else:
                            continue
                  #    enough money
                  if account_money >= buy_shares_3*buy_price:
                    account_shares = account_shares + buy_shares_3
                    account_money = account_money - buy_shares_3*buy_price

             #    sell strategy 1 satisfied
             if NDX_PBnum_s[i] > NDX_PB70 and NDX_PEnum_s[i] > NDX_PE70:
                  for k in range(NDX_PRICElen):
                    #    find the corresponding price, using time
                       if i == NDX_PElen-1:
                            if NDX_PRICE_DATE_str_s[k] >= PE_TSs[i]:
                                 #    sell price at QQQM
                                   sell_price = NDX_PRICEnum_s[k]/100
                                   sell_price_list.append(sell_price)
                                   sell_date.append(NDX_PRICE_DATE_str_s[k])
                       elif NDX_PRICE_DATE_str_s[k] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                            #    sell price at QQQM
                            sell_price = NDX_PRICEnum_s[k]/100
                            sell_price_list.append(sell_price)
                            sell_date.append(NDX_PRICE_DATE_str_s[k])
                       else:
                            continue
                  #    enough shares
                  if sell_shares_1 <= account_shares:
                    account_shares = account_shares - sell_shares_1
                    account_money = account_money + sell_shares_1*sell_price
                    #    sell strategy 2 satisfied
             if NDX_PBnum_s[i] > NDX_PB80 and NDX_PEnum_s[i] > NDX_PE80:
                  for k in range(NDX_PRICElen):
                    #    find the corresponding price, using time
                       if i == NDX_PElen-1:
                            if NDX_PRICE_DATE_str_s[k] >= PE_TSs[i]:
                                 #    sell price at QQQM
                                   sell_price = NDX_PRICEnum_s[k]/100
                                   sell_price_list.append(sell_price)
                                   sell_date.append(NDX_PRICE_DATE_str_s[k])
                       elif NDX_PRICE_DATE_str_s[k] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                            #    sell price at QQQM
                            sell_price = NDX_PRICEnum_s[k]/100
                            sell_price_list.append(sell_price)
                            sell_date.append(NDX_PRICE_DATE_str_s[k])
                       else:
                            continue
                  #    enough shares
                  if sell_shares_2 <= account_shares:
                    account_shares = account_shares - sell_shares_2
                    account_money = account_money + sell_shares_2*sell_price
                    #    sell strategy 3 satisfied
             if NDX_PBnum_s[i] > NDX_PB90 and NDX_PEnum_s[i] > NDX_PE90:
                  for k in range(NDX_PRICElen):
                    #    find the corresponding price, using time
                       if i == NDX_PElen-1:
                            if NDX_PRICE_DATE_str_s[k] >= PE_TSs[i]:
                                 #    sell price at QQQM
                                   sell_price = NDX_PRICEnum_s[k]/100
                                   sell_price_list.append(sell_price)
                                   sell_date.append(NDX_PRICE_DATE_str_s[k])
                       elif NDX_PRICE_DATE_str_s[k] >= PE_TSs[i] and NDX_PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                            #    sell price at QQQM
                            sell_price = NDX_PRICEnum_s[k]/100
                            sell_price_list.append(sell_price)
                            sell_date.append(NDX_PRICE_DATE_str_s[k])
                       else:
                            continue
                  #    enough shares
                  if sell_shares_3 <= account_shares:
                    account_shares = account_shares - sell_shares_3
                    account_money = account_money + sell_shares_3*sell_price


        ### SP500 strategy ###
        url_SP500_PE = "https://danjuanfunds.com/djapi/index_eva/pe_history/SP500?day=all"
        url_SP500_PB = "https://danjuanfunds.com/djapi/index_eva/pb_history/SP500?day=all"
        # url_pb = "https://danjuanfunds.com/djapi/index_eva/pb_history/SP500?day=5y"

        ## PE
        r_SP500_PE = requests.get(url_SP500_PE,headers=my_headers)
        SP500_PEstr_s = re.findall('"pe":(.*?),"ts"',r_SP500_PE.text)
        SP500_PEnum_s = [float(x) for x in SP500_PEstr_s]
        SP500_PEsorted_s = sorted(SP500_PEnum_s)
        SP500_PElen = len(SP500_PEsorted_s)
        SP500_PE20 = SP500_PEsorted_s[math.floor(0.2*SP500_PElen)-1]
        SP500_PE30 = SP500_PEsorted_s[math.floor(0.3*SP500_PElen)-1]
        SP500_PE70 = SP500_PEsorted_s[math.ceil(0.7*SP500_PElen)-1]
        SP500_PE80 = SP500_PEsorted_s[math.ceil(0.8*SP500_PElen)-1]
        SP500_PEcurrent = SP500_PEnum_s[SP500_PElen-1]
        ## PB
        r_SP500_PB = requests.get(url_SP500_PB,headers=my_headers)
        SP500_PBstr_s = re.findall('"pb":(.*?),"ts"',r_SP500_PB.text)
        SP500_PBnum_s = [float(x) for x in SP500_PBstr_s]
        SP500_PBsorted_s = sorted(SP500_PBnum_s)
        SP500_PBlen = len(SP500_PBsorted_s)
        SP500_PB20 = SP500_PBsorted_s[math.floor(0.2*SP500_PBlen)-1]
        SP500_PB30 = SP500_PBsorted_s[math.floor(0.3*SP500_PBlen)-1]
        SP500_PB70 = SP500_PBsorted_s[math.ceil(0.7*SP500_PBlen)-1]
        SP500_PB80 = SP500_PBsorted_s[math.ceil(0.8*SP500_PBlen)-1]
        SP500_PBcurrent = SP500_PBnum_s[SP500_PBlen-1]
        if  SP500_PEcurrent > SP500_PE80 and SP500_PBcurrent > SP500_PB80:
             sell_SP500 = 1
        else:
             sell_SP500 = 0
        if SP500_PEcurrent < SP500_PE20 and SP500_PBcurrent < SP500_PB20:
             buy_SP500 = 1
        else:
             buy_SP500 = 0

        time.sleep(2)

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
