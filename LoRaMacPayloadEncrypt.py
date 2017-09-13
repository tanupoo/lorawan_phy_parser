#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto import Random
import binascii

# The direction field (Dir) is 0 for uplink frames and 1 for downlink frames.
UP_LINK = 0
DOWN_LINK = 1

'''
LoRaWAN MAC Payload encoder/decoder.

Arguments:
    buf_hex: payload in hex.
    key_hex: key in hex, len must be 32 in hex (16-byte).
    devaddr_hex: DevAddr in hex, len must be 8 in hex (4-byte).
    dir_down: UP_LINK(=0) or DOWN_LINK(=1)
    fcnt_hex: FCnt in hex, len must be 8 in hex (4-byte).
        i.e. 16-bit maintained value + 16-bit in the payload
        if you don't know the former vlaue, it should be "0000".
    bigendian:
        False if you pass the hex bytes in the LoRaWAN MAC payload as it is.
        e.g. if DevAddr is "12345678", the form in the payload is "78563412".
        if you pass "78563412" to this function, the flag of bigendian has
        to be False.

This function refers to the function, LoRaMacPayloadEncrypt().
    https://github.com/Lora-net/LoRaMac-node/blob/master/src/mac/LoRaMacCrypto.c#L108
in Lora-net/LoRaMac-node.
4.3.3 MAC Frame Payload Encryption (FRMPayload) as well.
'''
def LoRaMacPayloadEncrypt(buf_hex, key_hex, devaddr_hex, dir_down, fcnt_hex,
                          bigendian=True):
    buf = bytearray(binascii.a2b_hex(buf_hex))
    key = binascii.a2b_hex(key_hex)
    devaddr = binascii.a2b_hex(devaddr_hex)
    fcnt = binascii.a2b_hex(fcnt_hex)
    size = len(buf)
    encBuffer = bytearray(size)

    cipher = AES.new(key, AES.MODE_ECB)

    def aes_encrypt_block(aBlock):
        return bytearray(cipher.encrypt(str(aBlock)))

    aBlock = bytearray(16)
    aBlock[0] = 1
    aBlock[5] = dir_down
    if bigendian:
        aBlock[6] = devaddr[3]
        aBlock[7] = devaddr[2]
        aBlock[8] = devaddr[1]
        aBlock[9] = devaddr[0]
        aBlock[10] = fcnt[3]
        aBlock[11] = fcnt[2]
        aBlock[12] = fcnt[1]
        aBlock[13] = fcnt[0]
    else:
        aBlock[6] = devaddr[0]
        aBlock[7] = devaddr[1]
        aBlock[8] = devaddr[2]
        aBlock[9] = devaddr[3]
        aBlock[10] = fcnt[0]
        aBlock[11] = fcnt[1]
        aBlock[12] = fcnt[2]
        aBlock[13] = fcnt[3]

    bufferIndex = 0
    ctr = 1

    while size >= 16:
        aBlock[15] = ctr & 0xff
        ctr += 1
        sBlock = aes_encrypt_block(aBlock)
        for i in range(16):
            encBuffer[bufferIndex + i] = buf[bufferIndex + i] ^ sBlock[i]
        size -= 16
        bufferIndex += 16

    if size > 0:
        aBlock[15] = ctr & 0xff
        sBlock = aes_encrypt_block(aBlock)
        for i in range(size):
            encBuffer[bufferIndex + i] = buf[bufferIndex + i] ^ sBlock[i]

    return encBuffer

