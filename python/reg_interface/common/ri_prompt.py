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

    def preloop(self):
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def postloop(self):
        if readline:
            readline.set_history_length(histfile_size)
            readline.write_history_file(histfile)

    def cmdloop_with_keyboard_interrupt(self):
        doQuit = False
        while doQuit != True:
            try:
                self.cmdloop()
                doQuit = True
            except KeyboardInterrupt:
                sys.stdout.write('\n')

    def do_exit(self, args):
        """Exit program"""
        return True

    def execute(self, other_function, args):
        other_function = 'do_'+other_function
        call_func = getattr(Prompt,other_function)
        try:
            call_func(self,*args)
        except TypeError:
            print 'Could not recognize command. See usage in tool.'

    def do_startup_test(self, args):
        print "Startup test passed"

    def complete_read(self, text, line, begidx, endidx):
        return completeReg(text)

    def complete_write(self, text, line, begidx, endidx):
        return completeReg(text)

    def do_connect(self, hostname):
        if (rpc_connect(hostname)):
            print '[Connection error] RPC connection failed'
            self.prompt = 'CTP7 > '
        else:
            self.prompt = hostname + ' > '
            pass

    def do_outputnode(self, args):
        """Output properies of node matching name. USAGE: outputnode <NAME>"""
        arglist = args.split()
        if len(arglist)==1:
            node = getNode(args)
            if node is not None:
                print node.output()
            else:
                print 'Node not found:',args

        else: print 'Incorrect number of arguments.' 
                
    def do_doc(self, args):
        """Alias for do_outputnode. Output properies of node matching name. USAGE: doc <NAME>"""
        self.do_outputnode(args)

    def do_mpeek(self,args):
        """Basic mpeek command to read register. USAGE: mpeek <address>"""
        print mpeek(args)

    def do_mpoke(self,args):
        """Basic mpoke command to write register. USAGE: mpoke <address> <value>"""
        arglist = args.split()
        if len(arglist)==2:
            print mpoke(arglist[0],arglist[1])
        else: print "Incorrect number of arguments!"

    def do_read(self, args):        
        """Reads register. USAGE: read <register name>. OUTPUT <address> <mask> <permission> <name> <value>"""        
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
        """ Directly read address. USAGE: readAddress <address> """
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
        """Read raw address (from XML file). USAGE: readRawAddress <address> """
        try: print readRawAddress(args)
        except: print 'Error reading address. (reg_interface)'

    def do_readAll(self, args):
        """Read all registers with read-permission"""
        for reg in getNodesContaining(''):
            if 'r' in str(reg.permission): print displayReg(reg) 
            
    def do_readGroup(self, args): #INEFFICIENT
        """Read all registers below node in register tree. USAGE: readGroup <register/node name> """
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
        """Read all registers containing KeyWord. USAGE: readKW <KeyWord> or readKW <KeyWord> link"""
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
        self.do_kw(args)

    def do_rwc(self, args):
        """Read all registers containing keyword supporting wild card. USAGE: rwc <KeyWord>"""
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
        """Writes register. USAGE: write <register name> <register value>"""
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
        """Dump addresses (not-a-real  ones) of all registers containing KeyWord. USAGE: dumpKW <KeyWord>"""
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
        """Read register certain number of times with a given interval in us. USAGE: rtest <regName> <number of times> <interval>"""
        arglist = args.split()
        if len(arglist)!=3:
            print 'Incorrect usage'
            return
        for i in range(int(arglist[1])):
            self.do_read(arglist[0])
            usleep(int(arglist[2]))

    def do_wtest(self, args):
        """Writes 1 to a register certain number of times with a given interval in us. USAGE: rtest <regName> <number of times> <interval>"""
        arglist = args.split()
        if len(arglist)!=3:
            print 'Incorrect usage'
            return
        for i in range(int(arglist[1])):
            self.do_write(arglist[0],1)
            usleep(int(arglist[2]))


