import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def clean_and_buy():
    try:
        # 1. Bersihkan order gantung cuma di koin-koin yang baru kita pake (Biar cepet)
        pairs = ['btc_idr', 'eth_idr', 'sundog_idr', 'aura_idr', 'payai_idr', 'looks_idr', 'trollsol_idr', 'sui_idr']
        for p in pairs:
            try:
                res = indodax.privatePostOpenOrders({'pair': p})
                if res.get('success') == '1' and res.get('return', {}).get('orders'):
                    for o in res['return']['orders']:
                        print(f"Cancelling {p} order {o['order_id']}...")
                        indodax.privatePostCancelOrder({'pair': p, 'order_id': o['order_id'], 'type': o['type']})
            except: continue

        # 2. Re-fetch saldo
        balance = indodax.fetch_balance()
        idr = int(balance['total'].get('IDR', 0))
        print(f"Saldo IDR Ready: Rp {idr:,.0f}")

        # 3. Hunting Micin Momentum (Top Volume)
        if idr >= 11000:
            tickers = indodax.fetch_tickers()
            candidates = []
            for s, t in tickers.items():
                if '/IDR' in s and s not in ['BTC/IDR', 'ETH/IDR', 'USDT/IDR']:
                    if t['quoteVolume'] > 2000000000:
                        candidates.append({'s': s, 'p': t['last'], 'v': t['quoteVolume']})
            
            candidates.sort(key=lambda x: x['v'], reverse=True)
            if candidates:
                target = candidates[0]
                spend = int(idr * 0.95)
                print(f"🚀 TURBO BUY: {target['s']} @ Rp {target['p']}")
                params = {'pair': target['s'].lower().replace('/', '_'), 'type': 'buy', 'price': int(target['p']), 'idr': spend}
                res = indodax.privatePostTrade(params)
                print("Result:", res)
        else:
            print("Saldo IDR belum cukup.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clean_and_buy()
