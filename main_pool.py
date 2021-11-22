import asyncio
from log_module import logger
from datetime import datetime

from consts import Consts
from exchange_server import ExchangeServer
from source_pool import SourcePool

NODDE_READER_PAUSE=1



class MainPool():
    def __init__(self,sources,nodes,exAddrMap,exchServerParams, HTTPServer=None):
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
        self.loop = asyncio.get_event_loop()
        self.sourcePool=SourcePool(sources,self.loop)
        self.sourcePool.readAllOneTime()                    #TODO  проверить как работает если нет доступа к source
        self.nodes=nodes
        for node in self.nodes:
            for source in self.sourcePool.sources:
                if source.id==node.sourceId:
                    node.source=source
        for node in self.nodes:
            if not node.source:
                raise ValueError(f'Cant find source {node.sourceId} for node {node.id}')
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
            self.loop.create_task(self.startReader())
    
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


    async def startReader(self):
        print ('start results Reader')
        try:
            while True:
                for node in self.nodes:
                    node.getResult()
                    if node.resultIN:
                        self.nodeHandler(node)
                    else:
                        print('No result')
                await asyncio.sleep(NODDE_READER_PAUSE)

        except asyncio.CancelledError:
            print('CancelledError')
        except Exception as e:
            logger.error(e)
        finally:
            print('startReader finally')
            return

        
