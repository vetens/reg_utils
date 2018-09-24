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

    parser = argparse.ArgumentParser(description='Arguments to supply to repeated_reg_read.py')

    parser.add_argument('reg_name', metavar='reg_name', type=str,help='Name of the register to read')
    parser.add_argument('nreads', metavar='nreads', type=str,help='Number of reads')
    parser.add_argument('sleeptime', metavar='sleeptime', type=str,help='Amount of time to sleep in microseconds')
    parser.add_argument('-f','--filename', metavar='filename', type=str, help="Filename to which output information is written", default="repeated_reg_read.txt")
    parser.add_argument('--card', metavar='card', type=str,help='CTP7 hostname (has no effect if you are running on a hostname that starts with eagle)',default="eagle26")

    args = parser.parse_args()

    f = open(args.filename,"w")        
            
    parseXML()
    
    hostname = socket.gethostname()

    if hostname[0:4] == "eagle":
        print("This script is running on"+str(hostname)+".")
        pass
    else:
       print("This script is not running on an eagle machine. rpc_connect(\""+str(args.card)+"\") will be called.")
       rpc_connect(args.card)   

    writeReg(getNode("GEM_AMC.GEM_SYSTEM.CTRL.LINK_RESET"),0x1)   

    time.sleep(float(args.sleeptime)/float(1000000))
    
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

    node = getNode(args.reg_name)

    d = {}
    
    for i in range(0,int(args.nreads)):
        value = readAddress(node.real_address)

        if value in d.keys():
            d[value] += 1
        else:
            d[value] = 1
        
        time.sleep(float(args.sleeptime)/float(1000000))

    crc_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.CRC_ERROR_CNT").real_address)
    packet_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.PACKET_ERROR_CNT").real_address)
    bitstuffing_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.BITSTUFFING_ERROR_CNT").real_address)
    timeout_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.TIMEOUT_ERROR_CNT").real_address)
    axi_strobe_error_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.AXI_STROBE_ERROR_CNT").real_address)
    transaction_cnt_after = readAddress(getNode("GEM_AMC.SLOW_CONTROL.VFAT3.TRANSACTION_CNT").real_address)

    print >> f, "| after  | "+crc_error_cnt_after+"    | "+packet_error_cnt_after+"       | "+bitstuffing_error_cnt_after+"            | "+timeout_error_cnt_after+"        | "+axi_strobe_error_cnt_after+"           | "+transaction_cnt_after+"      |"

    print >> f, "| delta  | "+str(int(crc_error_cnt_after,16) - int(crc_error_cnt_before,16))+"             | "+str(int(packet_error_cnt_after,16) - int(packet_error_cnt_before,16))+"                | "+str(int(bitstuffing_error_cnt_after,16) - int(bitstuffing_error_cnt_before,16))+"                     | "+str(int(timeout_error_cnt_after,16) - int(timeout_error_cnt_before,16))+"                 | "+str(int(axi_strobe_error_cnt_after,16) - int(axi_strobe_error_cnt_before,16))+"               | "+str(int(transaction_cnt_after,16) - int(transaction_cnt_before,16))+"          |"    
    
    print >> f, d
    
    #readAddress()
