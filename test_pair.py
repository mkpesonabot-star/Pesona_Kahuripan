import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def test_fixed_pair():
    try:
        # Kita coba format 'btc_idr' (pake underscore) yang biasanya standar Indodax
        symbol = 'aura_idr' 
        balance = indodax.fetch_balance()
        idr = int(balance['total'].get('IDR', 0) * 0.9)
        ticker = indodax.fetch_ticker('AURA/IDR')
        price = int(ticker['last'])
        
        params = {'pair': symbol, 'type': 'buy', 'price': price, 'idr': idr}
        print(f"🚀 Mencoba BUY {symbol}...")
        res = indodax.privatePostTrade(params)
        print("Res:", res)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_fixed_pair()
