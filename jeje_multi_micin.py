import ccxt
import time

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

# Target: TROLLSOL, JELLYJELLY, ZEREBRO (Micin potensial)
# Alokasi per koin Rp 15,000
targets = [
    {'coin': 'TROLLSOL', 'pair': 'trollsol_idr'},
    {'coin': 'JELLYJELLY', 'pair': 'jellyjelly_idr'},
    {'coin': 'ZEREBRO', 'pair': 'zerebro_idr'}
]

AMOUNT_PER_COIN = 15000

def execute_strategy():
    print(f"🚀 Memulai strategi alokasi Rp {AMOUNT_PER_COIN} per koin micin...")
    
    for item in targets:
        try:
            coin = item['coin']
            pair_id = item['pair']
            symbol = f"{coin}/IDR"
            
            # 1. Cek Harga
            ticker = indodax.fetch_ticker(symbol)
            price = ticker['last']
            ask_price = ticker['ask'] # Harga beli instan
            
            print(f"\n🔹 Eksekusi {coin}:")
            print(f"   Harga Market: Rp {price:,.0f} | Harga Beli Instan: Rp {ask_price:,.0f}")
            
            # 2. Hitung jumlah koin (Rp 15.000 / harga beli)
            # Indodax fee ~0.51% (taker), jadi kita sesuaikan sedikit
            amount_to_buy = AMOUNT_PER_COIN / ask_price
            
            # 3. Eksekusi BELI (Market/Instan)
            print(f"   Membeli {amount_to_buy:.8f} {coin}...")
            
            # Format amount agar tidak terlalu banyak desimal (Indodax sensitif)
            clean_amount = int(amount_to_buy) if amount_to_buy >= 1 else f"{amount_to_buy:.8f}"
            
            buy_res = indodax.privatePostTrade({
                'pair': pair_id,
                'type': 'buy',
                'price': int(ask_price),
                'idr': AMOUNT_PER_COIN
            })
            
            if buy_res.get('success') == '1':
                print(f"   ✅ BERHASIL BELI {coin}!")
                
                # 4. Pasang Sell Limit (Target Profit 10% agar bersih setelah fee)
                # Fee beli 0.51% + Fee jual 0.51% = ~1.02%. 
                # Jika target 10%, maka profit bersih ~9%.
                target_price = int(ask_price * 1.10)
                
                # Tunggu saldo terupdate sebentar
                time.sleep(2)
                balance = indodax.fetch_balance()
                actual_amount = balance['total'].get(coin, 0)
                
                if actual_amount > 0:
                    print(f"   🎯 Pasang target jual di Rp {target_price:,.0f} (Profit ~10%)")
                    sell_res = indodax.privatePostTrade({
                        'pair': pair_id,
                        'type': 'sell',
                        'price': target_price,
                        coin.lower(): f"{actual_amount:.8f}"
                    })
                    if sell_res.get('success') == '1':
                        print(f"   ✅ Sell Order terpasang!")
                    else:
                        print(f"   ❌ Gagal pasang sell order: {sell_res.get('error')}")
            else:
                print(f"   ❌ Gagal beli {coin}: {buy_res.get('error')}")
                
        except Exception as e:
            print(f"   ⚠️ Error pada {item['coin']}: {e}")

if __name__ == "__main__":
    execute_strategy()
