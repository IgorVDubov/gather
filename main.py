from log_module import logger
import log_module
import asyncio

from main_pool import MainPool
import classes
import globals
import sources


def sourcePoolInit(loop):
    from sources import ModuleList
    from source_pool import SourcePool
    return SourcePool(ModuleList,loop)

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
    loop=asyncio.get_event_loop()
    sourcePool=sourcePoolInit(loop)
    channels=[classes.Node(**machine) for machine in getNodes()]
    ModbusServer
    mainPool=MainPool(loop, sourcePool, channels, getMBServAddrMap(), getMBServParams(), globals.HTTPServer)
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