from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import datetime
import telegram
import numpy as np
import pandas as pd
import sys
import schedule
import os
from pykrx import stock
import time
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np

def kkrroling(site, xxppaath):
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')
    driver = webdriver.Chrome(options=webdriver_options)
    driver.get(site)
    time.sleep(1)
    table = driver.find_element(By.XPATH, xxppaath).text
    return table
def Strtofloat(list):
    list_float = []
    for i in range(0, len(list)):
        list_float.append(list[i].strip("%"))
    return list_float
def make_nalza(year, month, day):
    nalza =[]
    for i in range(0, len(year)):
        nalza.append(year[i] + month[i] + day[i].strip(","))
    return nalza
def strtodateformat(nalza, format):
    nalza_dateformat = []
    for i in range(0, len(nalza)):
        nalza_dateformat.append(datetime.datetime.strptime(nalza[i], format))
    return nalza_dateformat

def make_mv_avg(list, w):
    x = np.array(list, dtype=float)
    mv_avg = np.convolve(x, np.ones(w), 'valid') / w
    return mv_avg
def job():
    url1 = 'https://ycharts.com/indicators/us_pmi'
    xpathh1 = "/html/body/main/div/div[4]/div/div/div/div/div[1]/div[2]"
    nz_format_ism = '%Y%B%d'

    url2 = 'https://investing.com/economic-calendar/retail-sales-1878'
    xpathh2 = "//*[@id='eventHistoryTable1878']"
    nz_format_sales = '%Y%b%d'

    api_key = '5165191702:AAHfSlZy8SnvYBq58VWcfME7GgcENcVgCzM'
    bot = telegram.Bot(token=api_key)
    telegram_chat_id = '1786134332'

    today_date = (datetime.datetime.now().date()).strftime("%Y-%m-%d")

    #### ISM_PMI DATA Processing start
    data_ism = kkrroling(url1, xpathh1).split()
    data_sim_sl = data_ism[13::]
    data_sim_sl.reverse()

    value_ism_unt_202001 = data_sim_sl[0:100:4]
    year_ism_unt_202001 = data_sim_sl[1:100:4]
    month_ism_unt_202001 = data_sim_sl[3:100:4]
    day_ism_unt_202001 = data_sim_sl[2:100:4]

    value_ism_fro_202001 = data_sim_sl[102:-1:4]
    year_ism_fro_202001 = data_sim_sl[103::4]
    month_ism_fro_202001 = data_sim_sl[105::4]
    day_ism_fro_202001 = data_sim_sl[104::4]

    value_ism = value_ism_unt_202001 + value_ism_fro_202001
    nalza_fro_202001 = make_nalza(year_ism_fro_202001, month_ism_fro_202001, day_ism_fro_202001)
    nalza_unt_202001 = make_nalza(year_ism_unt_202001, month_ism_unt_202001, day_ism_unt_202001)
    nalza_ism = nalza_unt_202001 + nalza_fro_202001

    nalza_ism_dateformat = strtodateformat(nalza_ism, nz_format_ism)
    #### ISM_PMI DATA Processing end

    #### sales comparision year DATA Processing start

    data_sales = kkrroling(url2, xpathh2).split()
    data_sales.reverse()

    value_sales = Strtofloat(data_sales[1:-11:7])

    year_sales = data_sales[4:-11:7]
    month_sales = data_sales[6:-11:7]
    day_sales = data_sales[5:-11:7]

    nalza_sales = make_nalza(year_sales, month_sales, day_sales)
    nalza_sales_dateformat = strtodateformat(nalza_sales, nz_format_sales)

    # value_sales_mv_avg = make_mv_avg(value_sales, 5)
    # value_ism_mv_avg = make_mv_avg(value_ism, 5)

    ######################end

    ###Message Transfer
    def trnsfort():
        bot.sendMessage(chat_id=telegram_chat_id, text='{} 기준'.format(today_date))
        bot.sendMessage(chat_id=telegram_chat_id, text='pmi지수({}) : {} pmi지수({}) : {} pmi지수({}) : {}'
                        .format(nalza_ism_dateformat[-1].date().strftime("%Y-%m-%d"), value_ism[-1],
                                nalza_ism_dateformat[-2].date().strftime("%Y-%m-%d"), value_ism[-2],
                                nalza_ism_dateformat[-3].date().strftime("%Y-%m-%d"), value_ism[-3]))
        bot.sendMessage(chat_id=telegram_chat_id, text='sale지수({}) : {}  sale지수({}) : {} sale지수({}) : {}'
                        .format(nalza_sales_dateformat[-1].date().strftime("%Y-%m-%d"), value_sales[-1],
                                nalza_sales_dateformat[-2].date().strftime("%Y-%m-%d"), value_sales[-2],
                                nalza_sales_dateformat[-3].date().strftime("%Y-%m-%d"), value_sales[-3]))

        if ((value_ism[-1] > value_ism[-2] > value_ism[-3]) & (value_sales[-1] > value_sales[-2] > value_sales[-3])):
            bot.sendMessage(chat_id=telegram_chat_id, text='buy : korean stock // sell : American dollar bond')
        elif ((value_ism[-1] < value_ism[-2] < value_ism[-3]) & (value_sales[-1] < value_sales[-2] < value_sales[-3])):
            bot.sendMessage(chat_id=telegram_chat_id, text='buy : American dollar bond // sell : korean stock')
        else:
            bot.sendMessage(chat_id=telegram_chat_id, text='hold')

    trnsfort()

#############MAKE DATE LIST
def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [date.strftime("%Y%m%d") for date in pd.date_range(start, periods=(end - start).days + 1)]
    return dates

def make_mv_avg(list, w):
    x = np.array(list, dtype=float)
    mv_avg = np.convolve(x, np.ones(w), 'valid') / w
    return mv_avg


##################
TodaY_Str = datetime.now().date().strftime("%Y%m%d")


def howlong(day):
    today = datetime.now().date()
    howlongdayago = today - timedelta(days=day)
    return howlongdayago.strftime("%Y%m%d")


# print(df[["종가", "거래량", "종목코드", "종목명"]])
# print(df.iloc[1:, 3:])
def price_straight_array(da_te, MMarket):
    GOL_K = []
    stock_code = stock.get_market_ticker_list(TodaY_Str, market=MMarket)  # 현재일자 기준 가장 가까운 영업일의 코스피 상장종목 리스트
    for ticker in stock_code[:50]:
        df = stock.get_market_ohlcv_by_date(fromdate="20190104", todate=da_te, ticker=ticker)
        df = df.assign(종목코드=ticker, 종목명=stock.get_market_ticker_name(ticker))

        MV_fiv = make_mv_avg(df.iloc[:, 3].values.tolist(), 5)
        MV_ten = make_mv_avg(df.iloc[:, 3].values.tolist(), 10)
        MV_twe = make_mv_avg(df.iloc[:, 3].values.tolist(), 20)
        MV_sixt = make_mv_avg(df.iloc[:, 3].values.tolist(), 60)
        MV_bungi = make_mv_avg(df.iloc[:, 3].values.tolist(), 120)
        if (MV_fiv[-1] > MV_ten[-1] > MV_twe[-1] > MV_sixt[-1] > MV_bungi[-1]):
            GOL_K.append(df.iloc[-1:, -2].to_string())

        for i in range(0, len(GOL_K)):
            GOL_K[i] = GOL_K[i][-6:]

    time.sleep(1)
    return GOL_K


def Shaking_Volume(da_te, MMarket):
    GOL_K = []
    stock_code = stock.get_market_ticker_list(TodaY_Str, market=MMarket)  # 현재일자 기준 가장 가까운 영업일의 코스피 상장종목 리스트
    for ticker in stock_code:
        df = stock.get_market_ohlcv_by_date(fromdate="20180104", todate=da_te, ticker=ticker)
        df = df.assign(종목코드=ticker, 종목명=stock.get_market_ticker_name(ticker))

        MV_fiv = make_mv_avg(df.iloc[:, 3].values.tolist(), 5)
        MV_ten = make_mv_avg(df.iloc[:, 3].values.tolist(), 10)
        MV_twe = make_mv_avg(df.iloc[:, 3].values.tolist(), 20)
        MV_sixt = make_mv_avg(df.iloc[:, 3].values.tolist(), 60)
        MV_bungi = make_mv_avg(df.iloc[:, 3].values.tolist(), 120)

        if (len(MV_bungi) > 800):
            cout = 0
            for i in range(0, 600):
                if (MV_bungi[-603 + i] > MV_fiv[-603 + i]):
                    cout = cout + 1
            if (cout > 400) & (MV_bungi[-1] < MV_fiv[-1]) & (MV_bungi[-2] > MV_fiv[-2]):
                GOL_K.append(df.iloc[-1:, -2].to_string())
        for i in range(0, len(GOL_K)):
            GOL_K[i] = GOL_K[i][-6:]
    return GOL_K


def TR_VO_straight_array(da_te, MMarket):
    VO = []
    stock_code = stock.get_market_ticker_list(TodaY_Str, market=MMarket)  # 현재일자 기준 가장 가까운 영업일의 코스피 상장종목 리스트
    res = pd.DataFrame()
    for ticker in stock_code:
        df = stock.get_market_ohlcv_by_date(fromdate="20170104", todate=da_te, ticker=ticker)
        df = df.assign(종목코드=ticker, 종목명=stock.get_market_ticker_name(ticker))
        print(stock.get_market_ticker_name(ticker))
        print(df.iloc[:, 4].values.tolist()[-10:-1])
        time.sleep(2)


def num_to_name(list):
    GOL_K_NAME = []
    for ticker in list:
        GOL_K_NAME.append(stock.get_market_ticker_name(ticker))
    return GOL_K_NAME


def strtoint(lissst):
    intt_list = []
    for i in range(0, len(lissst)):
        intt_list.append(int(lissst[i]))
    return intt_list


def PPoPP(List_Today, List_dayago):
    New_List_GK = []

    for i in range(0, len(List_Today)):
        cnt = 0
        for k in range(0, len(List_dayago)):
            if List_Today[i] != List_dayago[k]:
                cnt = cnt + 1
        if cnt == len(List_dayago):
            New_List_GK.append(List_Today[i])
    return New_List_GK


A = num_to_name(Shaking_Volume(TodaY_Str, "ALL"))

for i in range(0, len(A)):
    print(A[i])
    print("https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={}".format(A[i]))










schedule.every().day.at("22:30").do(job())
while True:
    schedule.run_pending()
    time.sleep(1)
