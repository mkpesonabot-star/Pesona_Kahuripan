import ccxt

indodax = ccxt.indodax()

def scan_pasar():
    try:
        tickers = indodax.fetch_tickers()
        data = []
        for symbol, ticker in tickers.items():
            if '/IDR' in symbol:
                change = ticker.get('percentage')
                last = ticker.get('last')
                if change is not None and last is not None:
                    data.append({'symbol': symbol, 'change': change, 'price': last})
        
        # Sort manually
        data.sort(key=lambda x: x['change'], reverse=True)
        
        top_gainers = data[:5]
        top_losers = data[-5:]
        top_losers.reverse()
        
        print("=== TOP 5 NAIK (24H) ===")
        for row in top_gainers:
            print(f"{row['symbol']}: {row['change']:.2f}% (Rp {row['price']:,.0f})")
            
        print("\n=== TOP 5 TURUN (24H) ===")
        for row in top_losers:
            print(f"{row['symbol']}: {row['change']:.2f}% (Rp {row['price']:,.0f})")
            
    except Exception as e:
        print(f"Error pas nyecan pasar: {e}")

if __name__ == "__main__":
    scan_pasar()
