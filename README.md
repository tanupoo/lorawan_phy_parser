LoRaWAN PHY Payload Parser
==========================

## Requirement

Python 2.7 is required.

It probably doesn't work with Python 3.x.

## How to use

You can put the hex string of the LoRaWAN PHY Payload into the arughtment.
Or, you can pass the string as its stdin.

Then, it will parse the string and show the result like below.

    % python lrw_phy_parser.py 402105810080c9fe02a434eaa5f9787f187538d9b054ea0ffcb67898d4
    === PHYPayload ===
    ## MHDR        (x40): b01000000
      MType     (b010): Unconfirmed Data Up
      RFU       (b000):
      Major     (b00): LoRaWAN R1
    ## MACPayload
      FHDR          (x2105810080c9fe02a434eaa5f9787f187538d9b054ea0ffc)
        DevAddr     (x21058100): 00810521
        FCtrl       (b10000000): 80
          ADR       : 1
          ADRACKReq : 0
          ACK       : 0
          RFU       : 0
          FOptsLen  : 0
        FCnt        (xc9fe): 65225
    ## FPort       (x02): 2
    ## FRMPayload: a434eaa5f9787f187538d9b054ea0ffc
    ## MIC          : xb67898d4

If the payload include FOpts (MAC Commands), the output will be like below.
You can see a short description of each command.

    % python lrw_phy_parser.py 809a4ed301080200050707030703070308d7bcacbcfa
    === PHYPayload ===
    ## MHDR        (x80): b10000000
      MType     (b100): Confirmed Data Up
      RFU       (b000):
      Major     (b00): LoRaWAN R1
    ## MACPayload
      FHDR          (x9a4ed301080200050707030703070308d7)
        DevAddr     (x9a4ed301): 01d34e9a
        FCtrl       (b00001000): 08
          ADR       : 0
          ADRACKReq : 0
          ACK       : 0
          RFU       : 0
          FOptsLen  : 8
        FCnt        (x0200): 2
        FOpts       (x0507070307030703)
    ## MAC Command (FOpts)
      RXParamSetupAns (uplink) [05] [07]
        RFU: 00000
        RX1DRoffset ACK: 1
         ** Detail : RX2 slot channel was successfully set.
        RX2 Data rate ACK: 1
         ** Detail : RX2 slot data rate was successfully set.
        Channel ACK: 1
         ** Detail : RX1DRoffset was successfully set.
      NewChannelAns (uplink) [07] [03]
        RFU: 000000
        Data rate range ok: 1
         ** Detail : The data rate range is compatible with the possibilities of the end-device.
        Channel frequency ok: 1
         ** Detail : The device is able to use this frequency.
      NewChannelAns (uplink) [07] [03]
        RFU: 000000
        Data rate range ok: 1
         ** Detail : The data rate range is compatible with the possibilities of the end-device.
        Channel frequency ok: 1
         ** Detail : The device is able to use this frequency.
      NewChannelAns (uplink) [07] [03]
        RFU: 000000
        Data rate range ok: 1
         ** Detail : The data rate range is compatible with the possibilities of the end-device.
        Channel frequency ok: 1
         ** Detail : The device is able to use this frequency.
    ## FPort       (x08): 8
    ## FRMPayload: d7
    ## MIC          : xbcacbcfa

In the following case, if anyone know what is wrong, please tell me why ?

The specification said if FPort is zero and FRMPayload exists,
then the FRMPayload should be MAC Commands.
But, actually, not.  See below result.

    % python lrw_phy_parser.py 609a4ed301200100005c511c5fabd96bb2e77728639ae7674880dd1f948163
    === PHYPayload ===
    ## MHDR        (x60): b01100000
      MType     (b011): Unconfirmed Data Down
      RFU       (b000):
      Major     (b00): LoRaWAN R1
    ## MACPayload
      FHDR          (x9a4ed301200100005c511c5fabd96bb2e77728639ae7674880dd)
        DevAddr     (x9a4ed301): 01d34e9a
        FCtrl       (b00100000): 20
          ADR       : 0
          RFU       : 0
          ACK       : 1
          FPending  : 0
          FOptsLen  : 0
        FCnt        (x0100): 1
    ## FPort       (x00): 0
    WARNING: might be violate to the spec.
    ## FRMPayload: 5c511c5fabd96bb2e77728639ae7674880dd
    ## MIC          : x1f948163

