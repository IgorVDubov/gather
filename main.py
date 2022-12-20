#!/usr/bin/env python3

import logger as loggerLib
from loguru import logger
import asyncio
import sys
import os.path
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  #Если запускаем из под win    
from importlib.machinery import SourceFileLoader
import globals
scada_config=SourceFileLoader('scadaconfig','projects'+globals.PROJECT['path']+'scadaconfig.py').load_module
# import projects.demomachines.scadaconfig as scada_config

from mainpool import MainPool
import projects.demomachines.scadaconfig as scada_config
import channelbase
from webserver.webconnector import setHTTPServer
from exchangeserver import ModbusExchangeServer, MBServerAdrMapInit
from sourcepool import SourcePool
import db_interface
import classes




def init():
    loop=asyncio.get_event_loop()
    dbQuie=asyncio.Queue()
    sourcePool=SourcePool(scada_config.ModuleList,loop)
    channelBase=channelbase.ChannelBaseInit(scada_config.channelsConfig, dbQuie)
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
    print('ExchangeBindings')
    print(exchangeBindings)
    print('HTTPServer:')
    print(f"host:{httpParams.get('host')}, port:{httpParams.get('port')}, wsserver:{httpParams.get('wsserver')}, " if HTTPServer else None )
    
    mainPool=MainPool(loop, sourcePool, channelBase, ModbusExchServer, exchangeBindings, HTTPServer, dbQuie, DBInterface)
    logger.info ('init done')
    return mainPool


def main():
    loggerLib.loggerInit('ERROR')
    logger.info('Starting........')
    mainPool=init()
    mainPool.start()

if __name__=='__main__':
    main()
    