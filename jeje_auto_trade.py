import ccxt
import time

# Konfigurasi Jeje Bot
indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def get_momentum_signals():
    tickers = indodax.fetch_tickers()
    signals = []
    for symbol, ticker in tickers.items():
        if '/IDR' in symbol and ticker.get('quoteVolume', 0) > 2000000000:
            ohlcv = indodax.fetch_ohlcv(symbol, timeframe='1h', limit=2)
            if len(ohlcv) >= 2:
                change = (ohlcv[1][4] - ohlcv[0][1]) / ohlcv[0][1] * 100
                if change > 1.0: # Momentum naik > 1% dlm 1 jam
                    signals.append({
                        'symbol': symbol,
                        'raw_id': symbol.lower().replace('/', '_'),
                        'price': ticker['last'],
                        'change': change
                    })
    signals.sort(key=lambda x: x['change'], reverse=True)
    return signals

def execute_auto_trade():
    try:
        # 1. Cek Saldo
        balance = indodax.fetch_balance()
        idr = balance['total'].get('IDR', 0)
        
        if idr < 11000:
            print(f"Saldo IDR Rp {idr:,.0f} (Running/Empty).")
            return

        # 2. Cari Sinyal
        print("Jeje lagi nyari koin MICIN yang 'panas' (Exclude BTC/ETH)...")
        all_signals = get_momentum_signals()
        
        # Filter: Jangan BTC atau ETH
        signals = [s for s in all_signals if s['symbol'] not in ['BTC/IDR', 'ETH/IDR']]
        
        if not signals:
            print("Belum ada koin yang meledak volumenya.")
            return

        target = signals[0]
        print(f"🔥 Sinyal Ditemukan: {target['symbol']} (+{target['change']:.2f}%)")

        # 3. Eksekusi BUY (Pakai Raw API karena CCXT mapping error)
        # Main tipis-tipis: Gunakan maksimal 50% saldo IDR per transaksi kalau saldo cukup gede, 
        # tapi karena saldo sekarang pas-pasan (10k-30k), kita pakai 90% dulu biar bisa beli.
        percent_to_use = 0.90 if idr < 50000 else 0.50
        spend_idr = int(idr * percent_to_use)
        
        params = {
            'pair': target['raw_id'],
            'type': 'buy',
            'price': int(target['price']),
            'idr': spend_idr
        }
        
        print(f"🚀 Mengeksekusi BUY {target['symbol']} senilai Rp {spend_idr:,.0f}...")
        response = indodax.private_post_trade(params)
        
        if response.get('success') == '1' or response.get('success') == 1:
            print(f"✅ BERHASIL BELI {target['symbol']}!")
            print(f"Order ID: {response['return'].get('order_id')}")
        else:
            print(f"Gagal eksekusi: {response.get('error')}")

    except Exception as e:
        print(f"Error Jeje Bot: {e}")

if __name__ == "__main__":
    execute_auto_trade()
