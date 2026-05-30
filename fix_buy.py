import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def fix_and_buy():
    try:
        balance = indodax.fetch_balance()
        idr = balance['total'].get('IDR', 0)
        
        # Cari koin yang lagi meledak (Momentum 10 menit)
        tickers = indodax.fetch_tickers()
        candidates = []
        for s, t in tickers.items():
            if '/IDR' in s and s not in ['BTC/IDR', 'ETH/IDR', 'USDT/IDR']:
                if t['quoteVolume'] > 2000000000 and t['last'] > 0:
                    candidates.append({'s': s, 'p': t['last'], 'v': t['quoteVolume']})
        
        # Sort by volume/activity
        candidates.sort(key=lambda x: x['v'], reverse=True)
        
        if candidates and idr >= 10000:
            target = candidates[0]
            raw_id = target['s'].lower().replace('/', '_')
            spend = int(idr * 0.9)
            print(f"🚀 Manual Hit: {target['s']} @ Rp {target['p']}")
            params = {'pair': raw_id, 'type': 'buy', 'price': int(target['p']), 'idr': spend}
            res = indodax.privatePostTrade(params)
            print("Buy Response:", res)
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    fix_and_buy()
