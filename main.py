from log_module import logger
import log_module
import asyncio
from copy import deepcopy
from main_pool import MainPool
import scada_config
import channelbase
import globals

from exchange_server import ModbusExchangeServer
from source_pool import SourcePool


def MBServerAdrMapInit(channelBase:channelbase.ChannelsBase,addrMaping:dict)->dict:
    newAddrMap=deepcopy(addrMaping)
    bindings=dict()
    for unit in  newAddrMap:
        for regType,data in unit.get('map').items():
            for reg in data:
                if attr:=reg.pop('attr'):
                    bindings.update({reg['id']:channelbase.bindChannelAttr(channelBase,reg['id'],attr)})
                else:
                    raise Exception(f'no value to bind at {reg}')
    return newAddrMap, bindings

def init():
    loop=asyncio.get_event_loop()
    sourcePool=SourcePool(scada_config.ModuleList,loop)
    channelBase=channelbase.ChannelBaseInit(scada_config.nodes, scada_config.programms)
    newAddrMap, exchangeBindings = MBServerAdrMapInit(channelBase,scada_config.MBServerAdrMap)
    ModbusExchServer=ModbusExchangeServer(newAddrMap, globals.MBServerParams['host'], globals.MBServerParams['port'])
    # ModbusExchServer=None
    HTTPServer=globals.HTTPServer
    print ('Sources')
    print (sourcePool)
    print ('Channels:')
    print(channelBase)
    print('ExchangeBindings')
    print(exchangeBindings)
    mainPool=MainPool(loop, sourcePool, channelBase, ModbusExchServer, exchangeBindings, HTTPServer)
    logger.info ('init ok')
    return mainPool


def main():
    log_module.loggerInit('debug')
    logger.info('Starting........')
    mainPool=init()
    mainPool.start()

if __name__=='__main__':
    main()
    