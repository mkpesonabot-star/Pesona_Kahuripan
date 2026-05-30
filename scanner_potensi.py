import ccxt

indodax = ccxt.indodax({'enableRateLimit': True})

def scan_markets():
    print("Mencari koin dengan aktivitas tertinggi di Indodax hari ini...\n")
    try:
        tickers = indodax.fetch_tickers()
        idr_markets = {symbol: data for symbol, data in tickers.items() if '/IDR' in symbol}
        
        # Urutkan berdasarkan volume IDR
        sorted_by_volume = sorted(
            idr_markets.items(), 
            key=lambda x: float(x[1].get('quoteVolume') or 0), 
            reverse=True
        )
        
        print("🔥 TOP 5 KOIN POTENSIAL (Berdasarkan Volume Transaksi IDR):")
        print("*(Momentum 100% artinya harga saat ini menyentuh titik tertinggi dalam 24 jam)*\n")
        
        for symbol, data in sorted_by_volume[:5]:
            vol = float(data.get('quoteVolume') or 0)
            last = float(data.get('last') or 0)
            high = float(data.get('high') or 0)
            low = float(data.get('low') or 0)
            
            # Hitung posisi harga saat ini di antara low dan high 24 jam
            if high > low:
                posisi = ((last - low) / (high - low)) * 100
            else:
                posisi = 0
                
            print(f"🔹 {symbol}")
            print(f"   Harga : Rp {last:,.0f}")
            print(f"   Volume: Rp {vol:,.0f}")
            print(f"   Range : Rp {low:,.0f} - Rp {high:,.0f} (Momentum: {posisi:.1f}%)\n")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    scan_markets()
