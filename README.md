# PYTICC
Python module to interface with Texas Instruments CC1xxx Sub-1Ghz RF transceivers over SPI.

## Supported Models
 - CC1101

## Installation
```
pip install pyticc
```

## Basic usage
```
from pyticc.cc1101 import CC1101

cc = CC1101()
cc.sanity_check()
cc.recv_data()
```

## Command Strobes
```
cc.reset()
cc.power_down()
cc.sidle()
cc.enable_rx()
cc.enable_tx()
cc.wor_on()
cc.sx_off()
cc.calibrate()
cc.flush_rx_fifo()
cc.flush_tx_fifo()
```

## Convenience config methods (get or set)
```
cc.base_frequency(433)
cc.modulation('OOK')
cc.packet_length('PKT_LEN_VARIABLE')
cc.rx_bandwidth(325000)
cc.sync_word('FAFA')
cc.manchester(1)
cc.whitening(1)
```

## Read and write raw bytes to register
```
byte = cc.read_byte(0x10)
cc.write_byte('MDMCFG4', byte)
```

## Easy querying and modification of config register attributes
Query by address, or class attribute name.
```
cc.register_value(0x10)
{
  'CHANBW_E[1:0]': 1,
  'CHANBW_M[1:0]': 3,
  'DRATE_E[3:0]': 8
}

cc.register_write('MDMCFG4', 'CHANBW_M[1:0]', 0x02)

cc.register_write('MDMCFG4', 'CHANBW_M[1:0]', '101')
```

## To Do
 - Add more CCxxxx models.
 - JSON config dump/load would be cool.

## CONTACT
Jeff Leary
sillymonkeysoftware@gmail.com
