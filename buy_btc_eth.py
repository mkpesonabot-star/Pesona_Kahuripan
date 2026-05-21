import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

try:
    print("\nCoba beli BTC dengan Rp 15,000...")
    ticker = indodax.fetch_ticker('BTC/IDR')
    harga_beli = ticker['ask']
    
    response = indodax.privatePostTrade({
        'pair': 'btc_idr',
        'type': 'buy',
        'price': harga_beli,
        'idr': 15000
    })
    
    print("\n✅ Order BTC POST Trade Indodax BERHASIL!")
    print(response)
    
except Exception as e:
    print(f"❌ Error BTC: {e}")

try:
    print("\nCoba beli ETH dengan Rp 15,000...")
    ticker = indodax.fetch_ticker('ETH/IDR')
    harga_beli = ticker['ask']
    
    response = indodax.privatePostTrade({
        'pair': 'eth_idr',
        'type': 'buy',
        'price': harga_beli,
        'idr': 15000
    })
    
    print("\n✅ Order ETH POST Trade Indodax BERHASIL!")
    print(response)
    
except Exception as e:
    print(f"❌ Error ETH: {e}")

try:
    print("\nCek saldo terbaru...")
    info = indodax.privatePostGetInfo()
    balance_idr = info.get('return', {}).get('balance', {}).get('idr', 0)
    balance_zkj = info.get('return', {}).get('balance', {}).get('zkj', 0)
    balance_btc = info.get('return', {}).get('balance', {}).get('btc', 0)
    balance_eth = info.get('return', {}).get('balance', {}).get('eth', 0)
    print(f"Saldo IDR: Rp {balance_idr}")
    print(f"Saldo ZKJ: {balance_zkj}")
    print(f"Saldo BTC: {balance_btc}")
    print(f"Saldo ETH: {balance_eth}")

except Exception as e:
    print(f"❌ Error saldo: {e}")
