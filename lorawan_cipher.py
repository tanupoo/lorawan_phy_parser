from AES_ECB import aes_ecb_encrypt as aes128_encrypt
#from AES_CMAC import aes_cmac

'''
Generating LoRaWAN Keys for v1.0

Arguments:
    appkey: 3B
    appnonce: 3B
    netid: 3B
    devnonce: 2B

Return (NwkSKey, AppSKey)

    v1.0.2
    NwkSKey = aes128_encrypt(AppKey, 0x01 | AppNonce | NetID | DevNonce | pad16)
    AppSKey = aes128_encrypt(AppKey, 0x02 | AppNonce | NetID | DevNonce | pad16)
'''
def lorawan_gen_key(appkey, appnonce, netid, devnonce):
    base_data = appnonce + netid + devnonce + b"\x00\x00"
    nskey = aes128_encrypt(appkey, b"\x01" + base_data)
    askey = aes128_encrypt(appkey, b"\x02" + base_data)
    return nskey, askey

def lorawan_mic_joinreq():
    pass

def lorawan_encrypt(key, data):
    return aes128_encrypt(key, data)

if __name__ == "__main__" :
    from binascii import a2b_hex, b2a_hex
    def test_decode(key_hex, data_hex):
        data = aes128_encrypt(a2b_hex(key_hex), a2b_hex(data_hex))
        print("AppNonce:", b2a_hex(data[0:3][::-1]))
        print("NetID:", b2a_hex(data[3:6][::-1]))
        print("DevAddr:", b2a_hex(data[6:10][::-1]))
        print("DLSettings:", b2a_hex(data[10:11]))
        print("RxDelay:", b2a_hex(data[11:12]))
        print("CFList:", b2a_hex(data[12:][::-1]))
    key_hex = "00000000000000000000000000000000"
    data_hex = "eec723f2622b015c0b701ae7bda0c23d"
    test_decode(key_hex, data_hex)
    # AppNonce | NetID | DevAddr | DLSettings | RxDelay | CFList | MIC)
