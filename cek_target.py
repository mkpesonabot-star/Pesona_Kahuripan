import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def hitung_aset_update():
    try:
        balance = indodax.fetch_balance()
        total_value_idr = balance['total'].get('IDR', 0)
        
        for coin, amount in balance['total'].items():
            if coin != 'IDR' and amount > 0:
                try:
                    ticker = indodax.fetch_ticker(f"{coin}/IDR")
                    total_value_idr += (amount * ticker['last'])
                except:
                    continue
        
        # Modal awal 50rb + Top up 57rb
        modal_total = 50000 + 57000
        target = modal_total * 1.3
        progress = (total_value_idr / modal_total - 1) * 100
        
        print(f"Total Aset Sekarang: Rp {total_value_idr:,.0f}")
        print(f"Modal Total (50k + 57k): Rp {modal_total:,.0f}")
        print(f"Target (Profit 30%): Rp {target:,.0f}")
        print(f"Progress Profit: {progress:.2f}%")
        
        if total_value_idr >= target:
            print("STATUS: TARGET TERCAPAI! 🔥")
        else:
            print(f"STATUS: Kurang Rp {target - total_value_idr:,.0f} lagi buat nyentuh profit 30% dari modal total.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hitung_aset_update()
