from log_module import logger
import log_module
#import asyncio

from main_pool import MainPool
import node_class


def getModules():
    from globals import ModuleList
    return ModuleList

def getNodes():
    from globals import machinesList
    return machinesList

def getMBServAddrMap():
    from globals import MBServerAdrMap
    return MBServerAdrMap

def getMBServParams():
    from globals import MBServerParams
    return MBServerParams

def init():
    mainPool=MainPool(getModules(),[node_class.Node(**_) for _ in getNodes()], getMBServAddrMap(),getMBServParams() )
    print ('Sources')
    print (mainPool.sourcePool)
    print ('Nodes')
    for node in mainPool.nodes:
        print(node)
    logger.info ('init ok')
    return mainPool


def main():
    log_module.loggerInit('debug')
    logger.info('Starting........')
    mainPool=init()
    mainPool.start()
    
    


if __name__=='__main__':
    main()