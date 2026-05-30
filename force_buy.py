import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

# Note: Indodax market buy via CCXT is tricky. 
# Sometimes it's better to use a limit order slightly above market price to ensure execution.

def execute_trade():
    try:
        balance = indodax.fetch_balance()
        idr = balance['total'].get('IDR', 0)
        
        if idr < 11000:
            print("Saldo IDR mepet.")
            return

        # Ambil Top Gainer dari Scan Rame tadi
        # Kita coba target ONDO/IDR atau SOLAYER/IDR yang lagi panas
        symbol = 'ONDO/IDR' 
        ticker = indodax.fetch_ticker(symbol)
        price = ticker['last']
        
        # Hitung jumlah unit
        spend_idr = idr * 0.98 # Sisakan sedikit buat fee
        amount = spend_idr / price
        
        print(f"🚀 Mencoba BUY {symbol} via LIMIT ORDER (biar pasti eksekusi) di harga Rp {price:,.0f}")
        # Gunakan harga market sekarang untuk Limit Buy
        order = indodax.create_limit_buy_order(symbol, amount, price)
        print("✅ ORDER TERPASANG!")
        print(order)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    execute_trade()
