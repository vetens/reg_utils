from reg_xml_parser import getNode, parseInt, parseXML
from reg_base_ops import *
from print_utils import *
from bit_utils import *
from jtag import *
from virtex6 import *
import gpio as gpio
from sca_common_utils import *
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

def getOHlist(ohMask):
    ohList = []
    for i in range(0,12):
        if check_bit(ohMask, i):
            ohList.append(i)
    return ohList

def sendScaCommand(ohList, sca_channel, sca_command, data_length, data, doRead):
    #print('fake send: channel ' + hex(sca_channel) + ', command ' + hex(sca_command) + ', length ' + hex(data_length) + ', data ' + hex(data) + ', doRead ' + str(doRead))
    #return    

    d = data

    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_CHANNEL'), sca_channel)
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_COMMAND'), sca_command)
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_LENGTH'), data_length)
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_DATA'), d)
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_CMD.SCA_CMD_EXECUTE'), 0x1)
    reply = []
    if doRead:
        for i in ohList:
            reply.append(parseInt(readReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.SCA_REPLY_OH%d.SCA_RPY_DATA' % i))))
    return reply

def checkStatus(ohList):
    rxReady       = parseInt(readReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.STATUS.READY')))
    criticalError = parseInt(readReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.STATUS.CRITICAL_ERROR')))
    statusGood = True
    for i in ohList:
        if not check_bit(rxReady, i):
            printRed("OH #%d is not ready: RX ready = %d, critical error = %d" % (i, (rxReady >> i) & 0x1, (criticalError >> i) & 0x1))
            statusGood = False
    return statusGood

