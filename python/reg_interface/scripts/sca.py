#!/usr/bin/env python

from reg_utils.reg_interface.common.reg_xml_parser import getNode, parseInt, parseXML
from reg_utils.reg_interface.common.reg_base_ops import *
from reg_utils.reg_interface.common.print_utils import *
from reg_utils.reg_interface.common.bit_utils import *
from reg_utils.reg_interface.common.jtag import initJtagRegAddrs
from reg_utils.reg_interface.common.sca_utils import *
from reg_utils.reg_interface.common.sca_common_utils import *
from time import *
import socket

def compareFwFiles(args):
    import os
    if "bit" not in args.fwFileBit:
        print("you must supply a *.bit file to 'fwFileBit'")
        exit(os.EX_USAGE)
    if "mcs" not in args.fwFileMCS:
        print("you must supply a *.mcs file to 'fwFileMCS'")
        exit(os.EX_USAGE)

    from reg_utils.reg_interface.arm.program_fpga import compare_mcs_bit
    compare_mcs_bit(args.fwFileMCS, args.fwFileBit)
    return

def fpgaHardResetSync(args):
    scaInit(args)
    fpga_single_hard_reset()
    return

def fpgaHardResetAsync(args):
    ohList = scaInit(args)
    fpga_keep_hard_reset(ohList)
    fpga_remove_hard_reset(ohList)
    return

def fpgaId(args):
    scaInit(args)
    read_fpga_id(args.ohMask)
    return

def fpgaProgram(args):
    scaInit(args)

    hostname = socket.gethostname()
    if 'eagle' not in hostname:
        printRed("This method should only be called from the card!!")
        return
    
    import os
    if "bit" in args.fwFile:
        ftype = "bit"
        filename = args.fwFile
    elif "mcs" in args.fwFile:
        ftype = "mcs"
        filename = args.fwFile
    else:
        printRed('Usage: sca.py local <ohMask> program-fpga fwFile=<filename>')
        print("you must supply either a *.bit or a *.mcs file to 'fwFile'")
        return
    
    from reg_utils.reg_interface.arm.program_fpga import program_fpga
    program_fpga(args.ohMask,ftype,filename)
    return

def gpioRead(args):
    scaInit(args)
    gpio.read_input(args.ohMask)
    return

def gpioSetDirection(args):
    scaInit(args)
    gpio.set_direction(args.ohMask,args.gpioValue)
    return

def gpioSetOutput(args):
    scaInit(args)
    gpio.set_output(args.ohMask,args.gpioValue)

def scaInit(args, isReset=False):
    ohList = getOHlist(args.ohMask)

    parseXML()
    hostname = socket.gethostname()
    if 'eagle' in hostname:
        pass
    else:
        hostname = args.cardName
        rpc_connect(args.cardName)
    initJtagRegAddrs()

    heading("Hola, I'm SCA controller tester :)")

    if not checkStatus(ohList):
        if not isReset:
            exit()

    writeReg(getNode('GEM_AMC.SLOW_CONTROL.SCA.MANUAL_CONTROL.LINK_ENABLE_MASK'), args.ohMask)

    return ohList

def scaReset(args):
    scaInit(args=args,isReset=True)
    sca_reset(args.ohMask)
    return

def sysmon(args):
    scaInit(args)
    run_sysmon(args.ohMask)
    return
 
if __name__ == '__main__':
    # create the parser
    import argparse
    parser = argparse.ArgumentParser(description='Arguments to supply to sca.py')

    # Positional arguments
    parser.add_argument("cardName", type=str, help="hostname of the AMC you are connecting too, e.g. 'eagle64'; if running on an AMC use 'local' instead", metavar="cardName")
    parser.add_argument("ohMask", type=parseInt, help="ohMask to apply, a 1 in the n^th bit indicates the n^th OH should be considered", metavar="ohMask")
    subparserCmds = parser.add_subparsers(help="sca command help")

    # Create subparser for compare-mcs-bit
    parser_compareFwFiles = subparserCmds.add_parser("compare-mcs-bit", help="compares a *.mcs with a *.bit file to check if the firmware is the same")
    parser_compareFwFiles.add_argument("fwFileMCS",type=str, help="firmware mcs file to be used in the comparison", metavar="fwFileMCS")
    parser_compareFwFiles.add_argument("fwFileBit",type=str, help="firmware bit file to be used in the comparison", metavar="fwFileBit")
    parser_compareFwFiles.set_defaults(func=compareFwFiles)

    # Create subparser for fpga hard reset 
    parser_reset = subparserCmds.add_parser("h", help="A synchronous FPGA hard reset will be done to all OHs connected to this AMC")
    parser_reset.set_defaults(func=fpgaHardResetSync)

    # Create subparser for holding fpga in hard reset 
    parser_reset = subparserCmds.add_parser("hh", help="FPGA hard reset will be done on the selected OHs defined by the ohMask, which is not guaranteed to arrive to all selected OHs at the same time")
    parser_reset.set_defaults(func=fpgaHardResetAsync)

    # Create subparser for getting fpga ID 
    parser_reset = subparserCmds.add_parser("fpga-id", help="FPGA ID will be read through JTAG")
    parser_reset.set_defaults(func=fpgaId)

    # Create subparser for programming the fpga
    parser_programFPGA = subparserCmds.add_parser("program-fpga", help="Program OH FPGA with a bitfile or an MCS file")
    parser_programFPGA.add_argument("fwFile", type=str, help="firmware file to program fpga with, must end in either '*.bit' or '*.mcs'", metavar="fwFile")
    parser_programFPGA.set_defaults(func=fpgaProgram)

    # Create subparser for gpio-read-input
    parser_readGPIO = subparserCmds.add_parser("gpio-read-input", help="Read GPIO settings of the SCA")
    parser_readGPIO.set_defaults(func=gpioRead)

    # Create subparser for gpio-set-direction
    # Default corresponds to setting SCA output direction on OHv3c
    parser_setGPIODirection = subparserCmds.add_parser("gpio-set-direction", help="Set the GPIO Direction Mask")
    parser_setGPIODirection.add_argument("gpioValue", type=parseInt, default=0x0fffff8f, metavar="gpioValue",
            help="32 bit number where each bit represents a GPIO channel.  If a given bit is high it means that this GPIO channel will be set to OUTPUT mode, and otherwise it will be set to INPUT mode")
    parser_setGPIODirection.set_defaults(func=gpioSetDirection)
   
    # Create subparser for gpio-set-output
    # Default corresponds to setting SCA output value on the OHv3c
    parser_setGPIOOutput = subparserCmds.add_parser("gpio-set-output", help="Set the GPIO output values")
    parser_setGPIOOutput.add_argument("gpioValue", type=parseInt, default=0xf00000f0, metavar="gpioValue",
            help="32 bit number where each bit represents the 32 GPIO channels state")
    parser_setGPIOOutput.set_defaults(func=gpioSetOutput)

    # Create subparser for sca reset 
    parser_reset = subparserCmds.add_parser("r", help="SCA reset will be done")
    parser_reset.set_defaults(func=scaReset)

    # Create subparser for sysmon
    parser_sysmon = subparserCmds.add_parser("sysmon", help="Read FPGA sysmon data repeatedly")
    parser_sysmon.set_defaults(func=sysmon)

    # Parser the arguments and call the appropriate function
    args = parser.parse_args()
    args.func(args)
