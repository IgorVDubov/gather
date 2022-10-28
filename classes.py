from cgitb import handler
from typing import *
from abc import ABC, abstractmethod
import inspect
import consts
from myexceptions import ConfigException, ProgrammException


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

def getDeepAttrValue(obj:type, attr:str):
    '''
    return  instance subobjects attributes value
    obj - class instance
    attr - attributes: example getDeepAttrValue(a, 'vars.b') if vars is instance with attr 'b' returns a.vars.b value
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

def parseAttrParams(attrParam):
    '''
    parse attribute Params
    return obj, attribute
    get Number return None, Value
    get str'channelID' return channelID:int , None
    get str'channelID.atrName' return channelID:int , 'atrName':str
    get str'channelID.atrName.var' return channelID:int , 'atrName.var':str
    '''
    if isinstance(attrParam, str):                                     #аттрибут - связь 
        s=''
        for i in range(0,len(attrParam)):
            if attrParam[i]=='.':
                break
        if i==len(attrParam)-1:
            first=attrParam
        else:
            first=attrParam[:i+(1 if len(attrParam)==1 else 0)]
        other=attrParam[i+1:]
        try:
            BindChannelId=int(first)
            if not other:
                attr=None
            else:
                attr=other
        except ValueError:
            BindChannelId='self'
            attr=attrParam
        # print(f'{attrParam=}: {BindChannelId=},{attr=}')
        if attr == None:      # channelBinding
            return BindChannelId, None
        else:                # channel attr Binding
            return BindChannelId, attr
    elif not(attrParam) or isinstance(attrParam, (int, float, bool)):   #аттрибут - число или None
        return None, attrParam

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
        for i, (name, obj, objAttrName, parent) in enumerate(self.vars):
            s+=f'    {name}'+(f'<-->{parent.id if hasattr(parent,"id") else parent}.{objAttrName}' if obj else '')+f'={getattr(self,name)}'
            if i < len(self.vars)-1 :
                s+='\n'
        return s
    
    # def __repr__(self):
    #     return self.__str__()

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
        if obj !=None:
            parent=obj
            obj, objAttrName=self._getSubObjectAttr(obj, objAttrName)
        if not ((inspect.isclass(type(obj)) and not type(obj) == type )
                and isinstance( objAttrName, str) 
                and isinstance( name, str)):
            raise ConfigException(f'Wrong argument type adding binding, args: {name=}, {obj=}, {objAttrName=}')
        if not hasattr(obj, objAttrName):
            raise ConfigException(f'Instance {obj.channelType} id:{obj.id} has no attribute {objAttrName}')

        fget = lambda self: self._getProperty( name )
        fset = lambda self, value: self._setProperty( name, value )
        
        setattr( self, '_' + name, getattr(obj,objAttrName) )
        setattr( self.__class__, name, property( fget = fget, fset = fset ) )
        # setattr( self, name, property( fget = fget, fset = fset ) )
        try:
            if found:=next(filter(lambda var: var[0] == name, self.vars)):
                attrName, _obj, _objAttr, _parent = found
                self.vars.remove(found)
                self.vars.append((attrName, obj, objAttrName, parent))
                return 
        except StopIteration:
            pass
        self.vars.append((name, obj, objAttrName, parent))

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

    def bindObject2Attr(self, name:str, obj:type):
        '''
        adds arg binding to inctance
        name - argumrnt namr
        obj - binding instance
        '''
        
        setattr( self, '_' + name, obj )
        try:
            if found:=next(filter(lambda var: var[0] == name, self.vars)):
                attrName, _obj, _objAttr, _parent = found
                self.vars.remove(found)
                self.vars.append((attrName, obj, None, obj))
                return 
        except StopIteration:
            pass
        self.vars.append((name, obj, None, obj))

    def addVar(self, name, defaultValue=None):
        '''
        adds attribute to instance NO BINDING
        name:str  attribute name
        [defaultValue]:Any   default Value
        '''
        if not isinstance( name, str):
            raise ConfigException(f'Wrong argument type adding arg: {name=}')
        fget = lambda self: self._getAttrProperty( name )
        fset = lambda self, value: self._setAttrProperty( name, value )
        
        setattr( self, '_' + name, defaultValue)
        setattr( self.__class__, name, property( fget = fget, fset = fset ) )
        self.vars.append((name, None, None, None))
        
    def toDict(self):
        result=dict()
        for name, obj, attr, parent in self.vars:
            result.update({name:getattr(self,name)})
        return result
   
    def _getBinding(self, name):
        try:
            
            if found:=next(filter(lambda var: var[0] == name, self.vars)):
                attrName, obj, objAttr, parent = found
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

class Channel(object):
    channelType='channel'
    id=None
    result=None
    dost=None
    error=None
    handler:callable=None
    args:Vars=None
    type=None

    def __init__(self, id, args:Vars=None) -> None:
        self.id=id
        self.args=args
    @abstractmethod
    def __call__(self) -> Any: ...
    def toDict(self):...
    def toDictFull(self):
        return self.toDict()

    def __str__(self):
        return f' Channel: id:{self.id}' + f'\n  args:\n{self.args}' if self.args else ''
    
    def addArg(self, name, value=None):
        if not self.args:
            self.args=Vars()
        self.args.addVar(name, value)
    
    def bindArg(self, name:str, channel:type, argName:str):
        self.args.addBindVar(name, channel, argName)

    def bindChannel2Arg(self, name:str, channel:type):
        self.args.bindObject2Attr(name, channel)

    def addBindArg(self, name:str, channel:type, argName:str):
        if not self.args:
            self.args=Vars()
        obj=self if channel==None else channel
        if argName!=None:
            self.args.addBindVar(name, obj, argName)
        else:
            self.args.bindObject(name, obj)
    
    def toDictFull(self):
        return self.toDict()

    def toDict(self):
        if self.args:
            return { 
                    'channelType':self.channelType,
                    'id':self.id,
                    'args':self.args.toDict()}
        else:
            return { 'type':self.type, 'id':self.id}

class DBQuie(Channel):
    def __init__(self, id, dbQuie, args: Vars = None) -> None:
        self.dbQuie=dbQuie
        super().__init__(id, args)
    def __str__(self):
        return f'DBQuieChannel: id:{self.id}, quie length: {self.dbQuie.qsize()} '
   
    def put(self, data):
        self.dbQuie.put_nowait(data)

class DBConnector(Channel):
    def __init__(self, id, dbQuie, handler:callable, args: Vars = None) -> None:
        if handler==None:
            raise myexceptions.ConfigException(f'No handler at channel {id} params')
        self.handler=handler
        super().__init__(id, args)
        if args !=None:
            self.args.addVar(dbQuie)
    
    def execute(self):
        self.handler(self.args)

class Node(Channel):
    channelType='node'
    def __init__(self,id:int,moduleId:str, type:str, sourceIndexList:List, handler:callable=None, args:Vars=None) -> None:
        self.id=id
        self.sourceId=moduleId
        self.type=type
        self.sourceIndexList=sourceIndexList
        self.source=None
        self.resultIn=None
        self.result=None # данные после обработки handler
        self.handler=handler
        self.args=args

    def __str__(self):
        return f"Node: id:{self.id}, source:{self.source.id if self.source  else None}, source Id:{id(self.source)}, handler:{self.handler}, {self.result=},"  + (f'\n  args:\n{self.args}' if self.args else '')

    def toDictFull(self):
        result= { 
                'channelType':self.channelType,
                'id':self.id,
                'sourceId':self.sourceId,
                'type':self.type,
                'sourceIndexList':self.sourceIndexList,
                'source':self.source,
                'resultIn':self.resultIn,
                'result':self.result}
        if self.handler:
            result.update({'handler':self.handler.__name__})
        if self.args:
            result.update({'args':self.args.toDict()})
        return result
    
    def toDict(self):
        return {    'channelType':self.channelType,
                    'id':self.id,
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
                self.handler(self.args)    
            else:
                self.result=self.resultIN
        else:
            print (f'no source init for node id:{self.id}')
    
class Programm(Channel):
    channelType='programm'
    def __init__(self,id:int,handler:callable, args:Vars=None) -> None:
        self.id=id
        self.args=args
        self.handler=handler
    
    def __call__(self):
        try:
            self.handler(self.args)
        except Exception as e:
            raise ProgrammException(f'Exc in channel {self.id} handler:{self.handler.__name__} raise {e}')
    
    def toDictFull(self):
        return self.toDict()

    def toDict(self):
        result= { 'channelType':self.channelType,
                'id':self.id,
                'handler':self.handler.__name__}
        if self.args:
            result.update({'args':self.args.toDict()})
        return result
    
    def exec(self):
        return self.__call__()

    def __str__(self):
        return f'Programm id:{self.id}, handler:{self.handler}'+ f'\n  args:\n{self.args}' if self.args else ''

CHANNELS_CLASSES={  'channels':'classes.Channel',           # соответствие имени класса для корректной привязки в аргументах Vars 
                    'nodes':'classes.Node', 
                    'programms':'classes.Programm', 
                    'dbquie':'classes.DBQuie',  
                    'dbconnector':'classes.DBConnector'
                } 

def testVars():
    print('Test Vars class:')
    Cl=type('Cl',(),{'a':44})
    c=Cl()
    v=Vars()
    v.addVar('a',55)
    print('add attr a = 55')
    print(v)
    print('add binding to inst c <-> attr a , c.a= 44')
    v.addBindVar('a',c,'a')
    print (f'{v.a=}')
    print(v)
    print('change value of bind attr v.a to 500')
    v.a=500
    print(f'{c.a=}')
    assert(c.a==500)
    v.addVar('obj')
    # v.obj=c
    v.bindObject2Attr('obj',c)
    print(v)
    v.obj.a=65438
    print(f'{c.a=}')


def moduleTests():
    testVars()

if __name__ == '__main__':
    testVars()