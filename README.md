LoRaWAN PHY Payload Parser
==========================

This is a parser tool of the LoRaWAN PHY payload.

## Requirement

Python 2.7 is required.

Not tested with Python 3.x.

## Usage

    lorawan_phy_parser.py [-h] [-b BEACON_RFU] [--nsekey NSEKEY]
                          [--askey ASKEY] [--xfcnt XFCNT] [-i] [-v] [-d]
                          [HEX_STR [HEX_STR ...]]
    
    LoRaWAN frame parser. You can use stdin to pass the hex string if
    the HEX_STR is '-'.
    
    positional arguments:
      HEX_STR          a series or multiple of hex string.
    
    optional arguments:
      -h, --help       show this help message and exit
      -b BEACON_RFU    specify the number of bytes of the RFU in the beacon.
      --nsekey NSEKEY  specify NwkSEncKey(v1.1) or NwkSKey(v1.0.2).
      --askey ASKEY    specify AppSKey.
      --xfcnt XFCNT    specify the most significant 16-bit of the FCnt in hex.
      -i               ignore error. keep processing if any error happen
      -v               enable verbose mode.
      -d               increase debug mode.

## How to pass the hex string of the data

You can put the hex string of the LoRaWAN PHY Payload into the arguments.
The following string are decoded as a same string.  i.e. '01 02 03 04'

    01020304
    0102 0304
    01.02.03.04
    0x01 0x02 0x03 0x04
    0x01,0x02,0x03,0x04
    0102,0304

The separater is a new line code.
If you make a file containing some lines of the hex string like below.

    01020304
    05060708
    0a0b0c0d

The parser can decode each of them separately.
Don't forget to specify "-" as the argument to pass the content of
the file from the stdin, and the -i option if needed.  e.g.

    cat file | lorawan_phy_parser.py - -i

## How to use

It will parse the string and show the result like below.

    % lorawan_phy_parser.py 402105810080c9fe02a434eaa5f9787f187538d9b054ea0ffcb67898d4
    === PHYPayload ===
    [x 40 21 05 81 00 80 c9 fe 02 a4 34 ea a5 f9 78 7f 18 75 38 d9 b0 54 ea 0f fc b6 78 98 d4]
    ## MHDR           [x40] [b01000000]
      MType         : Unconfirmed Data Up [b010]
      RFU           : [b000]
      Major         : LoRaWAN R1 [b00]
    ## MACPayload
      FHDR            [x2105810080c9fe02a434eaa5f9787f187538d9b054ea0ffc]
        DevAddr     : 00810521 [x21058100]
        FCtrl       : [x80] [b10000000]
          ADR       : 1
          ADRACKReq : 0
          ACK       : 0
          RFU/ClsB  : 0
          FOptsLen  : 0 [b0000]
        FCnt        : 65225 [xc9fe]
    ## FPort        : 2 [x02]
    ## FRMPayload   : a434eaa5f9787f187538d9b054ea0ffc
    ## MIC          : b67898d4

If the payload include FOpts (MAC Commands) and if you use the -v option,
the output will be like below.
You can see a short description of each command.

    % lorawan_phy_parser.py 809a4ed301080200050707030703070308d7bcacbcfa
    === PHYPayload ===
    [x 80 9a 4e d3 01 08 02 00 05 07 07 03 07 03 07 03 08 d7 bc ac bc fa]
    ## MHDR           [x80] [b10000000]
      MType         : Confirmed Data Up [b100]
      RFU           : [b000]
      Major         : LoRaWAN R1 [b00]
    ## MACPayload
      FHDR            [x9a4ed301080200050707030703070308d7]
        DevAddr     : 01d34e9a [x9a4ed301]
        FCtrl       : [x08] [b00001000]
          ADR       : 0
          ADRACKReq : 0
          ACK       : 0
          RFU/ClsB  : 0
          FOptsLen  : 8 [b1000]
        FCnt        : 2 [x0200]
        FOpts         [x0507070307030703]
    ## MAC Command (No. CMD (CID DIR) [MSG])
      01. RXParamSetupAns (x05 uplink) [07]
        Status           : [b00000111]
          RFU            : [b00000]
          RX1DRoffset ACK: 1
            ** Detail:  RX1DRoffset was successfully set. 
        RX2 Data rate ACK: 1
            ** Detail:  RX2 slot channel was successfully set. 
        Channel ACK      : 1
            ** Detail:  RX2 slot channel was successfully set. 
      02. NewChannelAns (x07 uplink) [03]
        Status                : [x03]
          RFU                 : [b000000]
          Data rate range ok  : 1
            ** Detail:  The data rate range is compatible with the possibilities of the end-device. 
          Channel frequency ok: 1
            ** Detail:  The device is able to use this frequency. 
      03. NewChannelAns (x07 uplink) [03]
        Status                : [x03]
          RFU                 : [b000000]
          Data rate range ok  : 1
            ** Detail:  The data rate range is compatible with the possibilities of the end-device. 
          Channel frequency ok: 1
            ** Detail:  The device is able to use this frequency. 
      04. NewChannelAns (x07 uplink) [03]
        Status                : [x03]
          RFU                 : [b000000]
          Data rate range ok  : 1
            ** Detail:  The data rate range is compatible with the possibilities of the end-device. 
          Channel frequency ok: 1
            ** Detail:  The device is able to use this frequency. 
    ## FPort        : 8 [x08]
    ## FRMPayload   : d7
    ## MIC          : bcacbcfa

If the payload contains the encrypted field, you can specify NwkKey and/or AppSKey to decrypt it.  The following example specifies the AppSKey.

    % lorawan_phy_parser.py --askey=AAAAAAAAAAAAAAAAAAAAAAAAAAAAAABB 40,B2,00,EF,BE,9A,03,00,03,07,05,07,07,03,07,03,10,04,02,09,AA,50,B1,F0,79,2F,31,AD,9C,63,78,5F,83,8D,95,C6,FE,81,D2,97,09,BA,3C,6E,19,B7,71,43,7C,
    === PHYPayload ===
    [x 40 B2 00 EF BE 9A 03 00 03 07 05 07 07 03 07 03 10 04 02 09 AA 50 B1 F0 79 2F 31 AD 9C 63 78 5F 83 8D 95 C6 FE 81 D2 97 09 BA 3C 6E 19 B7 71 43 7C]
    ## MHDR           [x40] [b01000000]
      MType         : Unconfirmed Data Up [b010]
      RFU           : [b000]
      Major         : LoRaWAN R1 [b00]
    ## MACPayload
      FHDR            [xB200EFBE9A0300030705070703070310040209AA50B1F0792F31AD9C63785F838D95C6FE81D29709BA3C6E19]
        DevAddr     : BEEF00B2 [xB200EFBE]
        FCtrl       : [x9A] [b10011010]
          ADR       : 1
          ADRACKReq : 0
          ACK       : 0
          RFU/ClsB  : 1
          FOptsLen  : 10 [b1010]
        FCnt        : 3 [x0300]
        FOpts         [x03070507070307031004]
    ## MAC Command (No. CMD (CID DIR) [MSG])
      01. LinkADRAns (x03 uplink) [07]
        Status            : [b00000111] [x07]
          RFU             : [b00000]
          Power ACK       : 1
          Data_rate_ACK   : 1
          Channel_mask_ACK: 1
      02. RXParamSetupAns (x05 uplink) [07]
        Status           : [b00000111]
          RFU            : [b00000]
          RX1DRoffset ACK: 1
        RX2 Data rate ACK: 1
        Channel ACK      : 1
      03. NewChannelAns (x07 uplink) [03]
        Status                : [x03]
          RFU                 : [b000000]
          Data rate range ok  : 1
          Channel frequency ok: 1
      04. NewChannelAns (x07 uplink) [03]
        Status                : [x03]
          RFU                 : [b000000]
          Data rate range ok  : 1
          Channel frequency ok: 1
      05. PingSlotInfoReq (x10 uplink) [04]
        PingSlotParam: [b00000100] [x04]
          RFU        : [b0000]
          Periodicity: 2 [b10]
        FPort       : 2 [x02]
    ## FRMPayload   : [x09AA50B1F0792F31AD9C63785F838D95C6FE81D29709BA3C6E19]
      x 00 00 09 c4 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    ## MIC          : B771437C

