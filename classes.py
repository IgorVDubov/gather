from cgitb import handler
from time import time
from unicodedata import name
from unittest import result
from typing import *
from abc import ABC, abstractmethod
import inspect
import consts


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls

def getDeepAttr(obj:type, attr:str):
    '''
    return  instance subobjects attributes value
    obj - class instance
    attr - attributes: example 'a', 'vars.b' if vars instance of Var with attr 'b'
    '''
    s=''
    for i in range(0,len(attr)):
        if attr[i]=='.':
            result=getattr(obj,s)
            s=''
            obj=result
            continue
        s+=attr[i]
    return getattr(obj,s)

def getSubObjectAttr(obj:type, attr:str):
    '''
    return  subobjects instance and  attribute name for getattr
    obj - class instance
    attr - attributes: example 'a', 'vars.b' if vars instance of Var with attr 'b'
    return (subobj:type, name:str)
    example: getSubObjectAttr(someObj,'vars.b') returns (vars_instance,'b')
    '''
    s=''
    for i in range(0,len(attr)):
        if attr[i]=='.':
            result=getattr(obj,s)
            s=''
            obj=result
            continue
        s+=attr[i]
    return obj,s

class Var:
    def __init__(self,name:str, obj:type, objAttrName:str) -> None:
    # def __init__(self,name:str, obj:type, objAttrName:str, readonly:bool=False) -> None:
        self.name=name
        self.obj,self.objAttrName=getSubObjectAttr(obj,objAttrName)
        self.objAttrName=objAttrName
        # self.readonly=readonly

class BindVars:
    '''
    Binds dynamic added self instsnce attribute to another instance attribute
    can bins subobject attr in format 'instance_attr.a'
    '''
    # vars=[]

    def __init__(self):
        self.vars=[]

    def __str__(self):
        s=''
        for v in self.vars:
            s+=f'{v.name}<-{v.obj.id if hasattr(v.obj,"id") else v.obj}.{v.objAttrName} '
        return s
    
    def __repr__(self):
        # s=''
        # for v in self.vars:
        #     s+=f'{v.name}<-{v.obj.id if hasattr(v.obj,"id") else v.obj}.{v.objAttrName} '
        # return s
        return self.__str__()

    # def add(self,name:str, obj:type, objAttrName:str):
    #     return self._add(name, obj, objAttrName)

    def add(self, name:str, obj:type, objAttrName:str):
    # def add(self, name:str, obj:type, objAttrName:str, readonly=False):
        '''
        adds self attribute (name) bindig to instance (obj) attribute  (objAttrName)
        '''
        if not ((inspect.isclass(type(obj)) and not type(obj) == type )
                and isinstance( objAttrName, str) 
                and isinstance( name, str)):
            raise Exception(f'Wrong argument type adding binding, args: {name=}, {obj=}, {objAttrName=}')
        if not hasattr(obj, objAttrName):
            raise Exception(f'Instance {obj} has no attribute {objAttrName}')

        fget = lambda self: self._getProperty( name )
        fset = lambda self, value: self._setProperty( name, value )
        
        setattr( self, '_' + name, None )
        setattr( self.__class__, name, property( fget = fget, fset = fset ) )
        self.vars.append(Var(name, obj, objAttrName))
    
    def _getBinding(self, attrName):
        try:
            if found:=next(filter(lambda var: var.name == attrName, self.vars)):
                # return found.obj, found.objAttrName, found.readonly
                return found.obj, found.objAttrName
        except StopIteration:
            found=None
        return None, None
        # return None, None, None
        

    def _setProperty( self, name, value ):
        setattr( self, '_' + name, value )
        obj, objAttrName= self._getBinding(name)
        setattr( obj, objAttrName, value )
        # obj, objAttrName, readonly= self._getBinding(name)
        # if not readonly:
        #     setattr( obj, objAttrName, value )

    def _getProperty( self, name ):
        obj, objAttrName= self._getBinding(name)
        # return getattr( self, '_' + name )
        return getattr( obj, objAttrName )

class Vars:
    '''
    dynamic added attribute with setters and getters
    '''
    
    def add(self, name:str, defaultValue=None):
    # def add(self, name:str, obj:type, objAttrName:str, readonly=False):
        '''
        adds attribute to instance
        name:str  attribute name
        [defaultValue]:Any   default Value
        '''
        if not isinstance( name, str):
            raise Exception(f'Wrong argument type adding arg: {name=}')

        fget = lambda self: self._getProperty( name )
        fset = lambda self, value: self._setProperty( name, value )
        
        setattr( self, '_' + name, defaultValue )
        setattr( self.__class__, name, property( fget = fget, fset = fset ) )
    
            

    def _setProperty( self, name, value ):
        setattr( self, '_' + name, value )
    
    def _getProperty( self, name ):
        return getattr( self, '_' + name )

class Channel(ABC):
    id=None
    result=None
    dost=None
    error=None

    @abstractmethod
    def __call__(self) -> Any: ...
    
    def __str__(self):
        return f' Channel: id:{self.id}'

class Node(Channel):
    def __init__(self,id:int,moduleId:str, type:str, sourceIndexList:List,handler:callable=None) -> None:
        self.id=id
        self.sourceId=moduleId
        self.type=type
        self.sourceIndexList=sourceIndexList
        self.source=None
        self.resultIn=None
        self.result=None # данные после обработки handler
        self.handler=handler
        self.handlerStoredVars=None
    
    def __str__(self):
        return f''' Node: id:{self.id}, source:{self.source.id if self.source  else None}, source Id:{id(self.source)}, handler:{self.handler}, {self.result=}, {self.resultIn=}'''

    def __call__(self):
        if self.source:
            if self.source.result:
                if self.source.format==consts.DI:
                    self.resultIN=[self.source.result[i] for i in self.sourceIndexList]
                elif self.source.format==consts.AI:
                    self.resultIN=self.source.result[0]                                 # только 1-й элемент....  уточнить!!!!!!!!!!!!!!!!!!!!!!
            else:
                print(f'No result in channel {self.id} source {self.source}')
            # print(f'result in channel {self.id} = {self.source.result}')
            if self.handler:
                self.result,self.handlerStoredVars=handler(self.resultIN,self.handlerStoredVars)    #TODO поменять на VARS(), возможно BINDVARS()
            else:
                self.result=self.resultIN
        else:
            print (f'no source init for node id:{self.id}')
    
class Programm(Channel):
    def __init__(self,id:int,handler:callable,args:BindVars=None,stored:Vars=None) -> None:
        self.id=id
        self.stored=stored
        self.args=args
        self.handler=handler
    
    def __call__(self):
        self.stored=self.handler(self.args,self.stored)
    
    def exec(self):
        return self.__call__()

    def __str__(self):
        return f'Programm id:{self.id}, handler:{self.handler}'




if __name__ == '__main__':
    pass