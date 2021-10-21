'''
модуль обмена данными по запросам от внешних клиентов
реализация : ModBus
'''
import modbus_server
from consts import Consts 

class ExchangeServer(object):
    def __init__(self,serverType,addrMapP,serverParams):
        if serverType==Consts.MODBUS:
            self.server=modbus_server.MBServer(addrMapP,serverParams)
            self.start=self.mbStart
            self.stop=self.mbStop
            self.SetValue=self.mbSetIdValue
    
    def start():pass
    def stop():pass
    def SetValue():pass

    def mbStart(self):
        self.server.startInThread()
    
    def mbStop(self):
        self.server.stop()
    
    def mbSetIdValue(self,id,value):
        self.server.setValue(id,value)





if __name__ == '__main__':
    pass
