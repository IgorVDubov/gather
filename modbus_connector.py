import asyncio
from typing import Any
from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
from pymodbus.client.asynchronous import schedulers
import myexceptions

from consts import AI,DI
from logger import logger
from modbus_emulator import TestAsyncModbusClient
from bpacker import unpackCDABToFloat
from abc import ABC, abstractmethod

class AsyncBaseModbusClient(ABC):
    ip = None
    port = None
    connection = None

    def start():...
    @property
    def connected(self):...
    async def readInputRegisters_F4(address:int, regCount:int, unit:int):...
    async def readHoldingRegisters_F3(address:int, regCount:int, unit:int):...
    async def readDiscreteInputs_F2(address:int, regCount:int, unit:int):...
    async def writeCoil_F5(address:int, value:bool, unit:int):...
    async def writeWord_F6(address:int, value:int, unit:int):...



class AsyncModbusClient(AsyncBaseModbusClient):
    def __init__(self,ip,port,loop=None):
        self.ip=ip
        self.port=port
        self.loop=loop
        self.start()
    
    

    def start(self):
        if not self.loop:
            self.loop = asyncio.get_event_loop()
            asyncio.set_event_loop(self.loop)
        if self.ip[:4].lower()=='test':
            loop, self.connection = TestAsyncModbusClient(schedulers.ASYNC_IO, host=self.ip, port=self.port,loop=self.loop)
        else:
            loop, self.connection = ModbusClient(schedulers.ASYNC_IO, host=self.ip, port=self.port,loop=self.loop)
        print(f"Client ip:{ self.ip}, connection:{self.connection.connected} ")

    @property
    def connected(self):
        return self.connection.connected
    async def readInputRegisters_F4(self, address:int, regCount:int, unit:int):
        return await self.connection.read_input_registers(address, regCount, unit=self.unit)
    async def readHoldingRegisters_F3(address:int, regCount:int, unit:int):...
    async def readDiscreteInputs_F2(address:int, regCount:int, unit:int):...
    async def writeCoil_F5(address:int, value:bool, unit:int):...
    async def writeWord_F6(address:int, value:int, unit:int):...
    
class AsyncModbusConnection(AsyncModbusClient):
    """
    AsyncModbusClient 
    inits AsyncModbusConnection
    metod: readInputs fuction 3 and 4
    format: AI=1 return float / DI=2 return [bitsArr]
    """
    AI=1
    DI=2
    
    def __init__(self,ip,port,unit,address,count,format,function=None,loop=None):
        self.address=address
        self.regCount=count
        self.unit=unit
        if format==AI:
            self.format=self.AI
        elif format==DI:
            self.format=self.DI
        self.function=function

        self.error=None
        super().__init__(ip,port)

    def __str__(self):
        return f'ip:{self.ip}, port:{self.port}, unit:{self.unit}, address:{self.address}, regCount:{self.regCount}, function:{self.function}'

    async def read(self):
        connection=self.connection.protocol
        result=[]
        try:
            if self.function==4:
                readResult = await connection.read_input_registers(self.address, self.regCount, unit=self.unit)
                if not(readResult.isError()):
                    if self.format==self.DI:
                        result=[reg for reg in readResult.registers]
                    elif self.format==self.AI:
                        result=[unpackCDABToFloat (readResult.registers,2)]
                else:
                    # print ('*'*20,f'raise error:{readResult}')
                    self.error=readResult
                    raise myexceptions.ModbusException(readResult)
            elif self.function==3:
                readResult = await connection.read_holding_registers(self.address, self.regCount, unit=self.unit)
                if not(readResult.isError()):
                    result=[reg for reg in readResult.registers]
                else:
                    # print ('*'*20,f'raise error:{readResult}')
                    self.error=readResult
                    raise myexceptions.ModbusException(readResult)
            elif self.function==2:
                readResult = await connection.read_discrete_inputs(self.address, self.regCount, unit=self.unit)
                if not(readResult.isError()):
                    result = readResult.bits
                else:
                    self.error=readResult
                    # print ('*'*20,f'raise error:{readResult}')
                    raise myexceptions.ModbusException(readResult)
        except AttributeError:
            self.error='Connection error'
            result=None
            # raise ModbusExceptions.ConnectionException(result)
        #print(result)
        lock = asyncio.Lock()
        async with lock:
            self.result=result
        return result

    async def writeRegister(self,reg:int,value):
        ...

# if __name__ == '__main__':
#    startModbusLoop(diModules)
   