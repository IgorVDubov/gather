
"""
Modbus server class based on Pymodbus Synchronous Server 
--------------------------------------------------------------------------

"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
import asyncio
import struct
from threading import Thread

from pymodbus.datastore import (ModbusSequentialDataBlock, ModbusServerContext,
                                ModbusSlaveContext, ModbusSparseDataBlock)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.async_io import ModbusTcpServer, _serverList
from pymodbus.version import version

from myexceptions import ConfigException, ModbusExchangeServerException

#from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
# import logging
# FORMAT = ('%(asctime)-15s %(threadName)-15s'
#           ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
# logging.basicConfig(format=FORMAT)
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)


def packFloatTo2WordsCDAB(f):
    b=[i for i in struct.pack('<f',f)]
    return [b[i+1]*256+b[i] for i in range(0,len(b),2)]


class MBServer(ModbusTcpServer):
    def __init__(self,addrMap,serverParams,**kwargs):
        self.loop=kwargs.get("loop") or asyncio.get_event_loop()
        self.addrMap=addrMap
        self.serverParams=serverParams
        self.context=self.addrContextInit(addrMap)
        self.idMap=self.idAddrMapDictInit(addrMap)
        super().__init__(self.context,address=(self.serverParams['host'],self.serverParams['port']))

        
    def idAddrMapDictInit(self,addrMap):
        '''
        makes dict {id:(unut,adr,length,type)}
        '''
        idMap={}
        for unit in addrMap:
            di=unit['map'].get('di',None)
            if di:
                for device in di:
                    idMap[device['id']]=(unit['unit'],device['addr'],device['len'],'bits')
            hr=unit['map'].get('hr',None)
            if hr:
                for device in hr:
                    valLength=2 if device['type']=='float' else 1
                    idMap[device['id']]=(unit['unit'],device['addr'],valLength,device['type'])
            ir=unit['map'].get('ir',None)
            if ir:
                for device in ir:
                    valLength=2 if device['type']=='float' else 1
                    idMap[device['id']]=(unit['unit'],device['addr'],valLength,device['type'])
            # print(idMap)
        return idMap

    def addrContextInit(self,addrMap:dict):
        '''
        MBServerAdrMap=[
            {'unit':0x1, 
                'map':{
                    'di':[{'id':4207,'addr':1,'len':2},
                          {'id':4208,'addr':3,'len':2}],
                    'hr':[{'id':4209,'addr':0,'type':'int'},
                          {'id':4210,'addr':1,'type':'float'}]
                }
            }]
        returns ModbusServerContext
        '''
        slaves={}
        #context=None
        for unit in addrMap:
            slaveContext=ModbusSlaveContext()
            ci=unit['map'].get('ci',None)
            di=unit['map'].get('di',None)
            hr=unit['map'].get('hr',None)
            ir=unit['map'].get('ir',None)
            
            if ci:
                maxAddr=0
                length=1
                for device in di:
                    if device['addr']>maxAddr:
                        maxAddr=device['addr']
                        length=device['len']
                    else:
                        length=device['len']
                ciLength=maxAddr+length
            else:
                ciLength=1
            ciDataBlock=ModbusSequentialDataBlock(1,[0]*ciLength) 
            slaveContext.register(1,'c',ciDataBlock) 
            if di:
                maxAddr=0
                length=1
                for device in di:
                    if device['addr']>maxAddr:
                        maxAddr=device['addr']
                        length=device['len']
                    else:
                        length=device['len']
                diLength=maxAddr+length
            else:
                diLength=1
            diDataBlock=ModbusSequentialDataBlock(1,[0]*diLength) 
            slaveContext.register(2,'d',diDataBlock) 
            if hr:
                maxAddr=0
                length=0
                for device in hr:
                    if device['addr']>maxAddr:
                        maxAddr=device['addr']
                        length=2 if device['type']=='float' else 1
                    else:
                        length=2 if device['type']=='float' else 1
                hrLength=maxAddr+length
            else:
                hrLength=1
            hrDataBlock=ModbusSequentialDataBlock(1,[0]*hrLength) 
            slaveContext.register(3,'h',hrDataBlock)
            if ir:
                maxAddr=0
                length=1
                for device in ir:
                    if device['addr']>maxAddr:
                        maxAddr=device['addr']
                        length=2 if device['type']=='float' else 1
                    else:
                        length=2 if device['type']=='float' else 1
                irLength=maxAddr+length
            else:
                irLength=1
            irDataBlock=ModbusSequentialDataBlock(1,[0]*irLength)
            slaveContext.register(4,'i',irDataBlock)
            # if len(addrMap)==1:
            #     context=ModbusServerContext(slaves=slaveContext, single=True)
            # else:
            slaves[unit['unit']]=slaveContext
        #if context ==None:
        context=ModbusServerContext(slaves=slaves, single=False)
        return context

    def start(self):
        # StartTcpServer(self.context, address=(self.serverParams['host'],self.serverParams['port']))
        self.loop.create_task(self.serve_forever(),name='Exchange_Server')
    
    def stop(self):
        # self.server_close()
         asyncio.create_task(self.shutdown())
        

    def startInThread(self):
        serverThread = Thread(target = self.start)    
        serverThread.daemon=True
        serverThread.start()
        self.serverThread=serverThread
        
    def stopInThread(self):
        self.serverThread.stop()        #TODO передать signal на shutdown TcpServer

    def setCI(self,unit,addr,val):
        # print('setDI')
        self.context[unit].setValues(1,addr,val)
    
    def setDI(self,unit,addr,val):
        # print('setDI')
        self.context[unit].setValues(2,addr,val)

    def setInt(self,unit,addr,val):
        # print('setInt')
        self.context[unit].setValues(3,addr,[val])

    def setFloat(self,unit,addr,val):
        # print('setFloat')
        self.context[unit].setValues(4,addr,packFloatTo2WordsCDAB(val))
    
    def setValue(self,id,val):
        '''
        set value by ID according to addr map
        if val=None NOT SET value!!!!!
        id:int
        val: [b,b,b...] if DI
             int if HR type int
             float or int as float if HR type float
        '''
        try:
            unit,addr,length,valType=self.idMap.get(id,None)
        except TypeError:
            raise ConfigException(f'ModBus server[setValue]: cant get mnapping for id:{id}')
        if addr==None or val==None:                                                             
            # raise ModbusExchangeServerException('modbusServer setValue no such ID in map')
            return
        else:
            if valType=='bits':
                if type(val)==list:
                    val=val[:length]            #обрезаем результат в соответствии с заданной длиной записи
                    self.setDI(unit,addr,val)
                else:
                    raise ModbusExchangeServerException(f'modbusServer setValue value ({val}) for id:{id} is not list type')
            elif valType=='coil':
                if type(val)==bool:
                    self.setCI(unit,addr,val)
                else:
                    raise ModbusExchangeServerException(f'modbusServer setValue value ({val}) for id:{id} is not bool type')
            elif valType=='int':
                if type(val)==int:
                    self.setInt(unit,addr,val)
                else:
                    raise ModbusExchangeServerException(f'modbusServer setValue value ({val}) for id:{id} is not int type')
            elif valType=='float':
                if type(val) in (int,float):
                    self.setFloat(unit,addr,val)
                else:
                    raise ModbusExchangeServerException(f'modbusServer setValue value ({val}) for id:{id} is not int or float type')





def updating_writer(con):
    i=1
    context=con['con']
    while True:
        i+=1
        context[0].setValues(4,1,[i])
        #context[0].setValues(2,1,[1,0,0,1,0,1])
        sleep(1)

def run_server():

    store = ModbusSlaveContext(
        #di=ModbusSequentialDataBlock(1, [1]*16),
        di=None,
        ir=ModbusSequentialDataBlock(1, [65534,277,3,0]+packFloatTo2WordsCDAB(1.75))
        )
    # store = ModbusSlaveContext(
    #     ir=ModbusSequentialDataBlock(0, [4]*1))
    # store = ModbusSlaveContext(
        # di=ModbusSequentialDataBlock(0, [1]*1),
    #     co=ModbusSequentialDataBlock(0, [2]*1),
    #     hr=ModbusSequentialDataBlock(0, [3]*1),
    #     ir=ModbusSequentialDataBlock(0, [4]*1))

    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    # If you don't set this or any fields, they are defaulted to empty strings.
    # ----------------------------------------------------------------------- #
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()

    # ----------------------------------------------------------------------- #
    # run the server you want
    # ----------------------------------------------------------------------- #
    # Tcp:
   
   
    updating_writer_thread = Thread(target = updating_writer, args = [{'con':context}])    
    updating_writer_thread.daemon=True
    updating_writer_thread.start()

    StartTcpServer(context, identity=identity, address=("192.168.1.200", 5020))
    print ('afterstart')

async def call(server):
    i=1
    while True:
        try:
            i+=1
            server.setValue(4001,i)
            server.setValue(4002,i+50)
            # server.setValue(4003,[1])
            # server.setValue(4004,[i%2==True,0,1])
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break

from time import sleep


def main(loop):
    #run_server()
    MBServerParams={'host':'127.0.0.1','port':5021}
    mb_server_addr_map=[
    {'unit':0x1, 'map':{
        # 'di':[{'id':4001, 'attr':'result', 'addr':0, 'len':16}
        #     ],
        'ir':[
            {'id':4001, 'attr':'result', 'addr':1, 'type':'int'},
            {'id':4002, 'attr':'result', 'addr':2, 'type':'float'},
            # {'id':4003, 'attr':'result', 'addr':3, 'type':'int'},
            # {'id':4004, 'attr':'result', 'addr':4, 'type':'int'},
        ]
        }
    }]
 
    # server=loop.run_until_complete(StartAsyncTcpServer(mb_server_addr_map,MBServerParams,loop=loop))
    server=MBServer(mb_server_addr_map,MBServerParams,loop=loop)
    # l=_serverList(server,[],True)
    # l.run()
    loop.create_task(call(server))
    loop.create_task(server.serve_forever())
    # loop.run_forever()
    # server.start()
    # server.startInThread()

if __name__ == "__main__":
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    main(loop)
    loop.run_forever()

