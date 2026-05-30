import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def panic_sell():
    print("🔥 PANIC SELL: Jual Semua Koin 🔥")
    try:
        balance = indodax.fetch_balance()
        for coin, amount in balance['total'].items():
            if coin == 'IDR' or amount <= 0:
                continue
                
            symbol = f"{coin}/IDR"
            raw_id = f"{coin.lower()}_idr"
            
            try:
                ticker = indodax.fetch_ticker(symbol)
                price = ticker['last']
                value = amount * price
                
                print(f"💰 Found {coin}: {amount} (est. Rp {value:,.0f})")
                
                if value < 10000:
                    print(f"⚠️ Skipping {coin}: Nilai di bawah minimum 10rb IDR")
                    continue

                # Batalkan order yang ada untuk koin ini
                try:
                    res_orders = indodax.privatePostOpenOrders({'pair': raw_id})
                    if res_orders.get('success') == '1' and res_orders.get('return', {}).get('orders'):
                        for o in res_orders['return']['orders']:
                            print(f"❌ Membatalkan order {o['order_id']} untuk {coin}")
                            indodax.privatePostCancelOrder({
                                'pair': raw_id, 
                                'order_id': o['order_id'], 
                                'type': o['type']
                            })
                except:
                    pass

                # Jual instan (2% di bawah harga market biar langsung laku)
                sell_price = int(price * 0.98) 
                print(f"🚀 Jual {coin} @ Rp {sell_price}...")
                
                # Coba format integer dulu, kalau gagal baru pake float string
                clean_amt = int(amount) if amount == int(amount) else f"{amount:.8f}"
                
                params = {
                    'pair': raw_id,
                    'type': 'sell',
                    'price': sell_price,
                    coin.lower(): clean_amt
                }
                res = indodax.privatePostTrade(params)
                
                if res.get('success') == '1':
                    print(f"✅ BERHASIL JUAL {coin}!")
                else:
                    print(f"❌ Gagal jual {coin}: {res.get('error')}")

            except Exception as e:
                print(f"❌ Error pada {coin}: {e}")

    except Exception as e:
        print(f"🚨 Global Error: {e}")

if __name__ == "__main__":
    panic_sell()
