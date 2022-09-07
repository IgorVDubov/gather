'''
модуль обмена данными по запросам от внешних клиентов
реализация : ModBus
'''
import modbus_server
from abc import ABC, abstractmethod

class ExchangeServer(ABC):
    
    
    def start():...
    def stop():...
    def setValue():...
    def getValue():...

    


class ModbusExchangeServer(ExchangeServer):
    def __init__(self,addrMapP:list,serverHost, serverPort):
        
            self.server=modbus_server.MBServer(addrMapP,{'host':serverHost, 'port':serverPort})
    
    def start(self):
        self._mbStart()
    def stop(self):
        self._mbStop()
    def setValue(self,id,value):
        self._mbSetIdValue(id,value)
    def getValue(self, id): 
        return self._mbGetIdValue(id)

    def _mbStart(self):
        self.server.startInThread()
    
    def _mbStop(self):
        self.server.stop()
    
    def _mbSetIdValue(self,id,value):
        self.server.setValue(id,value)
    def _mbGetIdValue(self,id):
        return self.server.getValue(id)

if __name__ == '__main__':
    pass
