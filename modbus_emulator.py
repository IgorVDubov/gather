import asyncio
import random
from time import strftime, gmtime, sleep
from bpacker import packFloatToCDAB

class TestResult:
    def __init__(self):
        self.registers=[]
        self.bits=[]
    def isError(self):
        return False

class TestProtocol:
    def __init__(self,testType):
        self.result=TestResult()
        self.testType=testType

    async def read_input_registers(self, address, regNumber, unit):     #func4
        #print ('in read_input_registers')
        registers=[] 
        if self.testType==1:
            for _ in range(regNumber):  # все биты random
                registers.append(random.randint(0,1))
        elif self.testType==2:                # 0 бит random
            registers.append(random.randint(0,1))
            for _ in range(1,regNumber):
                registers.append(0)
        elif self.testType==3:                                # 0 бит по программе цикла (секунды любой минуты)
            registers.append(1)  # выставляем  бит0= 1
            cycle=[(0,2,False),(3,5,True),(6,8,False),(9,13,True),(14,19,False)
                   # ,(20,22,False),(23,25,True),(26,28,False),(29,33,True),(34,39,False)
                   # ,(40,42,False),(43,45,True),(46,48,False),(49,53,True),(54,59,False)
                    ]
            sec=int(strftime("%S", gmtime()))
            for period in cycle:
                if sec>= period[0] and sec<=period[1]:
                    registers.append(int(period[2]))
            for _ in range(0,regNumber-len(registers)):     #заполняем остаток 0
                registers.append(0)  
            #print(f'sec:{sec} reg:{registers}')
        elif self.testType==4:                                # аналоговый сигнал 1-10в по программе цикла (секунды любой минуты)
            minVal=1   #минимум 
            maxVal=9   #максимум 
            frontLength=2  #длина фронта
            cycle=[(0,14,maxVal),(15,19,minVal),(20,29,maxVal),(30,44,minVal),(54,59,maxVal)]
            sec=int(strftime("%S", gmtime()))
            for period in cycle:
                if sec>= period[0] and sec<=period[1]:
                    registers.append(period[2])
            for _ in range(1,regNumber):
                registers.append(0)
            #print(f'sec:{sec} reg:{registers}')
        
        elif self.testType==5:                # float random меняется каждые N сек
            minVal=7   #минимум 
            maxVal=60   #максимум 
            minValTreshold=2  #амплитуда
            minValTreshold=15  #амплитуда
            cycle=[(0,10,maxVal),(11,20,minVal),(21,30,maxVal),(31,40,minVal),(41,59,maxVal)]
            sec=int(strftime("%S", gmtime()))
            for period in cycle:
                if sec>= period[0] and sec<=period[1]:
                    tr=minValTreshold if period[2]==minVal else minValTreshold
                    tr=random.random()*tr/2
                    registers=packFloatToCDAB(period[2] + tr)
        self.result.registers=registers
        await asyncio.sleep(0.01)
        #print (f'out read_input_registers {self.result.registers}')
        return  self.result 

    async def read_discrete_inputs(self, address, regNumber, unit):         #func2
        bits=[]
        if self.testType==1:
            for _ in range(regNumber):
                bits.append(True==random.randint(0,1))
        if self.testType==2:
            bits.append(True==random.randint(0,1))
            for _ in range(1,regNumber):
                bits.append(False)
        elif self.testType==3:                                # 0бит=1 1бит по программе цикла (секунды любой минуты)
            bits.append(1)  # выставляем  бит0= 1
            cycle=[(0,2,False),(3,5,True),(6,8,False),(9,13,True),(14,19,False)
                   # ,(20,22,False),(23,25,True),(26,28,False),(29,33,True),(34,39,False)
                   # ,(40,42,False),(43,45,True),(46,48,False),(49,53,True),(54,59,False)
                    ]
            sec=int(strftime("%S", gmtime()))
            for period in cycle:
                if sec>= period[0] and sec<=period[1]:
                    bits.append(period[2])
            for _ in range(0,regNumber-len(bits)):
                bits.append(False)

        self.result.bits=bits
        await asyncio.sleep(0.01)
        return  self.result
    

class TestModbusConnection:
    def __init__(self,testType):
        self.connected=True
        self.protocol=TestProtocol(testType)
    
class TestAsyncModbusClient:
    """
    Эмулятор модбас клиента
    """
    def __new__(self,schedulers, host, port,loop):
        self.schedulers=schedulers
        self.host=host
        
        self.port=port
        self.loop=loop
        self.connection= TestModbusConnection(int(host[4:]))
        return self.loop, self.connection

if __name__=="__main__":
    loop,m=TestAsyncModbusClient(None, None, None,loop=None)
    while True:
        #print(f'{strftime("%S", gmtime())} {" "*(5+15*m.protocol.read_input_registers(1, 1, 1).registers[0])}*')
        print(m.protocol.read_input_registers(1, 16, 1).registers)
        sleep(1)
