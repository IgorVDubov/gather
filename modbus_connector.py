from pymodbus.compat import IS_PYTHON3, PYTHON_VERSION
if IS_PYTHON3 and PYTHON_VERSION >= (3, 4):
    from pymodbus.client.asynchronous import async_io
    import asyncio
    from asyncio.tasks import gather
    from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
    from pymodbus.client.asynchronous import schedulers
else:
    import sys
    sys.stderr("This example needs to be run only on python 3.4 and above")
    sys.exit(1)
import pymodbus.exceptions as ModbusExceptions
import time

import consts
from log_module import logger
from modbus_emulator import TestAsyncModbusClient
from bpacker import unpackCDABToFloat


class AsyncModbusConnection(object):
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.loop=None
        self.start()
    
    

    def start(self):
        self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)
        if self.ip[:4].lower()=='test':
            loop, self.connection = TestAsyncModbusClient(schedulers.ASYNC_IO, host=self.ip, port=self.port,loop=self.loop)
        else:
            loop, self.connection = ModbusClient(schedulers.ASYNC_IO, host=self.ip, port=self.port,loop=self.loop)
        print(f"Client ip:{ self.ip}, connection:{self.connection.connected} ")
    
class AsyncModbusClient(AsyncModbusConnection):
    """
    AsyncModbusClient 
    inits AsyncModbusConnection
    metod: readInputs fuction 3 and 4
    format: AI=1 return float / DI=2 return [bitsArr]
    """
    AI=1
    DI=2
    
    def __init__(self,ip,port,unit,address,count,format,function=None):
        self.address=address
        self.regCount=count
        self.unit=unit
        if format==consts.AI:
            self.format=self.AI
        elif format==consts.DI:
            self.format=self.DI
        self.function=function

        self.error=None
        super().__init__(ip,port)

    def __str__(self):
        return f'ip:{self.ip}, port:{self.port}, unit:{self.unit}, address:{self.address}, regCount:{self.regCount}, function:{self.function}'

    async def readInputs(self):
        connection=self.connection.protocol
        result=[]
        
        if self.function==4:
            readResult = await connection.read_input_registers(self.address, self.regCount, unit=self.unit)
            if not(readResult.isError()):
                if self.format==self.DI:
                    result=[reg for reg in readResult.registers]
                elif self.format==self.AI:
                    result=[unpackCDABToFloat (readResult.registers,2)]
            else:
                print ('*'*20,f'raise error:{readResult}')
                raise ModbusExceptions.ModbusException(result)
        elif self.function==3:
            readResult = await connection.read_holding_registers(self.address, self.regCount, unit=self.unit)
            if not(readResult.isError()):
                result=[reg for reg in readResult.registers]
            else:
                print ('*'*20,f'raise error:{readResult}')
                raise ModbusExceptions.ModbusException(result)
        elif self.function==2:
            readResult = await connection.read_discrete_inputs(self.address, self.regCount, unit=self.unit)
            if not(readResult.isError()):
                result = readResult.bits
            else:
                print ('*'*20,f'raise error:{readResult}')
                raise ModbusExceptions.ModbusException(result)

        #print(result)
        lock = asyncio.Lock()
        async with lock:
            self.result=result
        return result

# if __name__ == '__main__':
#    startModbusLoop(diModules)
   