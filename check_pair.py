import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def check_pair():
    try:
        markets = indodax.load_markets()
        print("Mencari pair ONDO...")
        for m in markets:
            if 'ONDO' in m:
                print(f"Ketemu Pair: {m}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_pair()
