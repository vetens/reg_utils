#!/usr/bin/env python

from reg_interface.common.reg_xml_parser import getNode, parseInt, parseXML
from reg_interface.common.reg_base_ops import *
from reg_interface.common.print_utils import *
from reg_interface.common.bit_utils import *
from reg_interface.common.jtag import initJtagRegAddrs
from reg_interface.common.sca_utils import *
from reg_interface.common.sca_common_utils import *
from time import *
import array
import struct
import socket

def main():

    instructions = ""
    ohMask = 0
    ohList = []

    if len(sys.argv) < 4:
        print('Usage: sca.py <card_name> <oh_mask> <instructions>. If running on the card, put `local` instead of hostname')
        print('instructions:')
        print('  r:        SCA reset will be done')
        print('  h:        FPGA hard reset will be done')
        print('  hh:       FPGA hard reset will be asserted and held')
        print('  fpga-id:  FPGA ID will be read through JTAG')
        print('  sysmon:   Read FPGA sysmon data repeatedly')
        print('  program-fpga:   Program OH FPGA with a bitfile or an MCS file. Requires a parameter "bit" or "mcs" and a filename')
        return
    else:
        ohMask = parseInt(sys.argv[2])
        ohList = getOHlist(ohMask)
        instructions = sys.argv[3]

    parseXML()
    hostname = socket.gethostname()
    if 'eagle' in hostname:
        pass
    else:
        rpc_connect(sys.argv[1])
    initJtagRegAddrs()

    heading("Hola, I'm SCA controller tester :)")

    if not checkStatus(ohList):
        if not 'r' in instructions:
            exit()

    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.LINK_ENABLE_MASK'), ohMask)

    if instructions == 'r':
        sca_reset(ohList)
    elif instructions == 'hh':
        fpga_keep_hard_reset(ohList)
    elif instructions == 'h':
        fpga_single_hard_reset()
    elif instructions == 'fpga-id':
        read_fpga_id(ohMask)

    elif instructions == 'sysmon':
        run_sysmon(ohMask)

    elif instructions == 'program-fpga':
        hostname = socket.gethostname()
        if 'eagle' in hostname:
            from reg_interface.arm.program_fpga import program_fpga
        else:
            printRed("This method should only be called from the card!!")
            return
        if len(sys.argv) < 5:
            printRed('Usage: sca.py local program-fpga <file-type> <filename>')
            printRed('file-type can be "mcs" or "bit"')
            return

        ftype = sys.argv[4]
        filename = sys.argv[5]
        program_fpga(ohMask,ftype,filename)

    elif instructions == 'test1':
        test1()
        
    elif instructions == 'test2':
        test2()

    elif instructions == 'compare-mcs-bit':
        if len(sys.argv) < 5:
            print("Usage: sca.py local compare-mcs-bit <mcs_filename> <bit_filename>")
            return
        mcsFilename = sys.argv[3]
        bitFilename = sys.argv[4]
        compare_mcs_bit(mcsFilename, bitFilename)

    elif instructions == 'gpio-set-direction':
        if len(sys.argv) < 4:
            print('Usage: sca.py local gpio-set-direction <direction-mask>')
            print('direction-mask is a 32 bit number where each bit represents a GPIO channel -- if a given bit is high it means that this GPIO channel will be set to OUTPUT mode, and otherwise it will be set to INPUT mode')
            return
        directionMask = parseInt(sys.argv[3])
        gpio.set_direction(ohMask,directionMask)

    elif instructions == 'gpio-set-output':
        if len(sys.argv) < 4:
            print('Usage: sca.py local gpio-set-output <output-data>')
            print('output-data is a 32 bit number representing the 32 GPIO channels state')
            return
        outputData = parseInt(sys.argv[3])
        gpio.set_output(ohMask,outputData)

    elif instructions == 'gpio-read-input':
        gpio.read_input(ohMask)
 
if __name__ == '__main__':
    main()
