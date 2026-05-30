import ccxt

indodax = ccxt.indodax()

def scan_all_idr():
    try:
        tickers = indodax.fetch_tickers()
        signals = []
        for symbol, ticker in tickers.items():
            if '/IDR' in symbol and ticker['last'] > 0:
                # Karena percentage None, kita cari koin yang lagi rame volumenya
                vol = ticker.get('quoteVolume', 0)
                if vol > 1000000000: # Volume > 1 Milyar IDR
                    signals.append({'symbol': symbol, 'price': ticker['last'], 'vol': vol})
        
        signals.sort(key=lambda x: x['vol'], reverse=True)
        print("=== KOIN RAME (VOLUME > 1M IDR) ===")
        for s in signals[:10]:
            print(f"- {s['symbol']}: Rp {s['price']:,.0f} (Vol: Rp {s['vol']:,.0f})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scan_all_idr()
