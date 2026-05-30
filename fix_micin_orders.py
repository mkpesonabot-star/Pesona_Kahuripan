import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

targets = [
    {'coin': 'TROLLSOL', 'pair': 'trollsol_idr', 'target': 1.10},
    {'coin': 'JELLYJELLY', 'pair': 'jellyjelly_idr', 'target': 1.10}
]

def fix_sell_orders():
    print("🛠 Memperbaiki Sell Order (Rounding to Integer)...")
    balance = indodax.fetch_balance()
    
    for item in targets:
        coin = item['coin']
        pair_id = item['pair']
        
        amt = balance['total'].get(coin, 0)
        if amt >= 1:
            # Bulatkan ke bawah agar tidak error decimal
            clean_amt = int(amt)
            ticker = indodax.fetch_ticker(f"{coin}/IDR")
            target_price = int(ticker['last'] * item['target'])
            
            print(f"🎯 Pasang Sell Limit {coin}: {clean_amt} @ Rp {target_price}")
            res = indodax.privatePostTrade({
                'pair': pair_id,
                'type': 'sell',
                'price': target_price,
                coin.lower(): clean_amt
            })
            print(f"Result {coin}:", res)
        else:
            print(f"⚠️ Saldo {coin} tidak cukup atau < 1 ({amt})")

if __name__ == "__main__":
    fix_sell_orders()
