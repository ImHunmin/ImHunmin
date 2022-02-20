import tradingeconomics as te

k = te.getIndicatorData(output_type='df')

print(k)