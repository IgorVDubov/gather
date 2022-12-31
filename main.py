#!/usr/bin/env python3

import asyncio
import os.path
import sys
from typing import List

from loguru import logger

import logger as loggerLib

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  #Если запускаем из под win    

import importlib

import globals

scada_config=importlib.import_module('projects.'+globals.PROJECT['path']+'.scadaconfig')
import channels.channels
import db_interface
from channels.channelbase import channel_base_init
from exchangeserver import MBServerAdrMapInit, ModbusExchangeServer
from mainpool import MainPool
from mutualcls import Data, EList, SubscriptChannelArg, WSClient
from sourcepool import SourcePool
from webserver.webconnector import setHTTPServer


def init():
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    dbQuie=asyncio.Queue()
    if len(modules:=scada_config.ModuleList):
        sourcePool=SourcePool(modules,loop)
    else:
        sourcePool=None 
    channel_base=channel_base_init(scada_config.channels_config, dbQuie)
    newAddrMap, exchangeBindings = MBServerAdrMapInit(channel_base,scada_config.MBServerAdrMap)
    ModbusExchServer=ModbusExchangeServer(newAddrMap, globals.MBServerParams['host'], globals.MBServerParams['port'],loop=loop)
    httpParams=globals.HTTPServerParams
    httpParams.update({'path':os.path.join(os.path.dirname(__file__),'webserver', 'webdata')})
    sbscrptions:EList[SubscriptChannelArg]=EList()
    ws_clients:EList(WSClient)=EList()
    HTTPServer=setHTTPServer(httpParams, Data(globals.users,channel_base, sbscrptions, ws_clients))
    DBInterface=db_interface.DBInterface(globals.DB_TYPE, globals.DB_PARAMS)
    #HTTPServer=None
    print ('Sources')
    print (sourcePool)
    print ('Channels:')
    print(channel_base)
    # import json
    # print(json.dumps([channel_base.nodesToDictFull()], sort_keys=True, indent=4))
    print(f'Modbus Exchange Server: {globals.MBServerParams["host"]}, {globals.MBServerParams["port"]}')
    print('ExchangeBindings')
    print(exchangeBindings)
    print('HTTPServer:')
    print(f"host:{httpParams.get('host')}, port:{httpParams.get('port')}, wsserver:{httpParams.get('wsserver')}, " if HTTPServer else None )
    
    mainPool=MainPool(loop, sourcePool, channel_base, sbscrptions, ws_clients ,ModbusExchServer, exchangeBindings, HTTPServer, dbQuie, DBInterface)
    logger.info ('init done')
    return mainPool

def test_component():
    loop=asyncio.get_event_loop()
    loggerLib.loggerInit('ERROR')
    logger.info('Starting........')
    httpParams=globals.HTTPServerParams
    channel_base=None
    HTTPServer=setHTTPServer(httpParams, channels.Data(globals.users,channel_base))
    loop.run_forever()

    

def main():
    loggerLib.loggerInit('ERROR')
    logger.info('Starting........')
    mainPool=init()
    mainPool.start()
    

if __name__=='__main__':
    main()
    # test_component()
    