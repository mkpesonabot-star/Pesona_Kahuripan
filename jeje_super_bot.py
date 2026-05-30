import ccxt
import time

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def aggressive_hunt():
    try:
        balance = indodax.fetch_balance()
        idr = balance['total'].get('IDR', 0)
        
        # Bersihkan sisa-sisa koin kecil yang gak bisa ditrade (Dust)
        # Fokus ke koin yang nilainya > 10rb agar bisa dieksekusi jual
        for coin, amount in balance['total'].items():
            if coin != 'IDR' and amount > 0:
                symbol = f"{coin}/IDR"
                try:
                    ticker = indodax.fetch_ticker(symbol)
                    value = amount * ticker['last']
                    if value >= 10000:
                        # Ini koin yang layak pantau profit
                        pass
                    else:
                        # Dust/Sisa micin, biarkan saja dulu
                        pass
                except: continue

        if idr < 11000:
            print("Saldo IDR belum cukup untuk open posisi baru.")
            return

        # Cari Koin Paling Ganas (Sesuai screenshot: LOOKS, PAYAI, dll)
        tickers = indodax.fetch_tickers()
        candidates = []
        for s, t in tickers.items():
            if '/IDR' in s and s not in ['BTC/IDR', 'ETH/IDR', 'USDT/IDR']:
                vol = t.get('quoteVolume', 0)
                if vol > 3000000000: # Volume > 3 Miliar
                    ohlcv = indodax.fetch_ohlcv(s, timeframe='1h', limit=2)
                    if len(ohlcv) >= 2:
                        change = (ohlcv[1][4] - ohlcv[0][1]) / ohlcv[0][1] * 100
                        if change > 1.0:
                            candidates.append({
                                'symbol': s,
                                'raw_id': s.lower().replace('/', '_'),
                                'price': t['last'],
                                'change': change
                            })
        
        candidates.sort(key=lambda x: x['change'], reverse=True)
        
        if candidates:
            # All-in ke 1-2 koin terbaik agar nilai transaksi > 10rb
            target = candidates[0]
            spend = int(idr * 0.95) # Gunakan hampir semua saldo sisa
            
            print(f"🚀 AGGRESSIVE BUY: {target['symbol']} (+{target['change']:.2f}%)")
            params = {
                'pair': target['raw_id'],
                'type': 'buy',
                'price': int(target['price']),
                'idr': spend
            }
            res = indodax.privatePostTrade(params)
            if res.get('success') == '1':
                print(f"✅ BERHASIL MASUK KE {target['symbol']}!")
            else:
                print(f"Gagal: {res.get('error')}")
        else:
            print("Belum ada koin dengan momentum ledakan yang pas.")

    except Exception as e:
        print(f"Error Aggressive: {e}")

if __name__ == "__main__":
    aggressive_hunt()
