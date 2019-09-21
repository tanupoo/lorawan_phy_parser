#from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from binascii import b2a_hex

class AES_CMAC():
    '''
    >>> cmac = AES_CMAC(b'Sixteen byte key')
    >>> cmac.update(b'Hello')
    >>> print(cmac.hexdigest())
    '''
    def __init__(self, key):
        self.obj = CMAC.new(key, ciphermod=AES)
        self.__cmac = None

    def update(self, data):
        self.__cmac = self.obj.update(data)

    def get(self):
        return self.__cmac

    def hexdigetst(self):
        return b2a_hex(self.__cmac)

