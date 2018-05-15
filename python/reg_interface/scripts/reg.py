#!/usr/bin/env python
import sys, os, subprocess

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-e", "--execute", type="str", dest="exe",
                      help="Function to execute once", metavar="exe", default=None)
    parser.add_option("-n", "--hostname", type="string", dest="hostname",
                      help="CTP7 hostname, default is the one used at p5", default="amc-s2e01-23-03")

    (options, args) = parser.parse_args()

    for path in sys.path:
        print path
    try:
       from gem_reg_interface_extras.ri_prompt_extended import *
       print "Extended prompt module found"
    except ImportError:
       from reg_interface.common.ri_prompt import *
       print "Extended prompt module not found, importing basic one"

    if options.exe:
        parseXML()
        if (rpc_connect(options.hostname)):
          print '[Connection error] RPC connection failed'
          exit
        prompt=Prompt()
        prompt.execute(options.exe,args)
        sys.exit()
    else:
        try:
            parseXML()
            prompt = Prompt()
            prompt.prompt = 'CTP7 > '
            print 'Starting CTP7 Register Command Line Interface. Please connect to CTP7 using connect <hostname> command unless you use it directly at the CTP7'
            prompt.cmdloop_with_keyboard_interrupt()
        except TypeError as te:
            print '[TypeError] Incorrect usage. See help... ', te
        except KeyboardInterrupt:
            print '\n'
