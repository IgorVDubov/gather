from log_module import logger
import log_module
import asyncio
from main_pool import MainPool
import classes
import globals
from exchange_server import ModbusExchangeServer
from source_pool import SourcePool

# def makeChannelBase():


def init():
    loop=asyncio.get_event_loop()
    sourcePool=SourcePool(globals.ModuleList,loop)
    channels=[classes.Node(**node) for node in globals.nodes]
    channels.extend([classes.Programm(**prg) for prg in globals.programms])

    # ModbusExchServer=ModbusExchangeServer(globals.MBServerAdrMap,globals.MBServerParams['host'],globals.MBServerParams['port'])
    ModbusExchServer=None
    HTTPServer=None
    if globals.HTTPServer:
        from tornado_serv import TornadoHTTPServerInit
        HTTPServer=TornadoHTTPServerInit(globals.HTTPServerParams['port'])
    mainPool=MainPool(loop, sourcePool, channels, ModbusExchServer, HTTPServer)
    print ('Sources')
    print (mainPool.sourcePool)
    print ('Channels:')
    for channel in mainPool.channels:
        print(channel)
    logger.info ('init ok')
    return mainPool


def main():
    log_module.loggerInit('debug')
    logger.info('Starting........')
    mainPool=init()
    mainPool.start()
    
    


if __name__=='__main__':
    main()