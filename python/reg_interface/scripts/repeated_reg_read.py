#!/usr/bin/env python

from reg_utils.reg_interface.common.reg_xml_parser import getNode, parseXML
from reg_utils.reg_interface.common.reg_base_ops import readAddress
from reg_utils.reg_interface.common.reg_base_ops import writeReg
from reg_utils.reg_interface.common.print_utils import printRed
from reg_utils.reg_interface.common.jtag import initJtagRegAddrs
from reg_utils.reg_interface.common.reg_base_ops import *

#from rw_reg import *
#from mcs import *

import time
import array
import struct
import os
import sys
import socket

import argparse

if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--filename", type="str", dest="filename", help="Filename to which output information is written", default="repeated_reg_read.txt")

    (options, args) = parser.parse_args()

    if len(args) != 3:
            print('Usage: repeated_reg_read.py <register_name> <number of times> <sleep time in microseconds>')
            exit(os.EX_USAGE)

    f = open(options.filename,"w")        
            
    parseXML()
    
    hostname = socket.gethostname()

    if hostname == "eagle26":
        print "This script is running on eagle26."
        pass
    else:
       print "This script is not running on eagle26. rpc_connect(\"eagle26\") will be called."
       rpc_connect("eagle26")   

       HW_RW_REG 

    writeReg(getNode("GEM_AMC.GEM_SYSTEM.CTRL.LINK_RESET"),0x1)   

    time.sleep(float(sys.argv[3])/float(1000000))
    
    crc_error_cnt_before = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.CRC_ERROR_CNT").real_address)
    packet_error_cnt_before = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.PACKET_ERROR_CNT").real_address)
    bitstuffing_error_cnt_before = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.BITSTUFFING_ERROR_CNT").real_address)
    timeout_error_cnt_before = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.TIMEOUT_ERROR_CNT").real_address)
    axi_strobe_error_cnt_before = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.AXI_STROBE_ERROR_CNT").real_address)
    transaction_cnt_before = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.TRANSACTION_CNT").real_address)
    link_reset_before = readAddress(getNode("GEM_AMC.GEM_SYSTEM.CTRL.LINK_RESET").real_address)

    print >> f, "|        | CRC_ERROR_CNT | PACKET_ERROR_CNT | BITSTUFFING_ERROR_CNT | TIMEOUT_ERROR_CNT | AXI_STROBE_ERROR_CNT | TRANSACTION_CNT |"
    print >> f, "|:------ | :------------ | :--------------- | :-------------------- | :---------------- | :------------------- | :-------------- |"
    print >> f, "| before | "+crc_error_cnt_before+"    | "+packet_error_cnt_before+"       | "+bitstuffing_error_cnt_before+"            | "+timeout_error_cnt_before+"        | "+axi_strobe_error_cnt_before+"           | "+transaction_cnt_before+"      |"

#    print "GEM_AMC.SLOW_CONTROL.VFAT3.CRC_ERROR_CNT = "+crc_error_cnt_before
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.PACKET_ERROR_CNT = "+packet_error_cnt_before
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.BITSTUFFING_ERROR_CNT = "+ bitstuffing_error_cnt_before
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.TIMEOUT_ERROR_CNT = "+timeout_error_cnt_before
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.AXI_STROBE_ERROR_CNT = "+axi_strobe_error_cnt_before
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.TRANSACTION_CNT = "+transaction_cnt_before
#    print "GEM_AMC.GEM_SYSTEM.CTRL.LINK_RESET = "+link_reset_before
    
    node = getNode(sys.argv[1])

    d = {}
    
    for i in range(0,int(sys.argv[2])):
        value = readAddress(node.real_address)

        if value in d.keys():
            d[value] += 1
        else:
            d[value] = 1
        
        time.sleep(float(sys.argv[3])/float(1000000))

    crc_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.CRC_ERROR_CNT").real_address)
    packet_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.PACKET_ERROR_CNT").real_address)
    bitstuffing_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.BITSTUFFING_ERROR_CNT").real_address)
    timeout_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.TIMEOUT_ERROR_CNT").real_address)
    axi_strobe_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.AXI_STROBE_ERROR_CNT").real_address)
    transaction_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.TRANSACTION_CNT").real_address)

    print >> f, "| after  | "+crc_error_cnt_after+"    | "+packet_error_cnt_after+"       | "+bitstuffing_error_cnt_after+"            | "+timeout_error_cnt_after+"        | "+axi_strobe_error_cnt_after+"           | "+transaction_cnt_after+"      |"

    print >> f, "| delta  | "+str(int(crc_error_cnt_after,16) - int(crc_error_cnt_before,16))+"             | "+str(int(packet_error_cnt_after,16) - int(packet_error_cnt_before,16))+"                | "+str(int(bitstuffing_error_cnt_after,16) - int(bitstuffing_error_cnt_before,16))+"                     | "+str(int(timeout_error_cnt_after,16) - int(timeout_error_cnt_before,16))+"                 | "+str(int(axi_strobe_error_cnt_after,16) - int(axi_strobe_error_cnt_before,16))+"               | "+str(int(transaction_cnt_after,16) - int(transaction_cnt_before,16))+"          |"    
    
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.CRC_ERROR_CNT = "+crc_error_cnt_after
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.PACKET_ERROR_CNT = "+packet_error_cnt_after
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.BITSTUFFING_ERROR_CNT = "+ bitstuffing_error_cnt_after
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.TIMEOUT_ERROR_CNT = "+timeout_error_cnt_after
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.AXI_STROBE_ERROR_CNT = "+axi_strobe_error_cnt_after
#    print "GEM_AMC.SLOW_CONTROL.VFAT3.TRANSACTION_CNT = "+transaction_cnt_after
#    print "GEM_AMC.GEM_SYSTEM.CTRL.LINK_RESET = "+link_reset_after

#    print "Delta GEM_AMC.SLOW_CONTROL.VFAT3.CRC_ERROR_CNT = "+str(int(crc_error_cnt_after,16) - int(crc_error_cnt_before,16))
#    print "Delta GEM_AMC.SLOW_CONTROL.VFAT3.PACKET_ERROR_CNT = "+str(int(packet_error_cnt_after,16) - int(packet_error_cnt_before,16))
#    print "Delta GEM_AMC.SLOW_CONTROL.VFAT3.BITSTUFFING_ERROR_CNT = "+ str(int(bitstuffing_error_cnt_after,16) - int(bitstuffing_error_cnt_before,16)) 
#    print "Delta GEM_AMC.SLOW_CONTROL.VFAT3.TIMEOUT_ERROR_CNT = "+str(int(timeout_error_cnt_after,16) - int(timeout_error_cnt_before,16))
#    print "Delta GEM_AMC.SLOW_CONTROL.VFAT3.AXI_STROBE_ERROR_CNT = "+str(int(axi_strobe_error_cnt_after,16) - int(axi_strobe_error_cnt_before,16))
#    print "Delta GEM_AMC.SLOW_CONTROL.VFAT3.TRANSACTION_CNT = "+str(int(transaction_cnt_after,16) - int(transaction_cnt_before,16))
#    print "Delta GEM_AMC.GEM_SYSTEM.CTRL.LINK_RESET = "+str(int(link_reset_after,16) - int(link_reset_before,16))

    print >> f, d
    
    #readAddress()
