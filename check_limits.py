import ccxt
indodax = ccxt.indodax()
indodax.load_markets()
for sym in ['ZKJ/IDR', 'BTC/IDR']:
    market = indodax.markets.get(sym)
    if market:
        print(f"{sym} Limits: {market['limits']}")
