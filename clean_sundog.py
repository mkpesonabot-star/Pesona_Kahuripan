import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def sell_all_sundog():
    try:
        # SUNDOG gantung karena sell tadi integer? Cek saldo real.
        balance = indodax.fetch_balance()
        amount = balance['total'].get('SUNDOG', 0)
        if amount > 0:
            ticker = indodax.fetch_ticker('SUNDOG/IDR')
            price = int(ticker['last'])
            params = {
                'pair': 'sundog_idr',
                'type': 'sell',
                'price': price,
                'sundog': f"{amount:.8f}" # Gunakan 8 desimal biar bersih
            }
            res = indodax.privatePostTrade(params)
            print("Clean Sell SUNDOG:", res)
    except Exception as e:
        print("Error Clean Sell:", e)

if __name__ == "__main__":
    sell_all_sundog()
