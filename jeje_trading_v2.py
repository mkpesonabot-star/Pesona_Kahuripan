import ccxt
import time
from datetime import datetime

# API Config
indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
    'rateLimit': 2000,
})

def get_rsi(symbol):
    try:
        ohlcv = indodax.fetch_ohlcv(symbol, timeframe='1h', limit=30)
        closes = [x[4] for x in ohlcv]
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        avg_gain = sum([d if d > 0 else 0 for d in deltas[-14:]]) / 14
        avg_loss = sum([-d if d < 0 else 0 for d in deltas[-14:]]) / 14
        rs = avg_gain / avg_loss if avg_loss > 0 else 100
        return 100 - (100 / (1 + rs))
    except Exception as e:
        if "too_many_requests" in str(e):
            print(f"Rate limit hit during RSI fetch for {symbol}, sleeping...")
            time.sleep(5)
        return 50

def run_trading_v2_optimized():
    try:
        print(f"=== JEJE TRADING V2 SCAN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===", flush=True)
        
        # 1. Get tickers
        tickers_info = indodax.fetch_tickers()
        print(f"Fetched {len(tickers_info)} tickers.", flush=True)

        # 2. Portfolio Management (Exit based on TP/SL)
        balance = indodax.fetch_balance()
        print(f"Checking portfolio for TP/SL...", flush=True)
        for coin, amt in balance['total'].items():
            if coin != 'IDR' and amt > 0:
                symbol = f"{coin.upper()}/IDR"
                if symbol in tickers_info:
                    t = tickers_info[symbol]
                    curr_p = t['last']
                    change = t.get('percentage', 0)
                    if change is None: change = 0
                    
                    if change >= 3.0 or change <= -1.5:
                        if (amt * curr_p) >= 10000:
                            print(f"💰 SELLING {coin} at {curr_p} (Change: {change}%)")
                            indodax.privatePostTrade({
                                'pair': symbol.lower().replace('/', '_'),
                                'type': 'sell',
                                'price': int(curr_p),
                                coin.lower(): f"{amt:.8f}"
                            })

        # 3. Hunting Micin
        idr = int(balance['total'].get('IDR', 0))
        print(f"Saldo IDR Ready: Rp {idr:,.0f}", flush=True)
        
        if idr < 15000: 
            print("Insufficient balance for new trades.")
            return

        candidates = []
        # Scanning loop removed as requested
        # for s, t in tickers_info.items():
        #     ...
        
        candidates.sort(key=lambda x: x['rsi'])
        
        for target in candidates:
            if idr < 15000: break
            print(f"🚀 BUY {target['s']} (Price: {target['p']}, RSI: {target['rsi']:.2f})")
            res = indodax.privatePostTrade({
                'pair': target['s'].lower().replace('/', '_'),
                'type': 'buy',
                'price': int(target['p']),
                'idr': 15000
            })
            if res.get('success') == '1':
                idr -= 15000
                print(f"✅ Executed buy for {target['s']}")

    except Exception as e:
        print(f"Bot Error: {e}")

if __name__ == "__main__":
    run_trading_v2_optimized()
