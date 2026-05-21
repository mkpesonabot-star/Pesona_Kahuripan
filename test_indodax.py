import ccxt

indodax = ccxt.indodax()

def check_tickers():
    try:
        tickers = indodax.fetch_tickers()
        print(f"Total symbols found: {len(tickers)}")
        # Print sample to see structure
        sample_keys = list(tickers.keys())[:5]
        for k in sample_keys:
            t = tickers[k]
            print(f"Symbol: {k}, Last: {t.get('last')}, Change: {t.get('percentage')}")
            
        data = []
        for symbol, ticker in tickers.items():
            # Indodax symbols in ccxt might be 'BTC/IDR' or 'btc_idr'
            if 'IDR' in symbol.upper():
                last = ticker.get('last')
                # Some exchange might use 'change' or 'percentage'
                change = ticker.get('percentage')
                if change is None:
                    # Fallback or calculation if needed, but ccxt usually provides percentage
                    pass
                
                if last is not None and change is not None:
                    data.append({'symbol': symbol, 'change': change, 'price': last})

        data.sort(key=lambda x: x['change'], reverse=True)
        
        print("\n=== TOP GAINERS (IDR) ===")
        for row in data[:5]:
            print(f"{row['symbol']}: {row['change']}% (Rp {row['price']:,.0f})")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_tickers()
