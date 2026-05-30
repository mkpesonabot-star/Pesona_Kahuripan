import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def sell_instant():
    try:
        # Kita pasang harga sell agak rendah biar langsung dimakan (Instant Sell)
        ticker = indodax.fetch_ticker('BTC/IDR')
        market_price = int(ticker['last'])
        sell_price = int(market_price * 0.99) # Turunin 1% biar instant
        
        balance = indodax.fetch_balance()
        btc = balance['total'].get('BTC', 0)
        
        if btc > 0:
            params = {
                'pair': 'btc_idr',
                'type': 'sell',
                'price': sell_price,
                'btc': f"{btc:.8f}"
            }
            print(f"🚀 INSTANT SELL {btc:.8f} BTC @ Rp {sell_price:,.0f}...")
            res = indodax.privatePostTrade(params)
            print("Res:", res)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sell_instant()
