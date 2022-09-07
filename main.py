from log_module import logger
import log_module
import asyncio
from copy import deepcopy
from main_pool import MainPool
import classes
import channelbase
import globals
from exchange_server import ModbusExchangeServer
from source_pool import SourcePool


# def makeChannelBase():

def MBServerAdrMapInit(channelBase:channelbase.ChannelsBase,addrMaping:dict)->dict:
    newAddrMap=deepcopy(addrMaping)
    bindings=dict()
    for unit in  newAddrMap:
        for regType,data in unit.get('map').items():
            for reg in data:
                if attr:=reg.pop('attr'):
                    print(f'{reg["id"]}, {attr}')
                    bindings.update({reg['id']:channelbase.bindChannelAttr(channelBase,reg['id'],attr)})
                else:
                    raise Exception(f'no value to bind at {reg}')
    return newAddrMap, bindings

def init():
    loop=asyncio.get_event_loop()
    sourcePool=SourcePool(globals.ModuleList,loop)
    channelBase=channelbase.ChannelBaseInit(globals.nodes, globals.programms)
    newAddrMap, exchangeBindings = MBServerAdrMapInit(channelBase,globals.MBServerAdrMap)
    print('exchangeBindings')
    print(exchangeBindings)
    ModbusExchServer=ModbusExchangeServer(newAddrMap, globals.MBServerParams['host'], globals.MBServerParams['port'])
    # ModbusExchServer=None
    HTTPServer=None
    if globals.HTTPServer:
        from tornado_serv import TornadoHTTPServerInit
        HTTPServer=TornadoHTTPServerInit(globals.HTTPServerParams['port'])
    mainPool=MainPool(loop, sourcePool, channelBase, ModbusExchServer, exchangeBindings, HTTPServer)
    print ('Sources')
    print (mainPool.sourcePool)
    print ('Channels:')
    print(mainPool.channelBase)
    logger.info ('init ok')
    return mainPool


def main():
    log_module.loggerInit('debug')
    logger.info('Starting........')
    mainPool=init()
    # mainPool.start()

if __name__=='__main__':
    main()
    