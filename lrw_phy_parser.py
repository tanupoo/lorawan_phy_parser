#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

MIC_LEN = 4
MSGDIR_DOWN = "down"
MSGDIR_UP = "up"

'''
a hex string in 1 byte into a binary string in 8 bits.
'''
def hex2bin(x_string):
    return bin(int(x_string, 16))[2:].zfill(8)

'''
MAC Command Parsers
'''
def print_detail(text):
    indent = "     ** Detail :"
    print(indent, text.strip())

def parse_maccmd_ServDev_LoRaWAN_version(x_Dev_LoRaWAN_version):
    b_Dev_LoRaWAN_version = hex2bin(x_Dev_LoRaWAN_version)
    b_Minor = hex2bin(b_Dev_LoRaWAN_version[4:])
    if int(b_Minor, 2) == 1:
        vs = "LoRaWAN x.1"
    else:
        vs = "RFU"
    print("    Dev_LoRaWAN_version: [b%s] [x%s]" % (b_Dev_LoRaWAN_version,
                                                    x_Dev_LoRaWAN_version))
    print("      Minor: %s [b%s]" % (vs, b_Minor))

def parse_maccmd_ResetInd(hex_data):
    print("    IS SUPPORTED BY V1.1 OR LATER.")
    offset = 0
    #
    parse_maccmd_ServDev_LoRaWAN_version(hex_data[offset])
    print_detail("""
This MAC command is only available to ABP devices activated on a LoRaWAN1.1
compatible network server. LoRaWAN1.0 servers do not implement this MAC
command OTA devices MUST NOT implement this command. The network server SHALL
ignore the ResetInd command coming from an OTA device.
With the ResetInd command, an ABP end-device indicates to the network
that it has been re-initialized and
that he has switched back to its default MAC & radio parameters
""")

def parse_maccmd_ResetConf(hex_data):
    print("    IS SUPPORTED BY V1.1 OR LATER.")
    offset = 0
    #
    parse_maccmd_ServDev_LoRaWAN_version(hex_data[offset])
    print_detail("""
The server's version carried by the ResetConf must be the same
than the device's version.  Any other value is invalid.
""")

def parse_maccmd_LinkCheckReq(hex_data):
    # zero length
    pass

def parse_maccmd_LinkCheckAns(hex_data):
    offset = 0
    #
    x_Margin = hex_data[offset]
    i_Margin = int(x_Margin, 16)
    print("    Margin: %d [x%s]" % (i_Margin, x_Margin))
    print_detail("""
The demodulation margin (Margin) is an 8-bit unsigned integer
in the range of 0..254
indicating the link margin in dB of the last successfully
received LinkCheckReq command.
A value of 0 means that the frame was received at the demodulation floor
(0 dB or no 948 margin) 
""")
    offset += 1
    #
    x_GwCnt = hex_data[offset]
    i_GwCnt = int(x_GwCnt, 16)
    print("    GwCnt: %d [x%s]" % (i_GwCnt, x_GwCnt))
    print_detail("""
The gateway count (GwCnt) is the number of gateways that successfully
received the last LinkCheckReq command.
""")

def parse_maccmd_LinkADRReq(hex_data):
    offset = 0
    #
    x_DataRate_TXPower = hex_data[offset]
    b_DataRate_TXPower = hex2bin(x_DataRate_TXPower)
    print("    DataRate_TXPower: [b%s] [x%s]" % (b_DataRate_TXPower,
                                                 x_DataRate_TXPower))
    b_datarate = b_DataRate_TXPower[0:3]
    b_txpower = b_DataRate_TXPower[4:]
    print("      DataRate: %d [b%s]" % (int(b_datarate,2), b_datarate))
    print("      TXPower : %d [b%s]" % (int(b_txpower,2), b_txpower))
    print_detail("""
REGION SPECIFIC.
A value 0xF (15 in decimal format) of either DataRate or TXPower
means that the device MUST
ignore that field, and keep the current parameter value.
""")
    offset += 1
    #
    x_ChMask = "%s%s" % (hex_data[offset], hex_data[offset+1])
    b_ChMask = "%s%s" % (hex2bin(x_ChMask[:2]), hex2bin(x_ChMask[2:]))
    print("    ChMask: [b%s] [b%s] [x%s]" % (b_ChMask[:8], b_ChMask[8:]))
    for i in range(16):
        print("      CH %d : %s" % (i, b_ChMask[i]))
    print_detail("""
The channel mask (ChMask) encodes the channels usable for uplink access.
A bit in the ChMask field set to 1 means that the corresponding channel
can be used for uplink transmissions if this channel allows the data rate
currently used by the end-device.
A bit set to 0 means the corresponding channels should be avoided.
""")
    offset += 2
    #
    x_Redundancy = hex_data[offset]
    b_Redundancy = hex2bin(x_Redundancy)
    print("    Redundancy: [b%s] [x%s]" % (b_Redundancy, x_Redundancy))
    print("      RFU: [b%s]" % Redundancy[0])
    print("      ChMaskCntl: [b%s]" % Redundancy[1:4])
    print_detail("""
REGION SPECIFIC.
The channel mask control (ChMaskCntl) field controls the
interpretation of the previously
defined ChMask bit mask.
""")
    b_NbTrans = Redundancy[4:]
    print("      NbTrans: %d [b%s]" % (int(b_NbTrans,2), b_NbTrans))
    print_detail("""
The NbTrans field is the number of transmissions for each uplink message.
""")

def parse_maccmd_LinkADRAns(hex_data):
    offset = 0
    #
    x_Status = hex_data[offset]
    b_Status = hex2bin(x_Status)
    b_Power_ACK = b_Status[5]
    b_Data_rate_ACK = b_Status[6]
    b_Channel_mask_ACK = b_Status[7]
    print("    Status            : [b%s] [x%s]" % b_Status, x_Status)
    print("      RFU             : [b%s]" % b_Status[0:5])
    print("      Power ACK       : %s" % b_Power_ACK)
    print("      Data_rate_ACK   : %s" % b_Data_rate_ACK)
    print("      Channel_mask_ACK: %s" % b_Channel_mask_ACK)
    if b_Power_ACK == "0":
        print_detail("""
The channel mask sent enables a yet undefined channel or the channel mask
required all channels to be disabled. The command was
discarded and the end- device state was not changed.
""")
    else:
        print_detail("""
The channel mask sent was successfully interpreted. All currently defined
channel states were set according to the mask.
""")
    print("      Data rate ACK:", Status[6])
    if b_Data_rate_ACK == "0":
        print_detail("""
The data rate requested is unknown to the end-device or is
not possible given the channel mask provided (not supported
by any of the enabled channels). The command was discarded
and the end-device state was not changed.
""")
    else:
        print_detail("""
The data rate was successfully set or the DataRate field of
the request was set to 15, meaning it was ignored
""")
    print("      Channel mask ACK:", Status[7])
    if b_Channel_mask_ACK == "0":
        print_detail("""
The device is unable to operate at or below the requested power level.. The
command was discarded and the end-device state was not
changed.
""")
    else:
        print_detail("""
The device is able to operate at or below the requested power level,, or the
TXPower field of the request was set to 15, meaning it
shall be ignored
""")

def parse_maccmd_DutyCycleReq(hex_data):
    offset = 0
    #
    x_DutyCyclePL = hex_data[offset]
    b_DutyCyclePL = hex2bin(x_DutyCyclePL)
    i_MaxDCycle = int(b_DutyCycleP[4:],2)
    print("    DutyCyclePL: [b%s]" % b_DutyCyclePL)
    print("      RFU: [b%s]" % cycle[0:4])
    print("      MaxDCycle: %.2f [b%s]" % (1./i_MaxDCycle, b_DutyCycleP[4:]))
    print_detail("""
A value of 0 corresponds to "no duty cycle limitation"
except the one set by the regional regulation.
""")

def parse_maccmd_DutyCycleAns(hex_data):
    # zero length
    pass

def parse_maccmd_RXParamSetupReq(hex_data):
    offset = 0
    #
    x_DLsettings = hex_data[offset]
    b_DLsettings = hex2bin(x_DLsettings)
    i_RX1DRoffset = int(b_DLsettings[1:4],2)
    print("    DLsettings: [b%s]" % b_DLsettings)
    print("      RFU: [b%s]" % b_DLsettings[0])
    print("      RX1DRoffset: %d [b%s]" % (i_RX1DRoffset, b_DLsettings[1:4]))
    print_detail("""
The RX1DRoffset field sets the offset between the uplink data
rate and the downlink data
rate used to communicate with the end-device on the first
reception slot (RX1). As a default
this offset is 0. The offset is used to take into account
maximum power density constraints
for base stations in some regions and to balance the
uplink and downlink radio link margins.
""")
    i_RX2DataRate = int(b_DLsettings[4:],2)
    print("      RX2DataRate: %d [b%s]" % (i_RX2DataRate, DLsettings[4:]))
    print_detail("""
The RX2DataRate field defines the data rate of a downlink using the second
receive window following the same convention as the
LinkADRReq command (0 means DR0/125kHz for example).
""")
    offset += 1
    #
    x_Frequency = ''.join(hex_data[offset:offset+3])
    print("    Frequency: [x%s]" % x_Frequency) 
    print_detail("""
The frequency (Frequency) field corresponds to the frequency of
the channel used for the second receive window, whereby
the frequency is coded following
the convention defined in the NewChannelReq command.
""")
    # XXX needs to be parsed Frequency

def parse_maccmd_RXParamSetupAns(hex_data):
    offset = 0
    #
    x_Status = hex_data[offset]
    b_Status = hex2bin(x_Status)
    b_RX1DRoffset_ACK = b_Status[5]
    b_RX2Datarate_ACK = b_Status[6]
    b_Channel_ACK = b_Status[7]
    print("    RFU: [b%s]" % b_Status[0:5])
    print("    RX1DRoffset ACK: %s" % b_RX1DRoffset_ACK)
    if b_RX1DRoffset_ACK == "0":
        print_detail("""
the uplink/downlink data rate offset for RX1 slot is not in the allowed range.
""")
    else:
        print_detail("""
RX1DRoffset was successfully set.
""")
    print("    RX2 Data rate ACK: %s" % b_RX2Datarate_ACK)
    if b_RX2Datarate_ACK == "0":
        print_detail("""
The data rate requested is unknown to the end-device.
""")
    else:
        print_detail("""
RX2 slot channel was successfully set.
""")
    print("    Channel ACK:", Status[7])
    if b_Channel_ACK == "0":
        print_detail("""
The frequency requested is not usable by the end-device.
""")
    else:
        print_detail("""
RX2 slot channel was successfully set.
""")

def parse_maccmd_DevStatusReq(hex_data):
    # zero length
    pass

def parse_maccmd_DevStatusAns(hex_data):
    offset = 0
    #
    Battery = int(hex_data[offset], 16)
    print("    Battery: %d (%s)" % (Battery, hex_data[offset]))
    if Battery == 255:
        print_detail("""
The end-device was not able to measure the battery level.
""")
    elif Battery == 0:
        print_detail("""
The end-device is connected to an external power source.
""")
    offset += 1
    Margin = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    Bargin: (%s)" % (hex_data[offset]))
    print("      RFU:", Margin[0:2])
    print("      Margin:", Margin[2:])
    print_detail("""
The margin (Margin) is the demodulation signal-to-noise ratio in dB rounded to
the nearest integer value for the last successfully received
DevStatusReq command. It is a signed
integer of 6 bits with a minimum value of -32
and a maximum value of 31.
""")

def parse_maccmd_NewChannelReq(hex_data):
    offset = 0
    #
    ChIndex = int(hex_data[offset], 16)
    print_detail("""
The channel index (ChIndex) is the index of the channel being
created or modified.
Depending on the region and frequency band used, the LoRaWAN specification imposes
default channels which must be common to all
devices and cannot be modified by the NewChannelReq command (cf. Chapter 6).
If the number of default channels is N, the default channels go from 0 to N-1,
and the acceptable range for ChIndex is N to 15.
A device must be able to handle at least 16
different channel definitions. In certain region
the device may have to store more than 16 channel definitions.
""")
    offset += 1
    #
    Freq = int(hex_data[offset], 16)
    print_detail("""
The frequency (Freq) field is a 24 bits unsigned integer. The actual channel
frequency in Hz
is 100 x Freq whereby values representing
frequencies below 100 MHz are reserved for
future use. This allows setting the frequency of
a channel anywhere between 100 MHz to
1.67 GHz in 100 Hz steps. A Freq value of 0
disables the channel. The end-device has to
check that the frequency is actually allowed by
its radio hardware and return an error
otherwise.
""")
    offset += 3
    #
    DrRange = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    DrRange: %s" % (hex_data[offset]))
    print("      MaxDR: ", DrRange[0:4])
    print("      MinDR: ", DrRange[4:])
    print_detail("""
the minimum data rate (MinDR) subfield
designate the lowest uplink data rate allowed on
this channel. For example 0 designates
DR0 / 125 kHz. Similarly, the maximum data rate
(MaxDR) designates the highest uplink
data rate. For example, DrRange = 0x77 means
that only 50 kbps GFSK is allowed on a
channel and DrRange = 0x50 means that DR0 / 125
kHz to DR5 / 125 kHz are supported.
""")

def parse_maccmd_NewChannelAns(hex_data):
    offset = 0
    #
    Status = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", Status[0:6])
    print("    Data rate range ok:", Status[6])
    if Status[6] == "0":
        print_detail("""
The designated data rate range exceeds the ones currently defined for this end-
device.
""")
    else:
        print_detail("""
The data rate range is compatible with the possibilities of the end-device.
""")
    print("    Channel frequency ok:", Status[7])
    if Status[7] == "0":
        print_detail("""
The device cannot use this frequency.
""")
    else:
        print_detail("""
The device is able to use this frequency.
""")

def parse_maccmd_RXTimingSetupReq(hex_data):
    offset = 0
    #
    Settings = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", Status[0:4])
    print("    Delay:", Status[4:])
    print_detail("""
The delay (Delay) field specifies the delay in second.
the value of 0 and 1 indicates 1 (s).
the value of 15 indicates 15 (s).
""")

def parse_maccmd_RXTimingSetupAns(hex_data):
    # zero length
    pass

def parse_maccmd_TxParamSetupReq(hex_data):
    offset = 0
    #
    DwellTime = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", DwellTime[0:2])
    print("    DownlinkDwellTime:", DwellTime[2])
    print("    UplinkDwellTime:", DwellTime[3])
    print("    MaxEIRP:", DwellTime[4:])

def parse_maccmd_TxParamSetupAns(hex_data):
    # zero length
    pass

def parse_maccmd_DlChannelReq(hex_data):
    offset = 0
    #
    ChIndex = int(hex_data[offset], 16)
    print_detail("""
The channel index (ChIndex) is the index of the
channel whose downlink frequency is
modified.
""")
    offset += 1
    #
    Freq = int(hex_data[offset], 16)
    print_detail("""
The frequency (Freq) field is a 24 bits unsigned integer. The actual downlink
frequency in Hz
is 100 x Freq whereby values representing
frequencies below 100 MHz are reserved for
future use. The end-device has to check that the
frequency is actually allowed by its radio
hardware and return an error otherwise.
""")

def parse_maccmd_DlChannelAns(hex_data):
    offset = 0
    #
    Status = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    RFU:", Status[0:6])
    print("    Uplink frequency exists:", Status[6])
    if Status[6] == "0":
        print_detail("""
The uplink frequency is not defined for this channel, the downlink frequency
can only be set for a channel that already has
a valid uplink frequency
""")
    else:
        print_detail("""
The uplink frequency of the channel is valid.
""")
    print("    Channel frequency ok:", Status[7])
    if Status[7] == "0":
        print_detail("""
The device cannot use this frequency.
""")
    else:
        print_detail("""
The device is able to use this frequency.
""")

#
# Class B Mac Command Parsers
#
def parse_maccmd_PingSlotInfoReq(hex_data):
    offset = 0
    #
    period = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    PingSlotParam:", hex_data[offset])
    print("      RFU:", period[0:4])
    print("      Periodicity:", period[5:7])
    print_detail("""
Periodicity = 0 means that the end-device opens a ping slot every second.
Periodicity = 7, every 128 seconds which is the
maximum ping period supported by the LoRaWAN Class B specification.
""")

def parse_maccmd_PingSlotInfoAns(hex_data):
    # zero length
    pass

def parse_maccmd_PingSlotChannelReq(hex_data):
    print("    NOT YET IMPLEMENTED.")

def parse_maccmd_PingSlotChannelAns(hex_data):
    print("    NOT YET IMPLEMENTED.")

def parse_maccmd_BeaconTimingReq(hex_data):
    print("    DEPRECATED.")

def parse_maccmd_BeaconTimingAns(hex_data):
    print("    DEPRECATED.")

def parse_maccmd_BeaconFreqReq(hex_data):
    Freq = int(hex_data[offset], 16)
    print_detail("""
Frequency is a 24bits unsigned integer. The actual beacon
channel frequency in Hz is 100 x frequ. This allows defining
the beacon channel anywhere between 100 MHz to 1.67 GHz
by 100 Hz step. The end-device has to check that the frequency
is actually allowed by its radio hardware and return an error otherwise.
A valid non-zero Frequency will force the device to listen
to the beacon on a fixed frequency channel even if the default
behavior specifies a frequency hopping beacon (i.e US ISM band).
A value of 0 instructs the end-device to use the default
beacon frequency plan as defined in the "Beacon physical layer" section.
Where applicable the device resumes frequency hopping beacon search.
""")

def parse_maccmd_BeaconFreqAns(hex_data):
    offset = 0
    #
    status = bin(int(hex_data[offset], 16))[2:].zfill(8)
    print("    Status:", hex_data[offset])
    print("      RFU:", status[0:6])
    print("      Beacon frequency ok:", period[6:7])
    print_detail("""
Bit=0: The device cannot use this frequency, the previous beacon frequency is
kept.
Bit=1: The beacon frequency has been changed
""")

#
# Class C Mac Command Parsers
#
def parse_maccmd_DeviceModeInd(hex_data):
    print("    NOT YET IMPLEMENTED.")

def parse_maccmd_DeviceModeConf(hex_data):
    print("    NOT YET IMPLEMENTED.")

'''
Table for MAC Command Parser
    name: MAC command name
    size: content size in size.
    parser: function name.
'''
mac_cmd_tab = {
    #
    # Class A Mac Command
    #
    "01": {
        MSGDIR_UP: {
            "name": "ResetInd",
            "size": 1,
            "parser": parse_maccmd_ResetInd
        },
        MSGDIR_DOWN: {
            "name": "ResetConf",
            "size": 1,
            "parser": parse_maccmd_ResetConf
        }
    },
    "02": {
        MSGDIR_UP: {
            "name": "LinkCheckReq",
            "size": 0,
            "parser": parse_maccmd_LinkCheckReq
        },
        MSGDIR_DOWN: {
            "name": "LinkCheckAns",
            "size": 2,
            "parser": parse_maccmd_LinkCheckAns
        }
    },
    "03": {
        MSGDIR_UP: {
            "name": "LinkADRAns",
            "size": 1,
            "parser": parse_maccmd_LinkADRAns
        },
        MSGDIR_DOWN: {
            "name": "LinkADRReq",
            "size": 4,
            "parser": parse_maccmd_LinkADRReq
        }
    },
    "04": {
        MSGDIR_UP: {
            "name": "DutyCycleAns",
            "size": 0,
            "parser": parse_maccmd_DutyCycleAns
        },
        MSGDIR_DOWN: {
            "name": "DutyCycleReq",
            "size": 1,
            "parser": parse_maccmd_DutyCycleReq
        }
    },
    "05": {
        MSGDIR_UP: {
            "name": "RXParamSetupAns",
            "size": 1,
            "parser": parse_maccmd_RXParamSetupAns
        },
        MSGDIR_DOWN: {
            "name": "RXParamSetupReq",
            "size": 4,
            "parser": parse_maccmd_RXParamSetupReq
        }
    },
    "06": {
        MSGDIR_UP: {
            "name": "DevStatusAns",
            "size": 2,
            "parser": parse_maccmd_DevStatusAns
        },
        MSGDIR_DOWN: {
            "name": "DevStatusReq",
            "size": 0,
            "parser": parse_maccmd_DevStatusReq
        }
    },
    "07": {
        MSGDIR_UP: {
            "name": "NewChannelAns",
            "size": 1,
            "parser": parse_maccmd_NewChannelAns
        },
        MSGDIR_DOWN: {
            "name": "NewChannelReq",
            "size": 5,
            "parser": parse_maccmd_NewChannelReq
        }
    },
    "08": {
        MSGDIR_UP: {
            "name": "RXTimingSetupAns",
            "size": 0,
            "parser": parse_maccmd_RXTimingSetupAns
        },
        MSGDIR_DOWN: {
            "name": "RXTimingSetupReq",
            "size": 1,
            "parser": parse_maccmd_RXTimingSetupReq
        }
    },
    "09": {
        MSGDIR_UP: {
            "name": "TxParamSetupAns",
            "size": 0,
            "parser": parse_maccmd_TxParamSetupAns
        },
        MSGDIR_DOWN: {
            "name": "TxParamSetupReq",
            "size": 1,
            "parser": parse_maccmd_TxParamSetupReq
        }
    },
    "0a": {
        MSGDIR_UP: {
            "name": "DlChannelAns",
            "size": 1,
            "parser": parse_maccmd_DlChannelAns
        },
        MSGDIR_DOWN: {
            "name": "DlChannelReq",
            "size": 4,
            "parser": parse_maccmd_DlChannelReq
        }
    },
    #
    # Class B Mac Command
    #
    "10": {
        MSGDIR_UP: {
            "name": "PingSlotInfoReq",
            "size": 1,
            "parser": parse_maccmd_PingSlotInfoReq
        },
        MSGDIR_DOWN: {
            "name": "PingSlotInfoAns",
            "size": 0,
            "parser": parse_maccmd_PingSlotInfoAns
        }
    },
    "11": {
        MSGDIR_UP: {
            "name": "PingSlotChannelAns",
            "size": 4,
            "parser": parse_maccmd_PingSlotChannelAns
        },
        MSGDIR_DOWN: {
            "name": "PingSlotChannelReq",
            "size": 1,
            "parser": parse_maccmd_PingSlotChannelReq
        }
    },
    "12": {
        MSGDIR_UP: {
            "name": "BeaconTimingReq",
            "size": 3,
            "parser": parse_maccmd_BeaconTimingReq
        },
        MSGDIR_DOWN: {
            "name": "BeaconTimingAns",
            "size": 0,
            "parser": parse_maccmd_BeaconTimingAns
        }
    },
    "13": {
        MSGDIR_UP: {
            "name": "BeaconFreqAns",
            "size": 1,
            "parser": parse_maccmd_BeaconFreqAns
        },
        MSGDIR_DOWN: {
            "name": "BeaconFreqReq",
            "size": 3,
            "parser": parse_maccmd_BeaconFreqReq
        }
    },
    #
    # Class C Mac Command
    #
    "20": {
        MSGDIR_UP: {
            "name": "DeviceModeInd",
            "size": 1,
            "parser": parse_maccmd_DeviceModeInd
        },
        MSGDIR_DOWN: {
            "name": "DeviceModeConf",
            "size": 1,
            "parser": parse_maccmd_DeviceModeConf
        }
    }
    }

def parse_mac_cmd(msg_dir, hex_data):
    offset = 0
    n_maccmd = 0
    while offset < len(hex_data):
        cid = hex_data[offset]
        a = mac_cmd_tab.has_key(cid)
        if a:
            t = mac_cmd_tab[cid][msg_dir]
            offset += 1
            n_maccmd += 1
            if t["size"] == 0:
                print("  %02d. %s (x%s %slink)" % (n_maccmd, t["name"],
                                                   cid, msg_dir))
            else:
                print("  %02d. %s (x%s %slink) [%s]" % (
                        n_maccmd, t["name"], cid, msg_dir,
                        ''.join(hex_data[offset:offset+t["size"]])))
            t["parser"](hex_data[offset:])
            offset += t["size"]
        else:
            print("ERROR: Proprietary MAC command [%s] has been found." %
                  hex_data[offset])
            raise("")

'''
MHDR parser
    7 6 5 | 4 3 2 |  1 0
    MType |  RFU  | Major
'''
def get_mtype_cmd(mtype):
    return {
        "000": "Join Request",
        "001": "Join Accept",
        "010": "Unconfirmed Data Up",
        "011": "Unconfirmed Data Down",
        "100": "Confirmed Data Up",
        "101": "Confirmed Data Down",
        "110": "RFU",
        "111": "Proprietary"
        }[mtype]

def get_major(major):
    return {
        "00": "LoRaWAN R1",
        "01": "RFU",
        "10": "RFU",
        "11": "RFU"
        }[major]

def parse_mhdr(hex_data):
    mhdr = hex_data[0]
    mhdr_bin = bin(int(mhdr, 16))[2:].zfill(8)
    mtype = mhdr_bin[0:3]
    mtype_cmd = get_mtype_cmd(mtype)
    mhdr_rfu = mhdr_bin[3:6]
    major = mhdr_bin[6:]
    print("## MHDR           [x%s] [b%s]" % (mhdr, mhdr_bin))
    print("  MType         : %s [b%s]" % (get_mtype_cmd(mtype), mtype))
    print("  RFU           : [b%s]" % mhdr_rfu)
    print("  Major         : %s [b%s]" % (get_major(major), major))
    #
    return mtype

'''
MACPayload parser

- MACPayload
    FHDR | FPort | FRMPayload

- FHDR
       4    |   1   |   2  | 0...15
    DevAddr | FCtrl | FCnt | FOpts

- FCtrl for downlink
     7  |    6   |  5  |    4     |   3...0
    ADR |   RFU  | ACK | FPending | FOptsLen

- FCtrl for uplink
     7  |    6   |  5  |    4     |   3...0
        |   ADR  |     |  RFT or  |
    ADR | ACKReq | ACK | Class B  | FOptsLen
'''
def parse_mac_payload(msg_dir, hex_data):
    devaddr = ''.join(hex_data[0:4][::-1])
    fctrl = hex_data[4]
    fctrl_bin = bin(int(fctrl, 16))[2:].zfill(8)
    print("  FHDR            [x%s]" % (''.join(hex_data)))
    print("    DevAddr     : %s [x%s]" % (devaddr, ''.join(hex_data[:4])))
    print("    FCtrl       : [x%s] [b%s]" % (fctrl, fctrl_bin))
    #
    adr = int(fctrl_bin[0:1])
    print("      ADR       : %d" % adr)
    if msg_dir == MSGDIR_DOWN:
        fctrl_rfu = fctrl_bin[1:2]
        ack = int(fctrl_bin[2:3])
        fpending = int(fctrl_bin[3:4])
        print("      RFU       : %s" % fctrl_rfu)
        print("      ACK       : %d" % ack)
        print("      FPending  : %d" % fpending)
    else:
        adrackreq = int(fctrl_bin[1:2])
        ack = int(fctrl_bin[2:3])
        fctrl_rfu_classb = int(fctrl_bin[3:4])
        print("      ADRACKReq : %d" % adrackreq)
        print("      ACK       : %d" % ack)
        print("      RFU/ClsB  : %d" % fctrl_rfu_classb)
    #
    foptslen = int(fctrl_bin[4:], 2)
    fcnt = int(''.join(hex_data[5:7][::-1]), 16)
    print("      FOptsLen  : %d [b%s]" % (foptslen, fctrl_bin[4:]))
    print("    FCnt        : %d [x%s]" % (fcnt, ''.join(hex_data[5:7])))

    '''
## FOptsLen, FOpts, FPort, FRMPayload

4.3.1.6 Frame options (FOptsLen in FCtrl, FOpts)
If FOptsLen is 0, the FOpts field is absent.
If FOptsLen is different from 0,
i.e. if MAC commands are present in the FOpts field, the port 0 cannot be used
(FPort must be either not present or different from 0).

MAC commands cannot be simultaneously present in the payload field and the frame
options field. Should this occur, the device shall ignore the frame.

4.3.2 Port field (FPort)
If the frame payload field is not empty, the port field must be present
If present, an FPort value of 0 indicates that the FRMPayload contains MAC commands

5 MAC Commands
A single data frame can contain any sequence of MAC commands, either piggybacked
in the FOpts field or, when sent as a separate data frame, in the FRMPayload field
with the FPort field being set to 0.
Piggybacked MAC commands are always sent without encryption and
must not exceed 15 octets. MAC commands sent as FRMPayload are always
encrypted and must not exceed the maximum FRMPayload length.

## Pseudo code

    #
    if foptslen is 0:
        fopts is None
    else:
        fopts is not None
    #
    if rest_len is 0:
        fport is None
    else:
        if fport == 0:
            if foptslen is not 0:
                ERROR
            else:
                FRMPayload is MACCommand.
        else:
            FRMPayload is a message.
    '''
    #
    fopts_offset = 7  # the index of the FOpts start.
    offset = fopts_offset
    fopts = None
    fport = None
    if foptslen:
        offset += foptslen
        fopts = hex_data[fopts_offset:offset]
        print("    FOpts         [x%s]" % (''.join(fopts)))
        print("## MAC Command (No. CMD (CID DIR) [MSG])")
        parse_mac_cmd(msg_dir, fopts)
    rest_len = len(hex_data[offset:])
    if rest_len:
        fport = hex_data[offset]
        print("## FPort        : %d [x%s]" % (int(fport, 16), fport))
        offset += 1
        rest_len -= 1
        if int(fport) == 0:
            if foptslen:
                print("ERROR: MAC Command is in both FOpts and FRMPayload.")
                raise("")
            # XXX
            # Here the spec in the section 5 said the FRMPayload must be MAC Commands.
            # But, there seems some devices use an app message with port 0.
            # So, currently, we don't parse it as MAC Commands.
            #
            #print("=== MAC Command (FRMPayload) ===")
            #parse_mac_cmd(msg_dir, hex_data[offset:])
            #
            print("WARNING: might be violate to the spec.")
            return rest_len
        elif int(fport) == "224":
            print("=== MAC Command test ===")
            return 0
        else:
            return rest_len
    #
    return 0

'''
JoinReq parser

      8    |   8    |    2
    AppEUI | DevEUI | DevNonce

'''
def parse_joinreq(hex_data):
    appeui = hex_data[0:8][::-1]
    deveui = hex_data[8:16][::-1]
    devnonce = hex_data[16:18]  # XXX little endian ?
    print("  AppEUI        (x%s): %s" % (''.join(appeui[::-1]), ''.join(appeui)))
    print("  DevEUI        (x%s): %s" % (''.join(deveui[::-1]), ''.join(deveui)))
    print("  DevNonce      (x%s): %s" % (''.join(devnonce),
                                         ''.join(devnonce[::-1])))

'''
JoinRes parser

        3    |   3   |    4    |     1      |    1    |  (16)
    AppNonce | NetID | DevAddr | DLSettings | RxDelay | (CFList)

'''
def parse_joinres(hex_data):
    # XXX endian check is not yet ?
    appnonce = hex_data[0:3]
    netid = hex_data[3:6]
    devaddr = hex_data[6:10]
    DLSettings = hex_data[10]
    RxDelay = hex_data[11]
    print("  AppNonce      : x%s" % (''.join(appnonce)))
    print("  NetID         : x%s" % (''.join(netid)))
    print("  DevAddr       : x%s" % (''.join(devaddr)))
    print("  DLSettings    : x%s" % (DLSettings))
    print("  RxDelay       : x%s" % (RxDelay))
    print("WARNING: not all implemented yet.")

'''
PHYPayload parser

      1  |    1...M   |  4
    MHDR | MACPayload | MIC
    MHDR |   JoinReq  | MIC
    MHDR |   JoinRes  | MIC
'''
def parse_phy_payload(hex_data):
    print("=== PHYPayload ===")
    print("[x %s]" % ' '.join(hex_data))
    # payload: i.e. MACPayload, Join Req, JoinRes
    payload_len = len(hex_data) - MIC_LEN
    payload = hex_data[1:payload_len]
    mic = hex_data[-MIC_LEN:]
    #
    mtype = parse_mhdr(hex_data)
    #
    msg_dir = MSGDIR_UP
    if mtype in [ "000", "011", "101" ]:
        msg_dir = MSGDIR_DOWN
    #
    if mtype == "000":
        print("## JoinReq")
        parse_joinreq(payload)
    elif mtype == "001":
        print("## JoinRes")
        parse_joinres(payload)
    else:
        print("## MACPayload")
        rest_len = parse_mac_payload(msg_dir, payload)
        if rest_len:
            print("## FRMPayload   :", ''.join(payload[-rest_len:]))
    #
    print("## MIC          : x%s" % (''.join(mic))) # XXX endian ?


def hexstr2array(hexstr):
    return [ hexstr[i:i+2] for i in range(0,len(hexstr),2) ]

def test_regress():
    v = [
        "402105810080160102a6bf4432169ea0784416868d9420dd244619443e",
        "40C1D25201A5050003070703120864FE226A9E"
        ]
    for d in v:
        parse_phy_payload(hexstr2array(d))
    exit(1)

'''
test code
'''
if __name__ == '__main__' :
    if len(sys.argv) == 1:
        hex_data = sys.stdin.readline().strip()
    elif sys.argv[1] in ["-h", "--help"]:
        print("Usage: %s (hex)" % (sys.argv[0]))
        print("    You can use stdin to pass the hex string as well.")
        exit(1)
    elif sys.argv[1] == "test":
        test_regress()
        exit(1)
    else:
        hex_data = ''.join(sys.argv[1:])
    parse_phy_payload(hexstr2array(hex_data))

