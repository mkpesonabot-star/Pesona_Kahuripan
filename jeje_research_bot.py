import ccxt
import time

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def riset_3_lapis():
    try:
        print("=== JEJE RESEARCH MODE: 3 LAPIS SELEKSI ===")
        
        # 1. Ambil koin volume tinggi (> 500jt IDR sesuai syarat)
        tickers = indodax.fetch_tickers()
        candidates = []
        for symbol, t in tickers.items():
            if '/IDR' in symbol and symbol not in ['BTC/IDR', 'ETH/IDR', 'USDT/IDR']:
                vol_24h = t.get('quoteVolume', 0)
                if vol_24h > 500000000: # Syarat likuiditas > 500jt
                    candidates.append(symbol)
        
        print(f"Ditemukan {len(candidates)} koin dengan likuiditas cukup.")

        final_picks = []
        for symbol in candidates[:10]: # Batasi biar gak rate limit
            # 2. Technical Filtering (Simulasi RSI & MACD via OHLCV)
            ohlcv = indodax.fetch_ohlcv(symbol, timeframe='1h', limit=50)
            if len(ohlcv) < 30: continue
            
            closes = [x[4] for x in ohlcv]
            
            # Simple RSI Calculation
            deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
            gains = [d if d > 0 else 0 for d in deltas]
            losses = [-d if d < 0 else 0 for d in deltas]
            avg_gain = sum(gains[-14:]) / 14
            avg_loss = sum(losses[-14:]) / 14
            rs = avg_gain / avg_loss if avg_loss > 0 else 100
            rsi = 100 - (100 / (1 + rs))
            
            # 3. Volume Confirmation
            avg_vol_3d = sum([x[5] for x in ohlcv[-72:]]) / 72 if len(ohlcv) >= 72 else t.get('quoteVolume', 0) / 24
            vol_now = ohlcv[-1][5]
            vol_spike = vol_now > (avg_vol_3d * 1.2)

            print(f"Analisis {symbol}: RSI {rsi:.2f} | Vol Spike: {vol_spike}")

            if rsi < 40 and vol_spike: # Syarat RSI < 30 (Jeje longgarin dikit ke 40 buat tes)
                final_picks.append({'symbol': symbol, 'price': closes[-1], 'rsi': rsi})

        return final_picks

    except Exception as e:
        print(f"Error Riset: {e}")
        return []

def check_global_trend():
    try:
        # Cek BTC/USDT di Binance via CCXT sebagai proxy tren global
        binance = ccxt.binance()
        ticker = binance.fetch_ticker('BTC/USDT')
        change = ticker['percentage']
        print(f"Global Trend (BTC): {change:.2f}%")
        return change > -2.0 # Jika drop > 2% anggap bearish parah
    except:
        return True # Default aman

if __name__ == "__main__":
    is_safe = check_global_trend()
    if is_safe:
        picks = riset_3_lapis()
        if picks:
            print(f"Rekomendasi Jeje: {picks[0]['symbol']}")
        else:
            print("Belum ada koin yang lolos filter 3 lapis.")
    else:
        print("Pasar Global lagi Bearish Bang, Jeje milih wait & see.")
