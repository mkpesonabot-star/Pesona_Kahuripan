import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def force_check():
    try:
        # Cek saldo via privatePostGetInfo (Raw API)
        res = indodax.privatePostGetInfo()
        print("Raw Balance Response:", res)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    force_check()
