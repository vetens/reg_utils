from reg_xml_parser import getNode
from reg_base_ops import writeReg
from print_utils import *
from bit_utils import hex
from sca_common_utils import getOHlist, sendScaCommand
from time import sleep

def set_direction(ohMask, directionMask):
    subheading('Disabling monitoring')
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.ADC_MONITORING.MONITORING_OFF'), 0xffffffff)
    sleep(0.01)
    ohList = getOHlist(ohMask)
    subheading('Setting the GPIO direction mask to ' + hex(directionMask))
    sendScaCommand(ohList, 0x2, 0x20, 0x4, directionMask, False)
 
def set_output(ohMask, outputData):
    subheading('Disabling monitoring')
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.ADC_MONITORING.MONITORING_OFF'), 0xffffffff)
    sleep(0.01)
    ohList = getOHlist(ohMask)
    subheading('Setting the GPIO output to ' + hex(outputData))
    sendScaCommand(ohList, 0x2, 0x10, 0x4, outputData, False)

def read_input(ohMask):
    subheading('Disabling monitoring')
    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.ADC_MONITORING.MONITORING_OFF'), 0xffffffff)
    sleep(0.01)
    ohList = getOHlist(ohMask)
    subheading('Reading the GPIO input')
    readData = sendScaCommand(ohList, 0x2, 0x1, 0x1, 0x0, True)
    idx = 0
    for oh in ohList:
        print('OH %d  GPIO Input = ' %(oh) + hex(readData[idx]))
        idx += 1


