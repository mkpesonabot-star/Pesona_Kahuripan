import ccxt

# Mencoba paksa mapping symbol ke format lama 'btc_idr'
indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def test_raw():
    try:
        # Langsung tembak pake private_post_trade
        # Indodax API: pair, type, price, idr/base_currency_amount
        balance = indodax.fetch_balance()
        idr = int(balance['total'].get('IDR', 0) * 0.9)
        
        symbol = 'btc_idr' # Format raw API Indodax
        print(f"🚀 Mencoba RAW Trade {symbol} dengan {idr} IDR...")
        
        # Method trade: pair, type, price, idr (untuk buy)
        # Kita pakai harga market btc sekarang
        ticker = indodax.fetch_ticker('BTC/IDR')
        price = int(ticker['last'])
        
        params = {
            'pair': symbol,
            'type': 'buy',
            'price': price,
            'idr': idr
        }
        
        response = indodax.private_post_trade(params)
        print("✅ RAW RESPONSE:")
        print(response)
        
    except Exception as e:
        print(f"Error Raw: {e}")

if __name__ == "__main__":
    test_raw()
