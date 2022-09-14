from cgitb import handler
from time import time
from tkinter.messagebox import NO
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

class Data():
    '''
    class for HTTP server data exchanging
    '''
    def __init__(self,users,channelbase) -> None:
        self.users = users
        self.channelBase = channelbase

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

# class Var_:
#     def __init__(self,name:str, obj:type, objAttrName:str) -> None:
#     # def __init__(self,name:str, obj:type, objAttrName:str, readonly:bool=False) -> None:
#         self.name=name
#         if obj !=None:
#             self.obj,self.objAttrName=getSubObjectAttr(obj,objAttrName)
#         else:
#             self.obj=None
#             self.objAttrName=None
#         self.objAttrName=objAttrName
#         # self.readonly=readonly

class Vars:
    '''
    Binds dynamic added self instsnce attribute to another instance attribute
    can bins subobject attr in format 'instance_attr.a'
    '''

    def __init__(self):
        self.__class__=type(self.__class__.__name__,(self.__class__,), {})
        self.vars=[]

    def __str__(self):
        s=''
        for name, obj, objAttrName in self.vars:
            s+=f'{name}'+(f'<-->{obj.id if hasattr(obj,"id") else obj}.{objAttrName}' if obj else '')+f'={getattr(self,name)}\n'
        return s
    
    def __repr__(self):
        return self.__str__()

    # def add(self,name:str, obj:type, objAttrName:str):
    #     return self._add(name, obj, objAttrName)
    @staticmethod
    def _getSubObjectAttr(obj:type, attr:str):
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

    def _add(self, name:str, obj:type, objAttrName:str):
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
        # setattr( self, name, property( fget = fget, fset = fset ) )
        if obj !=None:
            obj,objAttrName=self._getSubObjectAttr(obj,objAttrName)
        try:
            if found:=next(filter(lambda var: var[0] == name, self.vars)):
                attrName, _obj, _objAttr = found
                self.vars.remove(found)
                self.vars.append((attrName, obj, objAttrName))
                return 
        except StopIteration:
            pass
        self.vars.append((name, obj, objAttrName))

    def bindVar(self, name:str, obj:type, objAttrName:str):
        '''
        adds self attribute (name) bindig to instance (obj) attribute  (objAttrName)
        '''
        self._add(name, obj, objAttrName)
    
    def addBindVar(self, name:str, obj:type, objAttrName:str):
        '''
        adds self attribute (name) bindig to instance (obj) attribute  (objAttrName)
        '''
        self._add(name, obj, objAttrName)

    def addVar(self, name, defaultValue=None):
        '''
        adds attribute to instance NO BINDING
        name:str  attribute name
        [defaultValue]:Any   default Value
        '''
        if not isinstance( name, str):
            raise Exception(f'Wrong argument type adding arg: {name=}')
        fget = lambda self: self._getAttrProperty( name )
        fset = lambda self, value: self._setAttrProperty( name, value )
        
        setattr( self, '_' + name, defaultValue)
        setattr( self.__class__, name, property( fget = fget, fset = fset ) )
        self.vars.append((name, None, None))
        
    def toDict(self):
        result=dict()
        for name, obj, attr in self.vars:
            result.update({name:getattr(self,name)})
        return result
   
    def _getBinding(self, name):
        try:
            
            if found:=next(filter(lambda var: var[0] == name, self.vars)):
                attrName, obj, objAttr = found
                # return found.obj, found.objAttrName, found.readonly
                return obj, objAttr
        except StopIteration:
            found=None
        return None, None
        # return None, None, None

    def _setAttrProperty( self, name, value ):
        setattr( self, '_' + name, value )
    
    def _getAttrProperty( self, name ):
        return getattr( self, '_' + name )

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

# class Vars(object):
#     '''
#     dynamic added attribute with setters and getters
#     '''
#     def __init__(self):
#         self.__class__=type(self.__class__.__name__,(self.__class__,), {})
#         self.vars=[]

#     def add(self, name:str, defaultValue=None):
#     # def add(self, name:str, obj:type, objAttrName:str, readonly=False):
#         '''
#         adds attribute to instance
#         name:str  attribute name
#         [defaultValue]:Any   default Value
#         '''
#         if not isinstance( name, str):
#             raise Exception(f'Wrong argument type adding arg: {name=}')

#         fget = lambda self: self._getProperty( name )
#         fset = lambda self, value: self._setProperty( name, value )
        
#         setattr( self, '_' + name, defaultValue )
#         # setattr( self.__class__, name, property( fget = fget, fset = fset ) )
#         setattr( self.__class__, name, property( fget = fget, fset = fset ) )
#         self.vars.append(name)
            
#     def toDict(self):
#         result=dict()
#         for attr in self.vars:
#             result.update({attr:getattr(self,attr)})
#         return result
    
#     def __str__(self):
#         result=''
#         for attr in self.vars:
#             result+=f'{attr}={getattr(self,"_"+attr)}, '
#             return result

#     def _setProperty( self, name, value ):
#         setattr( self, '_' + name, value )
    
#     def _getProperty( self, name ):
#         return getattr( self, '_' + name )

class Channel(ABC):
    id=None
    result=None
    dost=None
    error=None
    argsMap:dict={}
    handler:callable=None
    args:Vars

    @abstractmethod
    def __call__(self) -> Any: ...
    def toDict(self):...
    def toDictFull(self):
        return self.toDict()

    def __str__(self):
        return f' Channel: id:{self.id}'

class Node(Channel):
    def __init__(self,id:int,moduleId:str, type:str, sourceIndexList:List, handler:callable=None, args:Vars=None, stored:Vars=None) -> None:
        self.id=id
        self.sourceId=moduleId
        self.type=type
        self.sourceIndexList=sourceIndexList
        self.source=None
        self.resultIn=None
        self.result=None # данные после обработки handler
        self.handler=handler

        if args:
            self.argsMap=args
            vars=Vars()
            for name, binding   in args():
                vars.add(name, value)
            self.stored=storedVars
        else:
            self.stored=None
        if stored:
            self.storedMap=stored
            storedVars=Vars()
            for name, value   in stored.items():
                storedVars.add(name, value)
            self.stored=storedVars
        else:
            self.stored=None

    
    def __str__(self):
        return f''' Node: id:{self.id}, source:{self.source.id if self.source  else None}, source Id:{id(self.source)}, handler:{self.handler}, {self.result=}, {self.resultIn=}'''

    def toDictFull(self):
        result= { 'id':self.id,
                'sourceId':self.sourceId,
                'type':self.type,
                'sourceIndexList':self.sourceIndexList,
                'source':self.source,
                'resultIn':self.resultIn,
                'result':self.result}
        if self.handler:
            result.update({'handler':self.handler.__name__,'handlerStoredVars':self.stored.toDict()})
        return result
    
    def toDict(self):
        return { 'id':self.id,
                'result':self.result}

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
                self.result,self.stored=self.handler(self.resultIN,self.stored)    #TODO поменять на VARS(), возможно BINDVARS()
            else:
                self.result=self.resultIN
        else:
            print (f'no source init for node id:{self.id}')
    
class Programm(Channel):
    def __init__(self,id:int,handler:callable,args:Vars=None,stored:Vars=None) -> None:
        self.id=id
        self.stored=stored
        self.args=args
        self.handler=handler
    
    def __call__(self):
        self.stored=self.handler(self.args,self.stored)
    
    def toDict(self):
        return { 'id':self.id,
                'handler':self.handler.__name__,
                'args':self.args.toDict(),
                'stored':self.stored.toDict()}
    
    def exec(self):
        return self.__call__()

    def __str__(self):
        return f'Programm id:{self.id}, handler:{self.handler}'




if __name__ == '__main__':
    pass