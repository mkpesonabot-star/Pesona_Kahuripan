import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def liquid_exit():
    try:
        # 1. Bersihkan order gantung dulu
        pairs = ['sui_idr', 'sundog_idr', 'looks_idr']
        for p in pairs:
            try:
                res = indodax.privatePostOpenOrders({'pair': p})
                if res.get('success') == '1' and res.get('return', {}).get('orders'):
                    for o in res['return']['orders']:
                        indodax.privatePostCancelOrder({'pair': p, 'order_id': o['order_id'], 'type': o['type']})
            except: continue

        # 2. Jual SUI & SUNDOG instan
        balance = indodax.fetch_balance()
        assets = {'SUI': 'sui_idr', 'SUNDOG': 'sundog_idr'}
        
        for coin, pair in assets.items():
            amt = balance['total'].get(coin, 0)
            if amt > 0:
                ticker = indodax.fetch_ticker(coin + '/IDR')
                price = int(ticker['last'] * 0.99) # Sell 1% below market for instant fill
                print(f"🚀 Liquidating {coin}: {amt} @ Rp {price}")
                params = {
                    'pair': pair,
                    'type': 'sell',
                    'price': price,
                    coin.lower(): f"{amt:.8f}"
                }
                res = indodax.privatePostTrade(params)
                print(f"Result {coin}:", res)

    except Exception as e:
        print(f"Error Liquid: {e}")

if __name__ == "__main__":
    liquid_exit()
