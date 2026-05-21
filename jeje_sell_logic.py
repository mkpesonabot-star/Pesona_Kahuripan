import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def check_profit_and_sell():
    try:
        balance = indodax.fetch_balance()
        for coin, amount in balance['total'].items():
            if coin != 'IDR' and amount > 0:
                symbol = f"{coin}/IDR"
                raw_id = f"{coin.lower()}_idr"
                
                try:
                    ticker = indodax.fetch_ticker(symbol)
                    current_p = ticker['last']
                    
                    ohlcv = indodax.fetch_ohlcv(symbol, timeframe='1h', limit=2)
                    if len(ohlcv) >= 2:
                        prev_p = ohlcv[0][4]
                        profit_pct = (current_p - prev_p) / prev_p * 100
                        
                        print(f"Checking {coin}: Rp {current_p:,.0f} | 1h: {profit_pct:.2f}% | Amt: {amount}")
                        
                        decision = None
                        if profit_pct >= 1.2: 
                            decision = "PROFIT TAKING 💰"
                        elif profit_pct <= -2.0:
                            decision = "CUT LOSS (Anti Nyungsep) 🛡️"
                        
                        if decision:
                            # Cek nilai minimum order (Indodax biasanya min 10rb IDR)
                            if (amount * current_p) < 10000:
                                print(f"Skipping {coin}: Nilai terlalu kecil (Rp {amount*current_p:,.0f})")
                                continue
                                
                            print(f"{decision} di {coin} ({profit_pct:.2f}%)! JUAL...")
                            params = {
                                'pair': raw_id,
                                'type': 'sell',
                                'price': int(current_p),
                                coin.lower(): int(amount) if amount >= 1 else amount
                            }
                            res = indodax.privatePostTrade(params)
                            if res.get('success') == '1':
                                print(f"✅ BERHASIL JUAL {coin}!")
                            else:
                                print(f"Gagal: {res.get('error')}")
                except Exception as inner_e:
                    print(f"Error checking {coin}: {inner_e}")
                    continue

    except Exception as e:
        print(f"Global Error: {e}")

if __name__ == "__main__":
    check_profit_and_sell()
