from cgitb import handler
from time import time
from unicodedata import name
from unittest import result
from handler_funcs import *
from typing import *
from abc import ABC, abstractmethod
import consts

__all__='''
        Node,
        Programm
'''

def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls

@auto_str
class Params():
    def __init__(self):
        self.result=None
        self.prevVal1=None
        self.timeStamp=time()
        self.length=0
        self.event=False
        self.changeEvent=False

class Chanel(ABC):
    @abstractmethod
    def __call__(self) -> Any:
        ...


class Node(Chanel):
    def __init__(self,id:int,moduleId:str,sourceIndexList:List,handler:callable=None) -> None:
        super().__init__()
        self.id=id
        self.sourceId=moduleId
        self.sourceIndexList=sourceIndexList
        self.source=None
        self.resultIN=None
        
        #self.resultIN=None #входящие данные
        self.resultOUT=None # данные после обработки handler
        if handler==None:
            self.handler=None
        else:
            self.handler=handler
            self.handlerStoredVars=None
    
    def __call__(self):
        if self.source:
            if self.source.result:
                if self.source.type==consts.DI:
                    self.resultIN=[self.source.result[i] for i in self.sourceIndexList]
                elif self.source.type==consts.AI:
                    self.resultIN=self.source.result[0]                                 # только 1-й элемент....  уточнить!!!!!!!!!!!!!!!!!!!!!!
            if self.handler:
                self.resultOUT,self.handlerStoredVars=handler(self.resultIN,self.handlerStoredVars)
            else:
                self.resultOUT=self.resultIN
        else:
            print (f'no source init for node id:{self.id}')
            
class Node_OLD(Chanel):
    def __init__(self,id:int,moduleId:str,type:str,sourceIndexList:List,handler:callable=None) -> None:
        super().__init__()
        self.id=id
        self.sourceId=moduleId
        self.type=type.lower()
        self.sourceIndexList=sourceIndexList
        self.source=None
        self.resultIN=None
        
        #self.resultIN=None #входящие данные
        self.resultOUT=None # данные после обработки handler
        if handler==None:
            self.handler=None
        

        if type(handler)==str:
            possibleFuncs = globals().copy()
            possibleFuncs.update(locals())
            self.funcParams=Params()
            func = possibleFuncs.get(handler)
            if func:
                self.handler=func
                # self.funcParams={}
                self.funcParams=Params()
            else:
                raise NotImplementedError(f"Method {func} not implemented")
        else:
            self.handler=None
    
    def __str__(self):
        return f'id= {self.id} type={self.type} handler:{self.handler} sourceId={self.source.id}, sourceIndexList:{self.sourceIndexList} source^:{id(self.source)}'

    def getResult(self):
        if self.source.result:
            if self.type=='di':
                self.resultIN=[self.source.result[i] for i in self.sourceIndexList]
            elif self.type=='ai':
                self.resultIN=self.source.result[0]             # только 1 элемент!!!!!!!!!!!!!!!!!!!!!!
           

    
class Programm(Chanel):
    def __init__(self,handler:callable,args:any) -> None:
        self.stored:any=None
        self.args=args
        self.handler=handler
    
    def __call__(self) -> Any:
        self.stored=self.handler(self.args,self.stored)


########## test def  ##########
def f1(obj1,stored):
    obj1.resultIN+=10
########## test def  ##########


if __name__ == '__main__':
    n1=Node(1,1,'AI',None,handler=None)
    n1.resultIN=50
    p=Programm(f1,n1)
    p()
    print(n1.resultIN)
