import ccxt

indodax = ccxt.indodax()
ticker = indodax.fetch_ticker('BTC/IDR')
print(ticker)
