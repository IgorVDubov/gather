import asyncio

import modbus_connector
from log_module import logger
from datetime import datetime

class Source(object):
    def __init__(self,module):
        self.id=module['id']
        self.period=module['period']
        self.result=None
        self.moduleType=module['type']
        if module['type']=='ModbusTcp':
            self.connection = modbus_connector.AsyncModbusClient(module['ip'],module['port'],module['unit'],
                                                                module['address'],module['count'],module['format'],
                                                                None if module.get('function')==(None or '') else module.get('function'))
        else:
            raise ValueError (f'No class for type {module["type"]}')
    
    async def read(self):
        self.result= await self.connection.readInputs()
        return self.result
    
    def __str__(self):
        return f' {id(self)}    id:{self.id}, moduleType:{self.moduleType}, period:{self.period}s, {self.connection.__str__()}'

class SourcePool(object):
    def __init__(self,modules,loop=None):
        self.sources=[]
        #self.results=[]
        for module in modules:
            self.sources.append(Source(module))             #TODO помещать сюда только если успешный инит клиента и тест чтения по адресу
        if loop ==None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop=loop
        self.cancelEvent=asyncio.Event()
    
    def __str__(self):
        s=''
        for source in self.sources:
            s+=source.__str__()+'\n'
        return s[:-1]
    
    def start(self):
        self.setTasks()
        self.startLoop()

    def setTasks(self):
        for source in self.sources:
            self.loop.create_task(self.loopSourceReader(source), name='task_'+source.id)
        #self.loop.create_task(self.startQueueReder())

    def startLoop(self):
        try:
            print ('start source read loop')
            self.loop.run_forever()
            print ('afetr run_forever')
        except KeyboardInterrupt:
            logger.info ('************* KeyboardInterrupt *******************')
            self.cancelEvent.set()
            for task in asyncio.all_tasks(loop=self.loop):
                task.cancel()
        finally:
            print ('************* loop close *******************')
            self.loop.stop()

    async def loopSourceReader(self,source):
        logger.debug (f'start loopReader client:{source.id}, period:{source.period}')
        while True:
            try:
                try:
                    beginTime=datetime.now()
                    # print(f'run read def {client.id}')
                    self.result=await source.read()
                    print(f'after read {source.id} def result:{self.result}')

                except asyncio.exceptions.TimeoutError as ex:
                    print(f"!!!!!!!!!!!!!!!!!!! asyncio.exceptions.TimeoutError for {source.id}:",ex)
                # except ModbusExceptions.ModbusException as ex:                                            #TODO взять exception от клиента
                #     print(f"!!!!!!!!!!!!!!!!!!! ModbusException in looper for {client.id} :",ex)
                delay=source.period-(datetime.now()-beginTime)
                if delay<=0:
                    logger.warning(f'Not enof time for read source {source.name} id:{source.id} ')
                await asyncio.sleep(delay)                                                          # TODO вычесть время на чтение??
            except asyncio.CancelledError:
                print("Got CancelledError")
                break
    
    def readAllOneTime(self):
        for source in self.sources:
            #print(f'run read task {source.id}')
            self.loop.run_until_complete(source.read())
            #print(f'next step  after read task {source.result}')
            if not source.result:
                raise ValueError(f'Cant read source {source.id}')

        # Let also finish all running tasks:
        # pending = asyncio.Task.all_tasks()
        # self.loop.run_until_complete(asyncio.gather(*pending))

        
 

