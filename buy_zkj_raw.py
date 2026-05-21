import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

symbol = 'ZKJ/IDR' 
modal = 11000

try:
    ticker = indodax.fetch_ticker(symbol)
    harga_beli = ticker['ask']
    jumlah_koin = round(modal / harga_beli, 0) # CCXT mungkin butuh bilangan bulat untuk lot jika koin murah

    print(f"Mencoba beli {symbol} dengan limit order (custom parameter idr)...")
    
    # API Indodax aslinya kalau IDR pakai parameter idr untuk jumlah rupiah
    # CCXT mungkin gagal parsing "amount" jika tidak pas.
    # Kita coba format ZKJ_IDR
    
    market_id = 'zkj_idr'
    
    response = indodax.privatePostTrade({
        'pair': market_id,
        'type': 'buy',
        'price': harga_beli,
        'idr': modal
    })
    
    print("\n✅ Order POST Trade Indodax BERHASIL!")
    print(response)
    
except Exception as e:
    print(f"❌ Gagal: {e}")
