import sys, os, socket
import cPickle as pickle
import gc
from collections import OrderedDict

"""``reg_xml_parser`` module defines XML address table parser"""

ADDRESS_TABLE_TOP = os.getenv("REG_XML_PATH")+'/amc_address_table_top.xml'
"""Address table location is defined through `$REG_XML_PATH`. The file name should be `amc_address_table_top.xml`"""
hostname = socket.gethostname()

DEBUG = True
nodes = OrderedDict()

class Node:
    """Class defining XML node 
    """
    name = ''
    """Node full name"""
    description = ''
    """Node description"""
    vhdlname = ''
    """Node VHDL name"""
    address = 0x0
    """Register address in relative address space"""
    real_address = 0x0
    """Register real address"""
    permission = ''  
    """Register permission. Possible values: 'r','w','rw' or None"""
    mask = 0x0
    """Register mask"""
    isModule = False
    """Flag indicating if a given node is a register or a module"""
    parent = None
    """Parent node"""
    level = 0
    warn_min_value = None
    """Min value warning threshold for monitoring"""
    error_min_value = None
    """Min value error threshold for monitoring"""

    def __init__(self):
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def getVhdlName(self):
        return self.name.replace(TOP_NODE_NAME + '.', '').replace('.', '_')

    def output(self):
        print 'Name:',self.name
        print 'Description:',self.description
        print 'Address:','{0:#010x}'.format(self.address)
        print 'Permission:',self.permission
        if self.mask is not None: 
            print 'Mask:','{0:#010x}'.format(self.mask)
        else:
            print 'Mask: None'
        print 'Module:',self.isModule
        print 'Parent:',self.parent.name

def main():
    parseXML()
    print 'Example:'
    random_node = nodes.values()[74]
    print 'Node:',random_node.name
    print 'Parent:',random_node.parent.name
    kids = []
    getAllChildren(random_node, kids)
    print len(kids), kids[0].name

def parseXML():
    print 'Open pickled address table if available ',ADDRESS_TABLE_TOP[:-3]+'pickle...'

    fname =  ADDRESS_TABLE_TOP[:-3] + "pickle"
    try:
        gc.disable()
        f = open(fname, 'r')
        global nodes 
        nodes = pickle.load(f) 
        f.close()
        gc.enable()
    except IOError:
        if 'eagle' in hostname:
            print 'Pickle file not found, please create new pickle file at the host PC and upload it to the CTP7 card'
            sys.exit()
        else:
            print 'Pickle file not found, parsing ',ADDRESS_TABLE_TOP,'...'
            import lxml.etree as xml
            tree = xml.parse(ADDRESS_TABLE_TOP)
            tree.xinclude()
            root = tree.getroot()
            vars = {}
            makeTree(root,'',0x0,nodes,None,vars,False)

            # Save parsed nodes as pickle
            name = ADDRESS_TABLE_TOP[:-3] + "pickle"
            f = open(name, 'w')
            pickle.dump(nodes, f, -1)
            f.close()

    return nodes

def makeTree(node,baseName,baseAddress,nodes,parentNode,vars,isGenerated):
    
    if (isGenerated == None or isGenerated == False) and node.get('generate') is not None and node.get('generate') == 'true':
        generateSize = parseInt(node.get('generate_size'))
        generateAddressStep = parseInt(node.get('generate_address_step'))
        generateIdxVar = node.get('generate_idx_var')
        for i in range(0, generateSize):
            vars[generateIdxVar] = i
            makeTree(node, baseName, baseAddress + generateAddressStep * i, nodes, parentNode, vars, True)
        return
    newNode = Node()
    name = baseName
    if baseName != '': name += '.'
    if node.get('id') is not None:
        name += node.get('id')
    name = substituteVars(name, vars)
    newNode.name = name
    if node.get('description') is not None:
        newNode.description = node.get('description')
    address = baseAddress
    if node.get('address') is not None:
        address = baseAddress + parseInt(node.get('address'))
    newNode.address = address
    newNode.real_address = (address<<2)+0x64000000
    newNode.permission = node.get('permission')
    newNode.mask = parseInt(node.get('mask'))
    newNode.isModule = node.get('fw_is_module') is not None and node.get('fw_is_module') == 'true'
    if node.get('sw_monitor_warn_min_threshold') is not None:
        newNode.warn_min_value = node.get('sw_monitor_warn_min_threshold') 
    if node.get('sw_monitor_error_min_threshold') is not None:
        newNode.error_min_value = node.get('sw_monitor_error_min_threshold') 
    nodes[name] = newNode
    if parentNode is not None:
        parentNode.addChild(newNode)
        newNode.parent = parentNode
        newNode.level = parentNode.level+1
    for child in node:
        makeTree(child,name,address,nodes,newNode,vars,False)

def getAllChildren(node,kids=[]):
    if node.children==[]:
        kids.append(node)
        return kids
    else:
        for child in node.children:
            getAllChildren(child,kids)

def getNode(nodeName):
    try: 
        return nodes[nodeName]
    except KeyError:
        print "Node %s not found" %(nodeName)
        return None

def getNodeFromAddress(nodeAddress):
    return next((node for node in nodes.values() if node.real_address == nodeAddress),None)

def getNodesContaining(nodeString):
    nodelist = [nodes[key] for key in nodes if nodeString in key]
    if len(nodelist): 
        return nodelist
    else: return None

#returns *readable* registers
def getRegsContaining(nodeString):
    nodelist = [nodes[key] for key in nodes if nodeString in key and nodes[key].permission is not None]
    if len(nodelist):
        return nodelist
    else: return None

def completeReg(string):
    possibleNodes = [] 
    completions = []
    currentLevel = len([c for c in string if c=='.'])
  
    possibleNodes = [node for node in nodes.values() if node.name.startswith(string) and node.level == currentLevel]
    if len(possibleNodes)==1:
        if possibleNodes[0].children == []: return [possibleNodes[0].name]
        for n in possibleNodes[0].children:
            completions.append(n.name)
    else:
        for n in possibleNodes:
            completions.append(n.name)
    return completions

def parseInt(s):
    if s is None:
        return None
    string = str(s)
    if string.startswith('0x'):
        return int(string, 16)
    elif string.startswith('0b'):
        return int(string, 2)
    else:
        return int(string)


def substituteVars(string, vars):
    if string is None:
        return string
    ret = string
    for varKey in vars.keys():
        ret = ret.replace('${' + varKey + '}', str(vars[varKey]))
    return ret

if __name__ == '__main__':
    main()
