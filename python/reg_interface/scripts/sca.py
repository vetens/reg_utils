#!/usr/bin/env python

from reg_utils.reg_interface.common.reg_xml_parser import getNode, parseXML
from reg_utils.reg_interface.common.reg_base_ops import *
from reg_utils.reg_interface.common.print_utils import *
from reg_utils.reg_interface.common.bit_utils import *
from reg_utils.reg_interface.common.jtag import initJtagRegAddrs
from reg_utils.reg_interface.common.sca_utils import *
from reg_utils.reg_interface.common.sca_common_utils import *
from time import *
import socket

def main(cardName, instructions, ohMask, fwFileBit=None, fwFileMCS=None, gpioValue=None):
    ohList = getOHlist(ohMask)

    parseXML()
    hostname = socket.gethostname()
    if 'eagle' in hostname:
        pass
    else:
        hostname = cardName
        rpc_connect(cardName)
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
            from reg_utils.reg_interface.arm.program_fpga import program_fpga
        else:
            printRed("This method should only be called from the card!!")
            return

        if fwFileBit is not None:
            ftype = "bit"
            filename = fwFileBit
        elif fwFileMCS is not None:
            ftype = "mcs"
            filename = fwFileMCS
        else:
            printRed('Usage: sca.py --cardName="local" --ohMask=<mask> --cmd="program-fpga" --fwFileBit=<filename>')
            printRed('if your firmware file is a *.msc file use the --fwFileMCS argument')
            return

        program_fpga(ohMask,ftype,filename)

    #elif instructions == 'test1':
    #    test1()
        
    #elif instructions == 'test2':
    #    test2()

    elif instructions == 'compare-mcs-bit':
        if ((fwFileBit is None) or (fwFileMCS is None)):
            print("Usage: sca.py --cardName=<cardName> --cmd='compare-mcs-bit' --fwFileMCS=<mcs_filename> --fwFileBit=<bit_filename>")
            return
        from reg_utils.reg_interface.arm.program_fpga import compare_mcs_bit
        compare_mcs_bit(fwFileMCS, fwFileBit)

    elif instructions == 'gpio-set-direction':
        if gpioValue is None:
            print('Usage: sca.py --cardName=<cardName> --cmd="gpio-set-direction" --gpioValue=<direction-mask>')
            print('direction-mask is a 32 bit number where each bit represents a GPIO channel -- if a given bit is high it means that this GPIO channel will be set to OUTPUT mode, and otherwise it will be set to INPUT mode')
            return
        gpio.set_direction(ohMask,gpioValue)

    elif instructions == 'gpio-set-output':
        if gpioValue is None:
            print('Usage: sca.py --cardName=<cardName> --cmd="gpio-set-output" --gpioValue=<output-data>')
            print('output-data is a 32 bit number representing the 32 GPIO channels state')
            return
        gpio.set_output(ohMask,gpioValue)

    elif instructions == 'gpio-read-input':
        gpio.read_input(ohMask)
 
if __name__ == '__main__':
    supportedCmds = [
            'compare-mcs-bit',
            'h',
            'hh',
            'fpga-id',
            'gpio-read-input',
            'gpio-set-direction',
            'gpio-set-output',
            'program-fpga',
            'r',
            'sysmon',
            #'test1',
            #'test2',
            ]
    from optparse import OptionParser
    import argparse
    parser = argparse.ArgumentParser(description='Arguments to supply to sca.py')
    parser.add_argument("--cardName", type="string", dest="cardName", default=None, required=True,
                      help="hostname of the AMC you are connecting too, e.g. 'eagle64'; if running on an AMC use 'local' instead", metavar="cardName")
    parser.add_argument("--cmd", type="string", dest="cmd", default=None, required=True, choices=supportedCmds,
                      help="command to be executed", metavar="cardName")
    parser.add_argument("--fwFileBit", type="string", dest="fwFileBit", default=None,
                      help="firmware bit file to be used with either 'program-fpga' or 'compare-mcs-bit' commands (e.g. --cmd='program-fpga')", metavar="fwFileBit")
    parser.add_argument("--fwFileMCS", type="string", dest="fwFileMCS", default=None,
                      help="firmware mcs file to be used with either 'program-fpga' or 'compare-mcs-bit' commands (e.g. --cmd='program-fpga')", metavar="fwFileBit")
    parser.add_argument("--gpioValue", type="int", dest="gpioValue", default=None,
                      help="gpio value to write with either 'gpio-set-direction' or 'gpio-set-output' commands (e.g. --cmd='gpio-set-direction')", metavar="gpioValue")
    parser.add_argument("--ohMask", type="int", dest="ohMask", default=0x1,
                      help="ohMask to apply, a 1 in the n^th bit indicates the n^th OH should be considered", metavar="ohMask")
    (options, args) = parser.parse_args()

    import os
    if ((options.fwFileBit is not None) and ("bit" not in options.fwFileBit)):
        print("you must supply a *.bit file to '--fwFileBit'")
        exit(os.EX_USAGE)
    if ((options.fwFileMCS is not None) and ("mcs" not in options.fwFileMCS)):
        print("you must supply a *.mcs file to '--fwFileMCS'")
        exit(os.EX_USAGE)

    main(
            cardName=options.cardName,
            instructions=options.cmd,
            ohMask=options.ohMask,
            fwFileBit=options.fwFileBit,
            fwFileMCS=options.fwFileMCS,
            gpioValue=options.gpioValue
            )
