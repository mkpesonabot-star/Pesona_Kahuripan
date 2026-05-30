import ccxt
import time
import sys
from datetime import datetime

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

# Target Koin yang kita hold
coins = {
    'ZKJ/IDR': {'pair_id': 'zkj_idr', 'highest': 0, 'drop_limit': 0.02}, # Jual kalau turun 2% dari puncak
    'BTC/IDR': {'pair_id': 'btc_idr', 'highest': 0, 'drop_limit': 0.015}, # Jual kalau turun 1.5% dari puncak
    'ETH/IDR': {'pair_id': 'eth_idr', 'highest': 0, 'drop_limit': 0.015} 
}

def log(msg):
    waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    teks = f"[{waktu}] {msg}"
    print(teks)
    with open("trading_log.txt", "a") as f:
        f.write(teks + "\n")

def check_and_sell():
    log("Bot Penjaga aktif. Memantau pergerakan harga...")
    while True:
        try:
            info = indodax.privatePostGetInfo()
            balances = info.get('return', {}).get('balance', {})
            
            for symbol, config in coins.items():
                koin_nama = symbol.split('/')[0].lower()
                saldo_koin = float(balances.get(koin_nama, 0))
                
                # Kalau saldo koin 0, skip
                if saldo_koin == 0:
                    continue
                
                ticker = indodax.fetch_ticker(symbol)
                last_price = ticker['last']
                bid_price = ticker['bid'] # Harga kalau kita jual instan sekarang
                
                # Update rekor harga tertinggi (Trailing Stop logic)
                if last_price > config['highest']:
                    config['highest'] = last_price
                
                # Hitung persentase penurunan dari puncak
                if config['highest'] > 0:
                    drop_percent = (config['highest'] - last_price) / config['highest']
                    
                    if drop_percent >= config['drop_limit']:
                        log(f"🚨 {symbol} turun {drop_percent*100:.2f}% dari pucuk! Momentum melemah. Eksekusi JUAL!")
                        
                        # Jual semua saldo koin ini
                        try:
                            # Menggunakan post trade indodax
                            response = indodax.privatePostTrade({
                                'pair': config['pair_id'],
                                'type': 'sell',
                                'price': bid_price,
                                koin_nama: saldo_koin
                            })
                            log(f"✅ Jual {symbol} BERHASIL: {response}")
                            # Reset agar tidak dijual berulang
                            config['highest'] = 0 
                        except Exception as sell_err:
                            log(f"❌ Gagal jual {symbol}: {sell_err}")
                            
        except Exception as e:
            log(f"⚠️ Error pantauan: {e}")
            
        # Istirahat 2 menit sebelum ngecek lagi
        time.sleep(120)

if __name__ == '__main__':
    check_and_sell()
