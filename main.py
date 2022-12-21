#!/usr/bin/env python3

import logger as loggerLib
from loguru import logger
import asyncio
import sys
import os.path
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  #Если запускаем из под win    

import globals
import importlib
scada_config=importlib.import_module('projects.'+globals.PROJECT['path']+'.scadaconfig')
from sourcepool import SourcePool
import channelbase
from webserver.webconnector import setHTTPServer
from exchangeserver import ModbusExchangeServer, MBServerAdrMapInit
import db_interface
import classes
from mainpool import MainPool




def init():
    loop=asyncio.get_event_loop()
    dbQuie=asyncio.Queue()
    if len(modules:=scada_config.ModuleList):
        sourcePool=SourcePool(modules,loop)
    else:
        sourcePool=None 
    channelBase=channelbase.channel_base_init(scada_config.channels_config, dbQuie)
    newAddrMap, exchangeBindings = MBServerAdrMapInit(channelBase,scada_config.MBServerAdrMap)
    ModbusExchServer=ModbusExchangeServer(newAddrMap, globals.MBServerParams['host'], globals.MBServerParams['port'])
    httpParams=globals.HTTPServerParams
    httpParams.update({'path':os.path.join(os.path.dirname(__file__),'webserver', 'webdata')})
    HTTPServer=setHTTPServer(httpParams, classes.Data(globals.users,channelBase))
    DBInterface=db_interface.DBInterface(globals.DB_TYPE, globals.DB_PARAMS)
    #HTTPServer=None
    print ('Sources')
    print (sourcePool)
    print ('Channels:')
    print(channelBase)
    # import json
    # print(json.dumps([channelBase.nodesToDictFull()], sort_keys=True, indent=4))
    print(f'Modbus Exchange Server: {globals.MBServerParams["host"]}, {globals.MBServerParams["port"]}')
    print('ExchangeBindings')
    print(exchangeBindings)
    print('HTTPServer:')
    print(f"host:{httpParams.get('host')}, port:{httpParams.get('port')}, wsserver:{httpParams.get('wsserver')}, " if HTTPServer else None )
    
    mainPool=MainPool(loop, sourcePool, channelBase, ModbusExchServer, exchangeBindings, HTTPServer, dbQuie, DBInterface)
    logger.info ('init done')
    return mainPool

def test_component():
    loop=asyncio.get_event_loop()
    loggerLib.loggerInit('ERROR')
    logger.info('Starting........')
    httpParams=globals.HTTPServerParams
    channelBase=None
    HTTPServer=setHTTPServer(httpParams, classes.Data(globals.users,channelBase))
    loop.run_forever()

    

def main():
    loggerLib.loggerInit('ERROR')
    logger.info('Starting........')
    mainPool=init()
    mainPool.start()
    

if __name__=='__main__':
    main()
    # test_component()
    