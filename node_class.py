from time import time
from handler_funcs import *

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

    


class Node(object):
    def __init__(self,id,moduleId,type,sourceIndexList,handler=None) -> None:
        super().__init__()
        self.id=id
        self.sourceId=moduleId
        self.type=type.lower()
        self.sourceIndexList=sourceIndexList
        self.source=None
        self.resultIN=None
        
        #self.resultIN=None #входящие данные
        self.resultOUT=None # данные после обработки handler
        
        possibleFuncs = globals().copy()
        possibleFuncs.update(locals())
        self.funcParams=Params()
        if handler:
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
           

    
