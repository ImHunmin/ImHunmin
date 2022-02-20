from pykrx import stock

tickers = stock.get_market_ticker_list("20220125")

print(tickers)

kospi = stock.get_market_ticker_list("20190225", market="KOSPI")

print(kospi)

for ticker in tickers:
    name = stock.get_market_ticker_name(ticker)
    print(name)


df = stock.get_market_ohlcv_by_ticker("20201021")
print(df.head(10))


