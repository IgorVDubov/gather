import logger as loggerLib
from loguru import logger
import asyncio
from copy import deepcopy
import os.path
from main_pool import MainPool
import scada_config
import channelbase
import globals
from webserver.web_connector import setHTTPServer
from exchange_server import ModbusExchangeServer
from source_pool import SourcePool
import classes


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
    httpParams=globals.HTTPServerParams
    httpParams.update({'path':os.path.join(os.path.dirname(__file__),'webserver', 'webdata')})
    HTTPServer=setHTTPServer(httpParams, classes.Data(globals.users,channelBase))
    #HTTPServer=None
    print ('Sources')
    print (sourcePool)
    print ('Channels:')
    print(channelBase)
    # import json
    # print(json.dumps([channelBase.nodesToDictFull()], sort_keys=True, indent=4))
    print('ExchangeBindings')
    print(exchangeBindings)
    print('HTTPServer:')
    print(f"host:{httpParams.get('host')}, port:{httpParams.get('port')}, wsserver:{httpParams.get('wsserver')}, " if HTTPServer else None )
    
    mainPool=MainPool(loop, sourcePool, channelBase, ModbusExchServer, exchangeBindings, HTTPServer)
    logger.info ('init ok')
    return mainPool


def main():
    loggerLib.loggerInit('ERROR')
    logger.info('Starting........')
    mainPool=init()
    mainPool.start()

if __name__=='__main__':
    main()
    