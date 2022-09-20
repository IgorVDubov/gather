import asyncio
from time import time
import json
from logger import logger
import classes
from consts import Consts
from exchange_server import ExchangeServer
from source_pool import SourcePool
from channelbase import ChannelsBase

NODDE_READER_PAUSE=1



class MainPool():
    def __init__(self,  loop:asyncio.AbstractEventLoop, 
                        sourcePool:SourcePool, 
                        channelBase:ChannelsBase,
                        exchangeServer:ExchangeServer=None, 
                        exchangeBindings:dict={},
                        HTTPServer=None):
        '''
        sources: source Module to read
            [{'id':'module_id(str)','type':'ModbusTcp','ip':'192.168.1.99','port':'502','unit':0x1, 'address':51, 'regNumber':2, 'function':4, 'period':0.5},...]
        channeBlase: channe Blase
        MBServAddrMap: ModBus server address map for requesting node data
            [{'unit':0x1, 'map':{
                        'di':[{'id':4207,'addr':1,'len':2},{'id':4208,'addr':3,'len':5},.......],
                        'hr':[{'id':4209,'addr':0,'type':'int'},{'id':4210,'addr':1,'type':'float'},..........] }  }]
        '''
        self.loop = loop
        self.cancelEvent=asyncio.Event()
        self.sourcePool=sourcePool
        self.sourcePool.readAllOneTime()                    #TODO  проверить как работает если нет доступа к source
                                                            #       или заполнять Null чтобы первый раз сработало по изменению
        self.channelBase=channelBase
       
        for node in (Channel for Channel in self.channelBase.channels if isinstance(Channel,classes.Node)):
            for source in self.sourcePool.sources:
                if source.id==node.sourceId:
                    node.source=source
                    break
        for node in (Channel for Channel in self.channelBase.channels if isinstance(Channel,classes.Node)):
            if not node.source:
                print(f'!!!!!!!!!!Cant find source {node.sourceId} for node {node.id}, remove from pool')
                self.channelBase.channels.pop(self.channelBase.channels.index(node))

        #self.cancelEvent=asyncio.Event()
        self.exchServer=exchangeServer
        self.exchangeBindings=exchangeBindings
        self.setTasks()
        self.HTTPServer= HTTPServer
            
    
    def start(self):   
        if self.exchServer:
            self.exchServer.start() 
        logger.info ('start source reader pool')
        self.startLoop()

    def startLoop(self):
        try:
            print ('start source read loop')
            self.loop.run_forever()
            print ('afetr run_forever')
        except KeyboardInterrupt:
            logger.info ('************* KeyboardInterrupt *******************')
            self.cancelEvent.set()
            for task in asyncio.all_tasks(loop=self.loop):
                print(f'Task {task.get_name()} cancelled')
                task.cancel()
            
        finally:
            if self.HTTPServer:
                print('HTTPServer stop')
                self.HTTPServer.stop()
                asyncio.run(self.HTTPServer.close_all_connections())
            self.loop.stop()
            print ('************* main loop close *******************')

    def setTasks(self):
            self.loop.create_task(self.startReader())
    

    async def startReader(self):                                
        # print ('start results Reader')
        # try:
            while True:
                before=time()
                for channel in self.channelBase.channels:
                    channel()
                                    
                for channelId, binding in self.exchangeBindings.items():
                    self.exchServer.setValue(channelId, binding.value)
                
                if len(self.HTTPServer.request_callback.wsClients):
                    for wsClient in self.HTTPServer.request_callback.wsClients:
                        wsClient.write_message(json.dumps(self.channelBase.toDict(), default=str))

                delay=NODDE_READER_PAUSE-(time()-before)
                if delay<=0:
                    logger.warning(f'Not enough time for channels calc loop, {len(self.channelBase.channels)} channels ')
                await asyncio.sleep(delay)
        
        # except asyncio.CancelledError:
        #     print('CancelledEvent in startReader')
        # except Exception as e:
        #     logger.error(e)
        # finally:
        #     print('startReader stops by exception ')
        #     return

        
