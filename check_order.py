import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

try:
    print("\nCek status order aktif (Open Orders)...")
    open_orders = indodax.privatePostOpenOrders()
    print(open_orders)
    
    print("\nCek saldo terbaru...")
    info = indodax.privatePostGetInfo()
    balance_idr = info.get('return', {}).get('balance', {}).get('idr', 0)
    balance_zkj = info.get('return', {}).get('balance', {}).get('zkj', 0)
    print(f"Saldo IDR: Rp {balance_idr}")
    print(f"Saldo ZKJ: {balance_zkj}")

except Exception as e:
    print(f"❌ Error: {e}")
