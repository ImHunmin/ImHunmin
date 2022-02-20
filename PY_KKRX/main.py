from pykrx import stock
import time
import pandas as pd
# import sqlite3
from datetime import datetime
import numpy as np
#############MAKE DATE LIST
def date_range(start, end):
    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    dates = [date.strftime("%Y%m%d") for date in pd.date_range(start, periods=(end-start).days+1)]
    return dates
# da_te = date_range("20180101", "20181231")
############ M D L END // MAking mv_avg
def make_mv_avg(list, w):
    x = np.array(list, dtype=float)
    mv_avg = np.convolve(x, np.ones(w), 'valid') / w
    return mv_avg
####################

# print(da_te)
# print(len(da_te))

# conn = sqlite3.connect("test.db", isolation_level=None)
# # 커서 획득
# c = conn.cursor()
# # 테이블 생성
# c.execute("CREATE TABLE DA_TE \
#     (id integer, name text, price integer, volume integer)")
#
# c.executemany(
#     'INSERT INTO DA_TE VALUES( ?,?,?,?)',
#
#
# )




# stock_code = stock.get_market_ticker_list(20210215) # 현재일자 기준 가장 가까운 영업일의 코스피 상장종목 리스트
# res = pd.DataFrame()
# for ticker in stock_code:
#      df = stock.get_market_ohlcv_by_date(fromdate="20170104", todate="20210520", ticker=ticker)
#      df = df.assign(종목코드=ticker, 종목명=stock.get_market_ticker_name(ticker))
#      res = pd.concat([res, df], axis=0)
#      time.sleep(1)
#  res = res.reset_index()
#  print(df)
#  print(df[["종가", "거래량", "종목코드", "종목명"]])
# print(df.iloc[:, 3:])


stock_code = stock.get_market_ticker_list(20210215) # 현재일자 기준 가장 가까운 영업일의 코스피 상장종목 리스트
for ticker in stock_code[:5]:
     df = stock.get_market_ohlcv_by_date(fromdate="20170104", todate="20210520", ticker=ticker)
     df = df.assign(종목코드=ticker, 종목명=stock.get_market_ticker_name(ticker))
     MV_fiv = make_mv_avg(df.iloc[:, 3].values.tolist(), 5)
     # MV_twe = make_mv_avg(df[["종가"]], 20)
     # MV_sit = make_mv_avg(df[["종가"]], 60)
     # MV_hundrtw = make_mv_avg(df[["종가"]], 120)
     # MV_year = make_mv_avg(df[["종가"]], 240)
     time.sleep(1)

print(df)
print(df[["종가", "거래량", "종목코드", "종목명"]])
print(type(df.iloc[:, 3].values.tolist()))







# for ticker in stock_code[:5]:
#     df = stock.get_market_ohlcv()
#     df = df.assign(종목코드=ticker, 종목명=stock.get_market_ticker_name(ticker))
#
# print(df)