import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import matplotlib.pyplot as plt
import datetime
import telegram
import sys
import schedule


def job():
    api_key = '5165191702:AAHfSlZy8SnvYBq58VWcfME7GgcENcVgCzM'
    bot = telegram.Bot(token=api_key)
    telegram_chat_id = '1786134332'
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')

    driver = webdriver.Chrome(options=webdriver_options)
    url1 = 'https://ycharts.com/indicators/us_pmi'
    driver.get(url1)
    time.sleep(1)
    table = driver.find_element(By.CLASS_NAME, 'col-md-8').text

    data_ism = table.split()


    driver2 = webdriver.Chrome(options=webdriver_options)
    url2 = 'https://investing.com/economic-calendar/retail-sales-1878'
    driver2.get(url2)
    time.sleep(1)
    table_sales = driver2.find_element(By.XPATH, "//*[@id='eventHistoryTable1878']").text
    data_sales = table_sales.split()

    data_sl = data_ism[243:]
    value_until_202001 = data_sl[5:104:4]
    value_from_202001 = data_sl[107::4]
    value = value_until_202001 + value_from_202001
    value.reverse()
    n_m_unt20_01 = data_sl[2:102:4]
    n_d_unt20_01 = data_sl[3:102:4]
    n_y_unt20_01 = data_sl[4:102:4]
    nz_unt20_01 = []
    for i in range(0, len(n_d_unt20_01)):
        nz_unt20_01.append(n_y_unt20_01[i] + n_m_unt20_01[i] + n_d_unt20_01[i].strip(","))

    n_m_fr_20_01 = data_sl[104::4]
    n_d_fr_20_01 = data_sl[105::4]
    n_y_fr_20_01 = data_sl[106::4]
    nz_fr_20_01 = []
    for i in range(0, len(n_d_fr_20_01)):
        nz_fr_20_01.append(n_y_fr_20_01[i] + n_m_fr_20_01[i] + n_d_fr_20_01[i].strip(","))

    nz_pmi = nz_unt20_01+nz_fr_20_01
    nz_pmi.reverse()
    pmi_value_float = []

    for i in range(0, len(value)):
        pmi_value_float.append(float(value[i]))
    pmi_nz_dateformat =[]
    for i in range(0, len(nz_pmi)):
        pmi_nz_dateformat.append(datetime.datetime.strptime(nz_pmi[i], '%Y%B%d'))

    d_r_y_value=data_sales[-2:-36:-7]
    n_r_y_year = data_sales[-5:-40:-7]
    n_r_y_month = data_sales[-7:-40:-7]
    n_r_y_day = data_sales[-6:-37:-7]
    n_r_y_date = []

    for i in range(0, len(n_r_y_year)):
        n_r_y_date.append(n_r_y_year[i]+n_r_y_month[i]+n_r_y_day[i].strip(","))

    n_r_y_dateformat =[]
    d_r_y_float_value =[]

    for i in range(0, len(n_r_y_date)):
        n_r_y_dateformat.append(datetime.datetime.strptime(n_r_y_date[i], '%Y%b%d'))

    for i in range(0, len(d_r_y_value)):
        d_r_y_float_value.append(float(d_r_y_value[i].strip("%")))

    today_date = (datetime.datetime.now().date()).strftime("%Y-%m-%d")

    bot.sendMessage(chat_id = telegram_chat_id, text = '{}'.format(today_date))
    if((pmi_value_float[-1]>pmi_value_float[-2]>pmi_value_float[-3])&(d_r_y_float_value[-1]>d_r_y_float_value[-2]>d_r_y_float_value[-3])):
        bot.sendMessage(chat_id = telegram_chat_id, text = 'buy : korean stock // sell : American dollar bond')
    elif((pmi_value_float[-1]<pmi_value_float[-2]<pmi_value_float[-3])&(d_r_y_float_value[-1]<d_r_y_float_value[-2]<d_r_y_float_value[-3])):
        bot.sendMessage(chat_id = telegram_chat_id, text = 'buy : American dollar bond // sell : korean stock')
    else:
        bot.sendMessage(chat_id=telegram_chat_id, text='hold')



schedule.every().days.at("08:40").do(job) #매일 8시40분에 실행

while True:
    schedule.run_pending()
    time.sleep(1)

# sys.exit()