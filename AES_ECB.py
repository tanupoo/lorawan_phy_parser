from Crypto.Cipher import AES

class AES_ECB():
    def __init__(self, key):
        '''
        key: 8 bytes of bytearray
        '''
        self.aes_ecb = AES.new(key, AES.MODE_ECB)

    def encrypt(self, data):
        '''
        data: any size of bytearray. expanded into 16 bytes if less.
        '''
        blk_list = []
        for i in range(0,len(data),16):
            blk = data[i:i+16]
            blk += b"\x00"*(16-len(blk))
            blk_list.append(self.encrypt_fixed(blk))
        return b"".join(blk_list)

    def encrypt_fixed(self, blk):
        '''
        data: the size of data must be 16 bytes.
        '''
        return self.aes_ecb.encrypt(bytes(blk))

def aes_ecb_encrypt(key, data):
    '''
    key: in bytes.
    data: in bytes.
    '''
    cipher = AES_ECB(key)
    return cipher.encrypt(data)

