import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def scan_micin_and_buy():
    try:
        tickers = indodax.fetch_tickers()
        balance = indodax.fetch_balance()
        idr = balance['total'].get('IDR', 0)
        
        candidates = []
        for symbol, ticker in tickers.items():
            if '/IDR' in symbol:
                vol = ticker.get('quoteVolume', 0)
                # Kriteria Micin Potensial: Volume > 5 Miliar IDR (Lagi Rame)
                if vol > 5000000000:
                    # Ambil OHLCV buat cek kenaikan 1 jam terakhir
                    ohlcv = indodax.fetch_ohlcv(symbol, timeframe='1h', limit=2)
                    if len(ohlcv) >= 2:
                        open_p = ohlcv[0][1]
                        close_p = ohlcv[1][4]
                        change = (close_p - open_p) / open_p * 100
                        if change > 1.0: # Naik > 1% dalam sejam terakhir (momentum)
                            candidates.append({'symbol': symbol, 'change': change, 'price': close_p})
        
        if not candidates:
            print("Belum ada koin micin yang 'panas' momennya Bang.")
            return

        # Ambil yang kenaikannya paling oke tapi belum overbought
        candidates.sort(key=lambda x: x['change'], reverse=True)
        target = candidates[0]
        
        print(f"Target Terdeteksi: {target['symbol']} (Naik {target['change']:.2f}% dlm 1 jam)")
        
        if idr >= 10000:
            print(f"🚀 HAJAR BUY {target['symbol']} senilai Rp {idr*0.9:,.0f}...")
            # order = indodax.create_market_buy_order(target['symbol'], idr * 0.9)
            # print("✅ BUY BERHASIL!")
            print("(Simulasi: Buy dinonaktifkan sementara untuk pengecekan akhir logic)")
        else:
            print("Saldo kurang Bang.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scan_micin_and_buy()
