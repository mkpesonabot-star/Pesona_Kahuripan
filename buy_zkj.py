import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

symbol = 'ZKJ/IDR'
modal = 11000 # 11 ribu IDR 

try:
    ticker = indodax.fetch_ticker(symbol)
    harga_beli = ticker['ask'] # beli limit di harga ask agar instan
    jumlah_koin = modal / harga_beli

    print(f"Mencoba beli {symbol} dengan limit order...")
    print(f"Harga limit: Rp {harga_beli}")
    print(f"Jumlah koin: {jumlah_koin:.8f}")

    order = indodax.create_limit_buy_order(symbol, jumlah_koin, harga_beli)
    print("\n✅ Order BERHASIL!")
    
except Exception as e:
    print(f"❌ Gagal: {e}")
