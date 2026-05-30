import ccxt

indodax = ccxt.indodax({
    'apiKey': 'J39YD5BL-KYLUOKNM-SRVXBFGO-AH28R0GI-PATUIOOP',
    'secret': '5bb884c048bb0b77049edd11045457fb2096df5efe7139ad1675f9c709178ba79e23be6cc2f0d4d6',
    'enableRateLimit': True,
})

def cancel_manual():
    try:
        # API Indodax raw method for open orders: openOrders
        res = indodax.privatePostOpenOrders({'pair': 'btc_idr'})
        print("Open Orders:", res)
        if res.get('success') == '1' and res.get('return', {}).get('orders'):
            for o in res['return']['orders']:
                oid = o['order_id']
                print(f"Cancelling {oid}...")
                indodax.privatePostCancelOrder({'pair': 'btc_idr', 'order_id': oid, 'type': o['type']})
            print("OK.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    cancel_manual()
