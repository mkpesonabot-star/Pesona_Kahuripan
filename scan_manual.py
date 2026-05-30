import ccxt

indodax = ccxt.indodax()

def scan_pasar_manual():
    try:
        tickers = indodax.fetch_tickers()
        data = []
        for symbol, ticker in tickers.items():
            if '/IDR' in symbol:
                last = ticker.get('last')
                # Indodax API often has 'baseVolume' or 'quoteVolume'
                # Let's try to calculate change manually if percentage is None
                # or just look for the most active ones.
                # Actually, let's try fetch_ohlcv for top 5 assets to get change.
                data.append({'symbol': symbol, 'price': last})

        print("=== DAERAH PANTAUAN IDR (5 Sampel) ===")
        for row in data[:10]:
            print(f"- {row['symbol']}: Rp {row['price']:,.0f}")
            
        print("\nBang Rico, Indodax API via CCXT nggak ngasih persentase 'change' langsung.")
        print("Jeje butuh waktu buat narik history harian koin-koin ini satu-satu.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scan_pasar_manual()
