from print_utils import *
from bit_utils import *
from reg_xml_parser import parseInt, getNode
from reg_base_ops import readReg, writeReg

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

