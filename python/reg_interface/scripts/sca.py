#!/usr/bin/env python

from reg_interface.common.reg_xml_parser import getNode, parseInt
from reg_interface.common.reg_base_ops import *
from reg_interface.common.print_utils import *
from reg_interface.common.jtag import *
from reg_interface.common.virtex6 import *
from reg_interface.common.sca_utils import *
import reg_interface.common.gpio as gpio
from time import *
import array
import struct
import socket

def sca_reset(ohList):
    subheading('Reseting the SCA')
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.CTRL.MODULE_RESET'), 0x1)
    checkStatus(ohList)

def fpga_single_hard_reset():
    subheading('Issuing FPGA Hard Reset')
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.CTRL.OH_FPGA_HARD_RESET'), 0x1)

def fpga_keep_hard_reset(ohList):
    subheading('Disabling monitoring')
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.ADC_MONITORING.MONITORING_OFF'), 0xffffffff)
    sleep(0.01)
    subheading('Asserting FPGA Hard Reset (and keeping it in reset)')
    sendScaCommand(ohList, 0x2, 0x10, 0x4, 0x0, False)

def read_fpga_id(ohMask):
    enableJtag(ohMask)
    ohList = getOHlist(ohMask)
    errors = 0
    timeStart = clock()
    for i in range(0,1):
        value = jtagCommand(True, Virtex6Instructions.FPGA_ID, 10, 0x0, 32, ohList)
        for oh in ohList:
            print(('OH #%d FPGA ID= ' % oh) + hex(value[oh]))
            if value[oh] != VIRTEX6_FPGA_ID:
                errors += 1
    
    totalTime = clock() - timeStart
    printCyan('Num errors = ' + str(errors) + ', time took = ' + str(totalTime))
    disableJtag()

def run_sysmon(ohMask):
    enableJtag(ohMask, 2)
    ohList = getOHlist(ohMask)
    try:
        while True:
            jtagCommand(True, Virtex6Instructions.SYSMON, 10, 0x04000000, 32, False)
            adc1 = jtagCommand(False, None, 0, 0x04010000, 32, ohList)
            adc2 = jtagCommand(False, None, 0, 0x04020000, 32, ohList)
            adc3 = jtagCommand(False, None, 0, 0x04030000, 32, ohList)
            jtagCommand(True, Virtex6Instructions.BYPASS, 10, None, 0, False)
        
            for oh in ohList:
                coreTemp = ((adc1[oh] >> 6) & 0x3FF) * 503.975 / 1024.0-273.15
                volt1 = ((adc2[oh] >> 6) & 0x3FF) * 3.0 / 1024.0
                volt2 = ((adc3[oh] >> 6) & 0x3FF) * 3.0 / 1024.0
        
                #printCyan('adc1 = ' + hex(adc1) + ', adc2 = ' + hex(adc2) + ', adc3 = ' + hex(adc3))
                printCyan(('=== OH #%d ===' % oh) + 'Core temp = ' + str(coreTemp) + ', voltage #1 = ' + str(volt1) + ', voltage #2 = ' + str(volt2))
        
            sleep(0.5)
    except KeyboardInterrupt:
        printMagenta("Interrupting SysMon") 
    disableJtag()

def test1():
    timeStart = clock()
    nn = getNode('GEM_AMC.SLOW_CONTROL.SCA.JTAG.TDI')
    for i in range(0,1000000):
        #print(str(i))
        #writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD_CHANNEL'), 0x02)
        #writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD_COMMAND'), 0x10)
        #writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD_LENGTH'), 0x4)
        #writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD_DATA'), 0x0)
        #readReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.JTAG.TDI'))
        wReg(ADDR_JTAG_TMS, 0x00000000)
        #sleep(0.01)
        #print('execute')
        #writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD_EXECUTE'), 0x1)          
    totalTime = clock() - timeStart
    printCyan('time took = ' + str(totalTime))

def test2():
    timeStart = clock()                                                              
    nn = getNode('GEM_AMC.SLOW_CONTROL.SCA.JTAG.TDI')                                
    for i in range(0,10000):
        print(str(i))
        sleep(0.001)
        writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.FPGA_HARD_RESET'), 0x1)

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
