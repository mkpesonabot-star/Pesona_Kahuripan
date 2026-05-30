import ccxt
import time
from datetime import datetime

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

# Koin yang dipantau (Drop limit 5% dari harga beli)
# Harga beli tadi: TROLLSOL ~2100, JELLY ~1179, ZEREBRO ~736
monitored_coins = {
    'TROLLSOL/IDR': {'pair_id': 'trollsol_idr', 'stop_loss': 1995}, # 2100 - 5%
    'JELLYJELLY/IDR': {'pair_id': 'jellyjelly_idr', 'stop_loss': 1120}, # 1179 - 5%
    'ZEREBRO/IDR': {'pair_id': 'zerebro_idr', 'stop_loss': 700} # 736 - 5%
}

def log(msg):
    waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{waktu}] {msg}")

def safety_guard():
    log("🛡 Safety Guard aktif. Memantau batas bawah aman (Stop Loss 5%)...")
    while True:
        try:
            balance = indodax.fetch_balance()
            for symbol, config in monitored_coins.items():
                coin_name = symbol.split('/')[0]
                amount = balance['total'].get(coin_name, 0)
                
                if amount < 1: continue
                
                ticker = indodax.fetch_ticker(symbol)
                last_price = ticker['last']
                
                if last_price <= config['stop_loss']:
                    log(f"🚨 ALERT: {coin_name} nyungsep ke Rp {last_price}! Di bawah batas aman Rp {config['stop_loss']}.")
                    log(f"Executing PANIC SELL for {coin_name}...")
                    
                    # 1. Cancel existing sell orders
                    try:
                        indodax.privatePostCancelOrder({'pair': config['pair_id'], 'type': 'sell'}) # Not efficient, but safe
                    except: pass
                    
                    # 2. Sell everything
                    try:
                        res = indodax.privatePostTrade({
                            'pair': config['pair_id'],
                            'type': 'sell',
                            'price': int(last_price * 0.98), # Sell lower for instant fill
                            coin_name.lower(): int(amount)
                        })
                        log(f"✅ Safe Exit {coin_name}: {res}")
                    except Exception as e:
                        log(f"❌ Gagal Safe Exit {coin_name}: {e}")
            
            time.sleep(300) # Cek tiap 5 menit
        except Exception as e:
            log(f"⚠️ Guard Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    safety_guard()
