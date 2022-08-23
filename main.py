from channel_handlers import programm_1
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
    
    
class Attr(object):
    def __init__(self,obj,attr) -> None:
        self._obj=obj
        self._attr=attr

    # @property
    # def self(self):
    #     return self.getattr(self._obj, self._attr)
    # @self.setter
    # def self(self, value):
    #     setattr(self._obj,self._attr,value)

    def __get__(self, __name):
        return getattr(self._obj, self._attr)
    def __set__(self,value) -> None:
        setattr(self._obj,self._attr,value)





if __name__=='__main__':
    # main()
    import channel_handlers
    nodes=[classes.Node(**{'id':4208,'moduleId':'test2','type':'DI','sourceIndexList':[0,1]})]
    nodes[0].result=1
    print(nodes[0])
    print(f'node {nodes[0].id} n={nodes[0].result}')
    # programms=[{'id':10001,'handler':channel_handlers.programm_1,'args':{'result':(4208,'result')},'stored':{'stored1':0}}]
    prg={'id':10001,'handler':channel_handlers.programm_1,'args':{'result':(4208,'result')},'stored':{'stored1':0}}
    for name, var_params  in prg['args'].items():
        id, var = var_params
        n=next(filter(lambda node: node.id == id, nodes))

        r=getattr(n,var)
        r1=Attr(n,var)
    # for prg in programms:
        # programm=
    r2=n.result

    print(r2)
    r2=3
    print(n)
    print(r1)
    print(f'node {nodes[0].id} n={nodes[0].result}')
    # prg=classes.Programm(**programm)
    # print(prg)