#!/usr/bin/env python

from reg_utils.reg_interface.arm.gbt_utils import programGBT
from time import *
import array
import struct
import os

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: gbt.py <oh_num> <gbt_num> <command>')
        print('available commands:')
        print('  config <config_filename_txt>:   Configures the GBT with the given config file (must use the txt version of the config file, can be generated with the GBT programmer software)')
        print('  v3b-phase-scan <base_config_filename_txt>:   Configures the GBT with the given config file, and performs an elink phase scan while checking the VFAT communication for each phase')
        exit(os.EX_USAGE)
    else:
        ohSelect = int(sys.argv[1])
        gbtSelect = int(sys.argv[2])
        command = sys.argv[3]
    
    if ohSelect > 11:
        printRed("The given OH index (%d) is out of range (must be 0-11)" % ohSelect)
        exit(os.EX_USAGE)
    if gbtSelect > 2:
        printRed("The given GBT index (%d) is out of range (must be 0-2)" % gbtSelect)
        exit(os.EX_USAGE)

    if ohSelect > 11:
        printRed("The given OH index (%d) is out of range (must be 0-11)" % ohSelect)
        exit(os.EX_USAGE)
    if gbtSelect > 2:
        printRed("The given GBT index (%d) is out of range (must be 0-2)" % gbtSelect)
        exit(os.EX_USAGE)

    programGBT(ohSelect, gbtSelect, command)
