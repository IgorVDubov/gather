
"""
Modbus server class based on Pymodbus Synchronous Server 
--------------------------------------------------------------------------

"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.version import version
from pymodbus.server.sync import StartTcpServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

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

from threading import Thread


import struct 
def packFloatTo2WordsCDAB(f):
    b=[i for i in struct.pack('<f',f)]
    return [b[i+1]*256+b[i] for i in range(0,len(b),2)]



class MBServer():
    def __init__(self,addrMap,host,port):
        #self.context=[slave for slave in self.addrMapInit(addrMap)]
        self.addrMap=addrMap
        self.host=host
        self.port=port
        self.context=self.addrContextInit(addrMap)
        self.idMap=self.idAddrMapDictInit(addrMap)
        pass
        
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
            print(idMap)
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
        StartTcpServer(self.context, address=(self.host,self.port))
    

    def startInThread(self):
        serverThread = Thread(target = self.start)    
        serverThread.daemon=True
        serverThread.start()
        self.serverThread=serverThread
        
    def stopInThread(self):
        self.serverThread.stop()        #TODO передать signal на shutdown TcpServer

    def setDI(self,unit,addr,val):
        # print('setDI')
        self.context[unit].setValues(2,addr,val)

    def setInt(self,unit,addr,val):
        # print('setInt')
        self.context[unit].setValues(4,addr,[val])

    def setFloat(self,unit,addr,val):
        # print('setFloat')
        self.context[unit].setValues(4,addr,packFloatTo2WordsCDAB(val))
    
    def setValue(self,id,val):
        '''
        set value by ID according to addr map
        id:int
        val: [b,b,b...] if DI
             int if HR type int
             float or int as float if HR type float
        '''
        unit,addr,length,valType=self.idMap.get(id,None)
        if addr==None:
            raise ValueError('modbusServer setValue no such ID in map')
            return
        else:
            if valType=='bits':
                if type(val)==list:
                    val=val[:length]            #обрезаем результат в соответствии с заданной длиной записи
                    self.setDI(unit,addr,val)
                else:
                    raise ValueError(f'modbusServer setValue value ({val}) for id:{id} is not list type')
            elif valType=='int':
                if type(val)==int:
                    self.setInt(unit,addr,val)
                else:
                    raise ValueError(f'modbusServer setValue value ({val}) for id:{id} is not int type')
            elif valType=='float':
                if type(val) in (int,float):
                    self.setFloat(unit,addr,val)
                else:
                    raise ValueError(f'modbusServer setValue value ({val}) for id:{id} is not int or float type')





def updating_writer(con):
    i=1
    context=con['con']
    while True:
        i+=1
        context[0].setValues(4,1,[i])
        #context[0].setValues(2,1,[1,0,0,1,0,1])
        sleep(1)

def run_server():
    # ----------------------------------------------------------------------- #
    # initialize your data store
    # ----------------------------------------------------------------------- #
    # The datastores only respond to the addresses that they are initialized to
    # Therefore, if you initialize a DataBlock to addresses of 0x00 to 0xFF, a
    # request to 0x100 will respond with an invalid address exception. This is
    # because many devices exhibit this kind of behavior (but not all)::
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #
    # Continuing, you can choose to use a sequential or a sparse DataBlock in
    # your data context.  The difference is that the sequential has no gaps in
    # the data while the sparse can. Once again, there are devices that exhibit
    # both forms of behavior::
    #
    #     block = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
    #     block = ModbusSequentialDataBlock(0x00, [0]*5)
    #
    # Alternately, you can use the factory methods to initialize the DataBlocks
    # or simply do not pass them to have them initialized to 0x00 on the full
    # address range::
    #
    #     store = ModbusSlaveContext(di = ModbusSequentialDataBlock.create())
    #     store = ModbusSlaveContext()
    #
    # Finally, you are allowed to use the same DataBlock reference for every
    # table or you may use a separate DataBlock for each table.
    # This depends if you would like functions to be able to access and modify
    # the same data or not::
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #     store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    #
    # The server then makes use of a server context that allows the server to
    # respond with different slave contexts for different unit ids. By default
    # it will return the same context for every unit id supplied (broadcast
    # mode).
    # However, this can be overloaded by setting the single flag to False and
    # then supplying a dictionary of unit id to context mapping::
    #
    #     slaves  = {
    #         0x01: ModbusSlaveContext(...),
    #         0x02: ModbusSlaveContext(...),
    #         0x03: ModbusSlaveContext(...),
    #     }
    #     context = ModbusServerContext(slaves=slaves, single=False)
    #
    # The slave context can also be initialized in zero_mode which means that a
    # request to address(0-7) will map to the address (0-7). The default is
    # False which is based on section 4.4 of the specification, so address(0-7)
    # will map to (1-8)::
    #
    #     store = ModbusSlaveContext(..., zero_mode=True)
    # ----------------------------------------------------------------------- #

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
    #
    # TCP with different framer
    # StartTcpServer(context, identity=identity,
    #                framer=ModbusRtuFramer, address=("0.0.0.0", 5020))

    # TLS
    # StartTlsServer(context, identity=identity, certfile="server.crt",
    #                keyfile="server.key", address=("0.0.0.0", 8020))

    # Udp:
    # StartUdpServer(context, identity=identity, address=("0.0.0.0", 5020))

    # socat -d -d PTY,link=/tmp/ptyp0,raw,echo=0,ispeed=9600 PTY,link=/tmp/ttyp0,raw,echo=0,ospeed=9600
    # Ascii:
    # StartSerialServer(context, identity=identity,
    #                    port='/dev/ttyp0', timeout=1)

    # RTU:
    # StartSerialServer(context, framer=ModbusRtuFramer, identity=identity,
    #                   port='/tmp/ttyp0', timeout=.005, baudrate=9600)

    # Binary
    # StartSerialServer(context,
    #                   identity=identity,
    #                   framer=ModbusBinaryFramer,
    #                   port='/dev/ttyp0',
    #                   timeout=1)


if __name__ == "__main__":
    from globals import MBServerAdrMap
    from globals import MBServerParams
    from time import sleep
    #run_server()
    server=MBServer(MBServerAdrMap,MBServerParams)
    server.startInThread()
    i=1
    while True:
        try:
            i+=1
            server.setValue(4209,i)
            server.setValue(4210,-9.99999)
            server.setValue(4207,[1])
            server.setValue(4208,[i%2==True,0,1])
            sleep(1)
        except KeyboardInterrupt:
            break
