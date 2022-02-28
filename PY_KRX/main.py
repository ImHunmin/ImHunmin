from pykrx import stock
import time
import pandas as pd
from datetime import datetime
import numpy as np


stock_code = stock.get_market_ticker_list(20210215) # 현재일자 기준 가장 가까운 영업일의 코스피 상장종목 리스트
res = pd.DataFrame()
for ticker in stock_code:
     df = stock.get_market_ohlcv_by_date(fromdate="20170104", todate="20210520", ticker=ticker)
     df = df.assign(종목코드=ticker, 종목명=stock.get_market_ticker_name(ticker))
     res = pd.concat([res, df], axis=0)
     time.sleep(1)
res = res.reset_index()
print(df)
print(df[["종가", "거래량", "종목코드", "종목명"]])
print(df.iloc[:, 3:])

# MV_fiv = make_mv_avg(df.iloc[:, 3].values.tolist(), 5)
# MV_twe = make_mv_avg(df.iloc[:, 3].values.tolist(), 20)
# MV_sit = make_mv_avg(df.iloc[:, 3].values.tolist(), 60)
# MV_hundrtw = make_mv_avg(df.iloc[:, 3].values.tolist(), 120)
# MV_year = make_mv_avg(df.iloc[:, 3].values.tolist(), 240)
# if (MV_fiv[-1] > MV_twe[-1] > MV_sit[-1] > MV_hundrtw[-1] > MV_year[-1]):
#     GOL_K.append(df.iloc[-1:, -1].values.tolist())


