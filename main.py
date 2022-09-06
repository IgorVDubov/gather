from log_module import logger
import log_module
import asyncio
from main_pool import MainPool
import classes
import channelbase
import globals
from exchange_server import ModbusExchangeServer
from source_pool import SourcePool

# def makeChannelBase():


def init():
    loop=asyncio.get_event_loop()
    sourcePool=SourcePool(globals.ModuleList,loop)
    channelBase=channelbase.ChannelBaseInit(globals.nodes, globals.programms)

    # ModbusExchServer=ModbusExchangeServer(globals.MBServerAdrMap,globals.MBServerParams['host'],globals.MBServerParams['port'])
    ModbusExchServer=None
    HTTPServer=None
    if globals.HTTPServer:
        from tornado_serv import TornadoHTTPServerInit
        HTTPServer=TornadoHTTPServerInit(globals.HTTPServerParams['port'])
    mainPool=MainPool(loop, sourcePool, channelBase, ModbusExchServer, HTTPServer)
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
    mainPool.start()
    
    
class Attr(object):
    def __init__(self,obj,attr) -> None:
        self._obj=obj
        self._attr=attr

    @property
    def get(self):
        return getattr(self._obj, self._attr)
    def set(self, value):
        setattr(self._obj,self._attr,value)

    # def __get__(self, __name):
    #     return getattr(self._obj, self._attr)
    # def __set__(self,value) -> None:
    #     setattr(self._obj,self._attr,value)





if __name__=='__main__':
    main()
    