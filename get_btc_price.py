import ccxt

indodax = ccxt.indodax()

def cek_harga_btc():
    try:
        ticker = indodax.fetch_ticker('BTC/IDR')
        return ticker['last']
    except:
        return None

if __name__ == "__main__":
    harga = cek_harga_btc()
    if harga:
        print(harga)
