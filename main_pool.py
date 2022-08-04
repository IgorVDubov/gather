import asyncio
from datetime import datetime
from typing import List
from log_module import logger
from datetime import datetime

from consts import Consts
from exchange_server import ExchangeServer
from source_pool import SourcePool

NODDE_READER_PAUSE=1



class MainPool():
    def __init__(self,  loop:asyncio.AbstractEventLoop, 
                        sourcePool:SourcePool, 
                        nodes:List,
                        exAddrMap,
                        exchServerParams, 
                        HTTPServer=None):
        '''
        sources: source Moduke to read
            [{'id':'module_id(str)','type':'ModbusTcp','ip':'192.168.1.99','port':'502','unit':0x1, 'address':51, 'regNumber':2, 'function':4, 'period':0.5},...]
        nodes: single Node params in suorce + handler function
            Node(id,moduleId,type,sourceIndexList,handler)
        MBServAddrMap: ModBus server address map for requesting node data
            [{'unit':0x1, 'map':{
                        'di':[{'id':4207,'addr':1,'len':2},{'id':4208,'addr':3,'len':5},.......],
                        'hr':[{'id':4209,'addr':0,'type':'int'},{'id':4210,'addr':1,'type':'float'},..........] }  }]
        '''
        self.loop = loop
        self.sourcePool=sourcePool
        self.sourcePool.readAllOneTime()                    #TODO  проверить как работает если нет доступа к source
                                                            #       или заполнять Null чтобы первый раз сработало по изменению
        self.nodes=nodes
        for node in self.nodes:
            for source in self.sourcePool.sources:
                if source.id==node.sourceId:
                    node.source=source
                    break
        for node in self.nodes:
            if not node.source:
                print(f'!!!!!!!!!!Cant find source {node.sourceId} for node {node.id}, remove from pool')
                self.nodes.pop(self.nodes.index(node))

        #self.cancelEvent=asyncio.Event()
        self.exchServer=ExchangeServer(Consts.MODBUS,exAddrMap,exchServerParams)
        self.setTasks()
        self.webApp=None
        if HTTPServer:
            # from async_HTTP_server import asyncHTTPserver
            # self.webApp=asyncHTTPserver()
            from tornado_serv import TornadoHTTPServerInit
            self.webApp=TornadoHTTPServerInit()
    
    def start(self):   
        self.exchServer.start() 
        # if self.webApp:
        #     self.webApp.start()
        self.sourcePool.start()

        logger.info ('start source reader pool')


    def setTasks(self):
            self.loop.create_task(self.calcChannelsLoop())
    
    def nodeHandler(self,node):
        if node.handler:
            node.funcParams=node.handler(node.resultIN, globalParams=node.funcParams)
            
            if node.funcParams.changeEvent:
                node.funcParams.changeEvent=False
            if node.funcParams.event:
                self.exchServer.SetValue(node.id,node.resultIN)
                #print(f'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} result:{node.funcParams.prevVal1} length:{node.funcParams.length}s ')
                node.funcParams.event=False
        else:
            self.exchServer.SetValue(node.id,node.resultIN)

    # def nodeHandler(self,node):
    #     node.funcParams=node.handler(node)
    #     if node.funcParams.event:
    #         print(f'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} result:{node.funcParams.prevVal1} length:{node.funcParams.length}s ')
    #         node.funcParams.event=False


    async def calcChannelsLoop(self):
        print ('start calcChannelsLoop')
        try:
            while True:
                before=datetime.now()
                for channel in self.channels:
                    channel.getResult()
                    if channel.resultIN:
                        self.nodeHandler(channel)
                    else:
                        print('No result')
                delay=NODDE_READER_PAUSE-(datetime.now()-before)
                if delay<=0:
                    logger.warning(f'Not enough time for channels calc loop, {len(self.channels)} channels ')
                await asyncio.sleep(delay)

        except asyncio.CancelledError:
            print('CancelledError')
        except Exception as e:
            logger.error(e)
        finally:
            print('calcChannelsLoop finally')
            return

        
