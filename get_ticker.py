import alpha_api,requests,json
api_key = alpha_api.api_key
my_headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
stock_code = ['LVMHF','META']
file_names = ['_adjusted_w','_EPS','_RSI']
for i_code in stock_code:
    j_number = 0
    url_ticker_w = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol='+i_code+'&apikey='+api_key
    url_EPS = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='+i_code+'&apikey='+api_key
    url_RSI = 'https://www.alphavantage.co/query?function=RSI&symbol='+i_code+'&interval=daily&time_period=14&series_type=close&apikey='+api_key
    urls = [url_ticker_w,url_EPS,url_RSI]
    for j_url in urls:
        # url_NDX_PE = "https://danjuanfunds.com/djapi/index_eva/pe_history/NDX?day=all"
        # r = requests.get(url_NDX_PE,headers=my_headers)
        r = requests.get(j_url)
        data = r.json()
        js_data = json.dumps(data,indent=4)
        file_name = 'logs_alpha/23-12-30/'+ i_code + file_names[j_number]+'.json'
        with open(file_name, "w") as file:
            file.write(js_data)
        j_number = j_number + 1

# # for test
# url_NDX_PE = "https://danjuanfunds.com/djapi/index_eva/pe_history/NDX?day=all"
# r = requests.get(url_NDX_PE,headers=my_headers)
# result_json = r.json()
# with open('output.json', 'w') as file:
#     json.dump(result_json, file,indent=4)