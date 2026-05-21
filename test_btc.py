import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def try_btc():
    try:
        symbol = 'BTC/IDR'
        ticker = indodax.fetch_ticker(symbol)
        price = ticker['last']
        balance = indodax.fetch_balance()
        idr = balance['total'].get('IDR', 0)
        
        amount = (idr * 0.9) / price
        print(f"🚀 Test BUY {symbol} @ {price}")
        order = indodax.create_limit_buy_order(symbol, amount, price)
        print("✅ SUCCESS!")
        print(order)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try_btc()
