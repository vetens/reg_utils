from cmd import Cmd
from reg_xml_parser import *
from reg_base_ops import *
import time
usleep = lambda x: time.sleep(x/1000000.0)

try:
    import readline
except ImportError:
    readline = None

MAX_OH_NUM = 11

histfile = os.path.expanduser('~/.reg_interface_history')
histfile_size = 1000

class Prompt(Cmd):
    """
    Class defining command line interface prompt.
       .. note :: 

          This is a base class and it can (should) be extended

    """
       
    cardname=None
    """AMC card host name"""
 
    def preloop(self):
        """Overwrites the default `preloop` behavior with addition of commands history. History file is ~/.reg_interface_history"""
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def postloop(self):
        """Overwrites the default `postloop` behavior with addition of commands history. History file is ~/.reg_interface_history"""
        if readline:
            readline.set_history_length(histfile_size)
            readline.write_history_file(histfile)

    def cmdloop_with_keyboard_interrupt(self):
        """Overwrites the default behavior such that on pressing `Ctrl-C` only the method which is currently running stops but the CLI is not terminated"""
        doQuit = False
        while doQuit != True:
            try:
                self.cmdloop()
                doQuit = True
            except KeyboardInterrupt:
                sys.stdout.write('\n')

    def do_exit(self, args):
        """Exit CLI interface"""
        return True

    def execute(self, other_function, args):
        """Allows non-interactive execution of any command"""
        other_function = 'do_'+other_function
        call_func = getattr(Prompt,other_function)
        try:
            call_func(self,*args)
        except TypeError:
            print 'Could not recognize command. See usage in tool.'

    def do_startup_test(self, args):
        print "Startup test passed"

    def complete_read(self, text, line, begidx, endidx):
        """Tab-completion for ``read`` method"""
        return completeReg(text)

    def complete_write(self, text, line, begidx, endidx):
        """Tab-completion for ``write`` method"""
        return completeReg(text)

    def do_connect(self, hostname):
        """Connect to the AMC board 

        :param str hostname: a hostname or IP address of the AMC board
        :return: A command prompt at connected AMC board or a generic prompt if connection attempt fails

        Usage:
        
        >>> connect <hostname>


        Example:

        >>> connect eagle60
        eagle60>

        """
        if (rpc_connect(hostname)):
            print '[Connection error] RPC connection failed'
            self.prompt = 'CTP7 > '
        else:
            self.prompt = hostname + ' > '
            self.cardname = hostname
            pass

    def do_outputnode(self, args):
        """
        .. _do_outputnode:
        
        Output properties of node matching name

        :param str name: Node (register) name
        :return: Properties of node matching name. 

        Usage: 

        >>> outputnode <name>

        """
        arglist = args.split()
        if len(arglist)==1:
            node = getNode(args)
            if node is not None:
                print node.output()
            else:
                print 'Node not found:',args

        else: print 'Incorrect number of arguments.' 
                
    def do_doc(self, args):
        """Alias for do_outputnode_. 

        Usage: 

        >>> doc <name>
       
        """
        self.do_outputnode(args)

    def do_mpeek(self,args):
        """Basic mpeek command to read register. 

        :param int address: Register address, usually in hex format
        :return: Register Value

        Usage: 

        >>> mpeek <address>

        """
        print mpeek(args)

    def do_mpoke(self,args):
        """Basic mpoke command to write register. 

        :param int address: Register address, usually in hex format
        :param uint_32 value: Value to write

        Usage: 

        >>> mpoke <address> <value>

        """
        arglist = args.split()
        if len(arglist)==2:
            print mpoke(arglist[0],arglist[1])
        else: print "Incorrect number of arguments!"

    def do_read(self, args):        
        """Reads register. 

        :param str name: Regiser name
        :return: |<address>|<mask>|<permission>|<name>|<value>|

        Usage: 

        >>> read <register name>

        """        
        reg = getNode(args)        
        if reg is not None:         
            address = reg.real_address        
            if 'r' in str(reg.permission):        
                print displayReg(reg)        
            elif reg.isModule: print 'This is a module!'        
            else: print hex(address),'\t',reg.name,'\t','No read permission!'         
        else:        
            print args,'not found!'

    def do_readAddress(self, args):
        """Directly read address. 

        :param uint_32 address: Register address
        :return: <address>    node: <Register Name>
                 <address>    <Register Value>

        Usage: 

        >>> readAddress <address>

        """
        try: reg = getNodeFromAddress(parseInt(args))
        except: 
            print 'Error retrieving node.'
            return
        if reg is not None: 
            address = reg.real_address
            print hex(address),'\t node: ', reg.name
            print hex(address),'\t',readAddress(address)
        else:
            print args,'not found!' 

    def do_readRawAddress(self, args):
        """Read raw address (from XML file)

        :param uint_32 address: Register address
        :return: <address>    node: <Register Name>
                 <address>    <Register Value>

        Usage: 

        >>> readRawAddress <address>

        """
        try: print readRawAddress(args)
        except: print 'Error reading address. (reg_interface)'

    def do_readAll(self, args):
        """Read all registers with read-permission

        .. note:: 

           INEFFICIENT

        Usage:

        >>> readALL

        """
        for reg in getNodesContaining(''):
            if 'r' in str(reg.permission): print displayReg(reg) 
            
    def do_readGroup(self, args): #INEFFICIENT
        """Read all registers with read-permission below node in register tree

        .. note:: 

           INEFFICIENT

        :param: str name: Register name

        Usage:

        >>> readGroup <name>

        """
        node = getNode(args)
        if node is not None: 
            print 'NODE:',node.name
            kids = []
            getAllChildren(node, kids)
            print len(kids),'CHILDREN'
            for reg in kids: 
                if 'r' in str(reg.permission): print displayReg(reg)
        else: print args,'not found!'

    def do_kw(self, args):
        """
        .. _do_kw:

        Read all registers containing KeyWord. 
      
        :param str keyword: Partial register name
        :param int link: Optical link, optional parameter. If provided, the output list of registers will be only from that link
        :return: Table of register names, permissions and values for registers containing keyword in their names

        Usage: 
    
        >>> readKW <keyword> 

        or 

        >>> readKW <keyword> <link>

        """
        arglist = args.split()
        if len(arglist)==1:
            if getNodesContaining(args) is not None and args!='':
                for reg in getNodesContaining(args):
                    address = reg.real_address
                    if 'r' in str(reg.permission):
                        print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7),readReg(reg)
                    elif reg.isModule: print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7) #,'Module!'
                    else: print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7) #,'No read permission!' 
            else: print args,'not found!'
        elif len(arglist)==2:
            found = False
            if getNodesContaining(arglist[0]) is not None and arglist[0]!='':
                for reg in getNodesContaining(arglist[0]):
                    ohx = 'OH%s.'%(arglist[1])
                    if ohx not in reg.name:
                        continue
                    found = True
                    address = reg.real_address
                    if 'r' in str(reg.permission):
                        print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7),readReg(reg)
                    elif reg.isModule: print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7) #,'Module!'
                    else: print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7) #,'No read permission!' 
                if not found: 
                    print arglist[0],' for link %s not found!'%(arglist[1])
            else: print arglist[0],'not found!'
        else: print "Incorrect number of arguments!"

    def do_readKW(self, args):
        """Alias for do_kw_"""
        self.do_kw(args)

    def do_rwc(self, args):
        """Read all registers containing keyword supporting wild card. 

        :param str keyword: Wild-carded keyword
        :return: Table of register names, permissions and values for registers containing keyword in their names

        Usage: 
         
        >>> rwc <KeyWord>

        """
        arglist = args.split('*')
        reg_superset = [getNodesContaining(arg) for arg in arglist if arg!='' ]
        try:
            result = reduce(set.intersection, map(set, reg_superset))
        except TypeError:
            print args,'not found!'
            return
        if result is None: 
            print args,'not found!'
            return
        for reg in sorted(result):
            address = reg.real_address
            if 'r' in str(reg.permission):
                print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7),readReg(reg)
            elif reg.isModule: print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7) #,'Module!'
            else: print hex(address).rstrip('L'),reg.permission,'\t',tabPad(reg.name,7) #,'No read permission!' 

    def do_write(self, args):
        """Write register applying register mask 

        :param str name: Register name 
        :param uint_32 value: Value to write 

        Usage: 
       
        >>> write <register name> <register value>

        """
        arglist = args.split()
        if len(arglist)==2:
            reg = getNode(arglist[0])
            if reg is not None:
                try: value = parseInt(arglist[1])
                except: 
                    print 'Write Value must be a number!'
                    return
                if 'w' in str(reg.permission): print writeReg(reg,value)
                else: print 'No write permission!'                
            else: print arglist[0],'not found!'
        else: print "Incorrect number of arguments!"

    def do_dumpKW(self, args):
        """Dump addresses (not-a-real ones) of all registers containing keyword. 

        :param str keyword: Keyword
        :return: Create a file `reg_dump.txt` and write there a table of register names, permissions and values for registers containing keyword in their names 

        Usage: 
      
        >>> dumpKW <keyword>

        """
        if getNodesContaining(args) is not None and args!='':
            with open("reg_dump.txt","w") as f:
                f.write('')
            for reg in getNodesContaining(args):
                address = reg.address
                with open("reg_dump.txt","a") as f:
                  if 'r' in str(reg.permission):
                      temp_s =  hex(address).rstrip('L') + '\t' + tabPad(reg.name,7) +'\n'
                      f.write(temp_s)
                  elif reg.isModule: 
                      temp_s =  hex(address).rstrip('L') + '\t' + tabPad(reg.name,7) +'\n'
                      f.write(temp_s)
                  else:
                      temp_s =  hex(address).rstrip('L') + '\t' + tabPad(reg.name,7) +'\n'
                      f.write(temp_s)
            print "DONE!"
        else: print args,'not found!'

    def do_rtest(self, args):
        """Read register certain number of times with a given interval in us. 

        :param str name: Register name
        :param int ntimes: Number of times to read the register
        :param int interval: Interval between reads in microseconds

        Usage: 
    
        >>> rtest <name> <ntimes> <interval>

        """
        arglist = args.split()
        if len(arglist)!=3:
            print 'Incorrect usage'
            return
        for i in range(int(arglist[1])):
            self.do_read(arglist[0])
            usleep(int(arglist[2]))

    def do_wtest(self, args):
        """Writes 1 to a register certain number of times with a given interval in us. 

        :param str name: Register name
        :param int ntimes: Number of times to read the register
        :param int interval: Interval between reads in microseconds

        Usage: 
    
        >>> wtest <name> <ntimes> <interval>

        """
        arglist = args.split()
        if len(arglist)!=3:
            print 'Incorrect usage'
            return
        for i in range(int(arglist[1])):
            self.do_write(arglist[0],1)
            usleep(int(arglist[2]))


