import math,time
def strategy2(PEnum_s,stock_code,PRICEnum_s,PRICE_DATE_str_s,PE_buy_thresh1,PE_buy_thresh2,PE_buy_thresh3,\
              PE_sell_thresh1,PE_sell_thresh2,PE_sell_thresh3,\
               account_money,account_shares,buy_shares_1,buy_shares_2,buy_shares_3,sell_shares_1,sell_shares_2,sell_shares_3,index2fund_ratio,start_yr,trace_wks):
     print("initial account shares: ",account_shares,"\ninitial account money: ",account_money)
     # PE
     PElen_total = len(PEnum_s)
     PEcurrent = PEnum_s[PElen_total-1]
     # PE timing
    #  PE_TSs = [timeStamp(x) for x in PE_TSnum_s]
     ## PRICE
     PRICElen = len(PRICEnum_s)
     PRICEcurrent = PRICEnum_s[-1]
     start_idx = start_yr*52
     long_hold_shares = math.floor(account_money/PRICEnum_s[start_idx]*index2fund_ratio)
     long_hold_value =  long_hold_shares * PRICEcurrent/index2fund_ratio
     start_eval_date = PRICE_DATE_str_s[start_idx]
     start_eval_price = PRICEnum_s[start_idx]
     print(stock_code+" evaluation start date: ",start_eval_date,"\n"+stock_code+" start price:",start_eval_price)
     print(stock_code+" shares if buy from start: ",long_hold_shares,"\n"+stock_code+" value if buy from start:",long_hold_value)
     buy_price_list = []
     buy_date_list = []
     sell_date_list = []
     sell_price_list = []
     actual_buy_price_list = []
     actual_buy_date_list = []
     actual_sell_date_list = []
     actual_sell_price_list = []
     
     if start_idx<trace_wks:
          raise TraceTimeError('tracing too many weeks, no data available')
     # eval_start = math.ceil(PElen_total/2) # start the evaluation from the 6th yr, using the first 5 yrs as index
     for i in range(start_idx,PElen_total):
          # PE
          PEsorted_s = sorted(PEnum_s[i-trace_wks:i])
          PElen = len(PEsorted_s)
          PE10 = PEsorted_s[math.floor(PE_buy_thresh3*PElen)-1]
          PE20 = PEsorted_s[math.floor(PE_buy_thresh2*PElen)-1]
          PE30 = PEsorted_s[math.floor(PE_buy_thresh1*PElen)-1]
          PE70 = PEsorted_s[math.ceil(PE_sell_thresh1*PElen)-1]
          PE80 = PEsorted_s[math.ceil(PE_sell_thresh2*PElen)-1]
          PE90 = PEsorted_s[math.ceil(PE_sell_thresh3*PElen)-1]
          #    buy strategy 1 satisfied
          if PEnum_s[i] < PE30:
            #    for j in range(PRICElen):
            #    #    find the corresponding price, using time
            #         if i == PElen-1:
            #              if PRICE_DATE_str_s[j] >= PE_TSs[i]:
                              #    buy price at QQQM
            buy_price = PRICEnum_s[i]/index2fund_ratio
            buy_price_list.append(buy_price)
            buy_date = PRICE_DATE_str_s[i]
            buy_date_list.append(buy_date)
                    # elif PRICE_DATE_str_s[j] >= PE_TSs[i] and PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                    #      #    buy price at QQQM
                    #      buy_price = PRICEnum_s[j]/index2fund_ratio
                    #      buy_price_list.append(buy_price)
                    #      buy_date = PRICE_DATE_str_s[j]
                    #      buy_date_list.append(buy_date)
                    # else:
                    #      continue
               #    enough money
            if account_money >= buy_shares_1*buy_price and buy_shares_1>0:
                account_shares = account_shares + buy_shares_1
                account_money = account_money - buy_shares_1*buy_price
                actual_buy_price_list.append(buy_price)
                actual_buy_date_list.append(buy_date)
          #    buy strategy 2 satisfied
          if PEnum_s[i] < PE20:
            #    for j in range(PRICElen):
            #    #    find the corresponding price, using time
            #         if i == PElen-1:
            #              if PRICE_DATE_str_s[j] >= PE_TSs[i]:
                              #    buy price at QQQM
            buy_price = PRICEnum_s[i]/index2fund_ratio
            buy_price_list.append(buy_price)
            buy_date = PRICE_DATE_str_s[i]
            buy_date_list.append(buy_date)
                    # elif PRICE_DATE_str_s[j] >= PE_TSs[i] and PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                    #      #    buy price at QQQM
                    #      buy_price = PRICEnum_s[j]/index2fund_ratio
                    #      buy_price_list.append(buy_price)
                    #      buy_date = PRICE_DATE_str_s[j]
                    #      buy_date_list.append(buy_date)
                    # else:
                    #      continue
               #    enough money
            if account_money >= buy_shares_2*buy_price and buy_shares_2>0:
                account_shares = account_shares + buy_shares_2
                account_money = account_money - buy_shares_2*buy_price
                actual_buy_price_list.append(buy_price)
                actual_buy_date_list.append(buy_date)
          #    buy strategy 3 satisfied
          if  PEnum_s[i] < PE10:
            #    for j in range(PRICElen):
            #    #    find the corresponding price, using time
            #         if i == PElen-1:
            #              if PRICE_DATE_str_s[j] >= PE_TSs[i]:
                              #    buy price at QQQM
            buy_price = PRICEnum_s[i]/index2fund_ratio
            buy_price_list.append(buy_price)
            buy_date = PRICE_DATE_str_s[i]
            buy_date_list.append(buy_date)
                    # elif PRICE_DATE_str_s[j] >= PE_TSs[i] and PRICE_DATE_str_s[j] < PE_TSs[i+1]:
                    #      #    buy price at QQQM
                    #      buy_price = PRICEnum_s[j]/index2fund_ratio
                    #      buy_price_list.append(buy_price)
                    #      buy_date = PRICE_DATE_str_s[j]
                    #      buy_date_list.append(buy_date)
                    # else:
                    #      continue
               #    enough money
            if account_money >= buy_shares_3*buy_price and buy_shares_3>0:
                account_shares = account_shares + buy_shares_3
                account_money = account_money - buy_shares_3*buy_price
                actual_buy_price_list.append(buy_price)
                actual_buy_date_list.append(buy_date)

          #    sell strategy 1 satisfied
          if  PEnum_s[i] > PE70:
            #    for k in range(PRICElen):
            #    #    find the corresponding price, using time
            #         if i == PElen-1:
                        #  if PRICE_DATE_str_s[k] >= PE_TSs[i]:
                              #    sell price at QQQM
            sell_price = PRICEnum_s[i]/index2fund_ratio
            sell_price_list.append(sell_price)
            sell_date = PRICE_DATE_str_s[i]
            sell_date_list.append(sell_date)
                    # elif PRICE_DATE_str_s[k] >= PE_TSs[i] and PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                    #      #    sell price at QQQM
                    #      sell_price = PRICEnum_s[k]/index2fund_ratio
                    #      sell_price_list.append(sell_price)
                    #      sell_date = PRICE_DATE_str_s[k]
                    #      sell_date_list.append(sell_date)
                    # else:
                    #      continue
               #    enough shares
            if sell_shares_1 <= account_shares and sell_shares_1 > 0:
                account_shares = account_shares - sell_shares_1
                account_money = account_money + sell_shares_1*sell_price
                actual_sell_price_list.append(sell_price)
                actual_sell_date_list.append(sell_date)
                    
               #    sell strategy 2 satisfied
          if  PEnum_s[i] > PE80:
            #    for k in range(PRICElen):
            #    #    find the corresponding price, using time
            #         if i == PElen-1:
            #              if PRICE_DATE_str_s[k] >= PE_TSs[i]:
                              #    sell price at QQQM
            sell_price = PRICEnum_s[i]/index2fund_ratio
            sell_price_list.append(sell_price)
            sell_date = PRICE_DATE_str_s[i]
            sell_date_list.append(sell_date)
                    # elif PRICE_DATE_str_s[k] >= PE_TSs[i] and PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                    #      #    sell price at QQQM
                    #      sell_price = PRICEnum_s[k]/index2fund_ratio
                    #      sell_price_list.append(sell_price)
                    #      sell_date = PRICE_DATE_str_s[k]
                    #      sell_date_list.append(sell_date)
                    # else:
                    #      continue
               #    enough shares
            if sell_shares_2 <= account_shares and sell_shares_2 > 0:
                account_shares = account_shares - sell_shares_2
                account_money = account_money + sell_shares_2*sell_price
                actual_sell_price_list.append(sell_price)
                actual_sell_date_list.append(sell_date)
               #    sell strategy 3 satisfied
          if  PEnum_s[i] > PE90:
            #    for k in range(PRICElen):
            #    #    find the corresponding price, using time
            #         if i == PElen-1:
            #              if PRICE_DATE_str_s[k] >= PE_TSs[i]:
                              #    sell price at QQQM
            sell_price = PRICEnum_s[i]/index2fund_ratio
            sell_price_list.append(sell_price)
            sell_date = PRICE_DATE_str_s[i]
            sell_date_list.append(sell_date)
                    # elif PRICE_DATE_str_s[k] >= PE_TSs[i] and PRICE_DATE_str_s[k] < PE_TSs[i+1]:
                    #      #    sell price at QQQM
                    #      sell_price = PRICEnum_s[k]/index2fund_ratio
                    #      sell_price_list.append(sell_price)
                    #      sell_date = PRICE_DATE_str_s[k]
                    #      sell_date_list.append(sell_date)
                    # else:
                    #      continue
               #    enough shares
            if sell_shares_3 <= account_shares and sell_shares_3 > 0:
                account_shares = account_shares - sell_shares_3
                account_money = account_money + sell_shares_3*sell_price
                actual_sell_price_list.append(sell_price)
                actual_sell_date_list.append(sell_date)
     print("final "+stock_code+" account shares: ",account_shares,"\nfinal "+stock_code+" account money: ",account_money,"\nfinal "+stock_code+" shares and money combined: ",account_money+account_shares*PRICEcurrent/index2fund_ratio)
     return account_shares,account_money,PRICEcurrent,long_hold_shares,long_hold_value,buy_price_list,sell_price_list,buy_date_list,sell_date_list,\
          actual_buy_price_list,actual_buy_date_list,actual_sell_price_list,actual_sell_date_list