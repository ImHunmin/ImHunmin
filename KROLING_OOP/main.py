from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import datetime
import telegram
import sys
import schedule
def kkrroling(site, xxppaath):
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('headless')
    driver = webdriver.Chrome(options=webdriver_options)
    driver.get(site)
    time.sleep(1)
    table = driver.find_element(By.XPATH, xxppaath).text
    return table
def make_nalza(year, month, day):
    nalza =[]
    for i in range(0, len(year)):
        nalza.append(year[i] + month[i] + day[i].strip(","))
    return nalza
def strtodateformat(nalza, format):
    nalza_dateformat = []
    for i in range(0, len(nalza)):
        nalza_dateformat.append(datetime.datetime.strptime(nalza[i], format))
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

    value_ism_fro_202001 = data_sim_sl[102::4]
    year_ism_fro_202001 = data_sim_sl[103::4]
    month_ism_fro_202001 = data_sim_sl[105::4]
    day_ism_fro_202001 = data_sim_sl[104::4]

    value_ism = value_ism_unt_202001+value_ism_fro_202001

    nalza_fro_202001 = make_nalza(year_ism_fro_202001, month_ism_fro_202001, day_ism_fro_202001)
    nalza_unt_202001 = make_nalza(year_ism_unt_202001, month_ism_unt_202001, day_ism_unt_202001)
    nalza_ism = nalza_unt_202001+nalza_fro_202001

    print(value_ism)

    strtodateformat(nalza_ism, nz_format_ism)
#### ISM_PMI DATA Processing end

#### sales comparision year DATA Processing start

    data_sales = kkrroling(url2, xpathh2).split()
    data_sales.reverse()

    value_sales = data_sales[1:-5:7]
    year_sales = data_sales[4:-5:7]
    month_sales = data_sales[6:-5:7]
    day_sales = data_sales[5:-5:7]

    nalza_sales = make_nalza(year_sales, month_sales, day_sales)

    strtodateformat(nalza_sales, nz_format_sales)

#### sales comparision year DATA Processing end

###Message Transfer

    bot.sendMessage(chat_id=telegram_chat_id, text='{}'.format(today_date))
    bot.sendMessage(chat_id=telegram_chat_id, text=
    'pmi지수 : {}'.format(value_ism[-2]))




    # if((value_ism[-1]>value_ism[-2]>value_ism[-3])&(value_sales[-1]>value_sales[-2]>value_sales[-3])):
    #     bot.sendMessage(chat_id = telegram_chat_id, text = 'buy : korean stock // sell : American dollar bond')
    # elif((value_ism[-1]<value_ism[-2]<value_ism[-3])&(value_sales[-1]<value_sales[-2]<value_sales[-3])):
    #     bot.sendMessage(chat_id = telegram_chat_id, text = 'buy : American dollar bond // sell : korean stock')
    # else:
    #     bot.sendMessage(chat_id=telegram_chat_id, text='hold')

schedule.every().days.at("22:33").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
