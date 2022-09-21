from loguru import logger
import classes 
from myexceptions import ChannelException, ConfigException
from time import time

CHANNELS_EXEC_ORDER=[classes.Node,classes.Channel,classes.Programm, classes.DBQuie]

class ChannelsBase():
    channels=[]
    channelsExecTime=None
    
    def add(self,channel:classes.Channel):
        try:
            found=next(filter(lambda _channel: _channel.id == channel.id, self.channels))
        except StopIteration:
            found=None
        if not found:
            if len(self.channels):
                try:
                    for ch in self.channels:
                        if CHANNELS_EXEC_ORDER.index(type(ch))>CHANNELS_EXEC_ORDER.index(type(channel)):
                            # print (f'insert channel {channel.id} ' )
                            self.channels.insert(self.channels.index(ch),channel)
                            return
                except ValueError:
                    logger.warning(f'cant find order on CHANNELS_EXEC_ORDER for channel {channel.id}, move to end')
            self.channels.append(channel)
            # print (f'append channel {channel.id} ' )
        else:
            raise Exception(f'duplicate id in channel base adding {channel} ')
    
    def get(self, id:int)->classes.Channel:
        try:
            found=next(filter(lambda _channel: _channel.id == id, self.channels))
        except StopIteration:
            found=None
        return found

    def execute(self, id:int):
        channel=self.get(id)
        try:
            result=channel()
        except ChannelException as e:
            logger.error(e)
        return result
    # def executeAll(self):
    #     for channelType in CHANNELS_EXEC_ORDER:
    #         for channel in [ch for ch in self.channels if isinstance(ch, channelType)]:
    #             print(f'exec {channel.id}')
    #             channel()
    def executeAll(self):
        startTime=time()
        for channel in self.channels:
            print(f'exec {channel.id}')
            channel()
        self.channelsExecTime=time()-startTime

    def nodesToDict(self):
        result=dict()
        result.setdefault(classes.Node.__name__.lower(),[])
        for channel in self.channels:
            if isinstance(channel, classes.Node):
                result[classes.Node.__name__.lower()].append(channel.toDict())
        return result
    
    def nodesToDictFull(self):
        result=dict()
        result.setdefault(classes.Node.__name__.lower(),[])
        for channel in self.channels:
            if isinstance(channel, classes.Node):
                result[classes.Node.__name__.lower()].append(channel.toDictFull())
        return result
    
    def toDict(self):
        result=dict()
        for chType in CHANNELS_EXEC_ORDER:          #!!! если нет нового класса канала в массиве - не будет включен!!!!!!!!
            result.setdefault(chType.__name__.lower(),[])
        for channel in self.channels:
            result[channel.__class__.__name__.lower()].append(channel.toDict())
        return result
    
    def toDictFull(self):
        result=dict()
        for chType in CHANNELS_EXEC_ORDER:          #!!! если нет нового класса канала в массиве - не будет включен!!!!!!!!
            result.setdefault(chType.__name__.lower(),[])
        for channel in self.channels:
            result[channel.__class__.__name__.lower()].append(channel.toDictFull())
        return result

    def __str__(self) -> str:
        return ''.join(channel.__str__()+'\n' for channel in self.channels )






def ChannelBaseInit(channelsConfig, dbQuie):
    # сначала у всех каналов создаем аттрибуты, потом привязываем связанные
    bindings=[]
    dbQuieChannel=False
    chBase=ChannelsBase()
    for channelType in channelsConfig:
        chType=eval(classes.CHANNELS_CLASSES.get(channelType))
        if chType==classes.Channel:
            cls=classes.Channel
        elif chType==classes.Node:
            cls=classes.Node
        elif chType==classes.Programm:
            cls=classes.Programm
        elif chType==classes.DBQuie:
            cls=classes.DBQuie
            dbQuieChannel=True
        else:
            raise ConfigException(f'no type in classes for {chType} {channelType}')
        for channelConfig in channelsConfig.get(channelType):
            if dbQuieChannel:
                channelConfig.update({'dbQuie':dbQuie})
            if channelConfig.get('args'):
                args=channelConfig.pop('args')
                channel=cls(**channelConfig)
                for name, arg in args.items():
                    bindId, param= classes.parseAttrParams(arg)
                    if bindId != None:
                        channel.addArg(name)
                        bindings.append((channel, name, bindId, param))
                    else:
                        channel.addArg(name, param)
            else:
                channel=cls(**channelConfig)
            chBase.add(channel)
        dbQuieChannel=False
    for (channel2Bind, name, bindId, param) in bindings:
        if bindId=='self':
            channel2Bind.bindArg(name, channel2Bind, param)
        elif bindId and param:
            channel2Bind.bindArg(name, chBase.get(bindId), param)
        elif bindId and param==None:
            channel2Bind.bindChannel2Arg(name, chBase.get(bindId))
    bindings=[]
    return chBase


def bindChannelAttr(channelBase, id:int,attrNmae:str)->classes.Vars:
    '''
    id- channel id
    attrname:str - channel attribute mane 
    '''
    if channel:=channelBase.get(id):
        bindVar=classes.Vars()
        bindVar.addBindVar('value',channel,attrNmae)
        return bindVar
    else:
        raise ConfigException(f'Cant find channel {id} in channelBase')

if __name__ == '__main__':
    nodes=[  
            #{'id':4207,'moduleId':'ModuleA','type':'DI','sourceIndexList':[0,1],'handler':'func_1'},
            # {'id':4208,'moduleId':'ModuleB','type':'AI','sourceIndexList':[0]},
            {'id':4208,'moduleId':'test2','type':'DI','sourceIndexList':[0,1]},
            {'id':4209,'moduleId':'test3','type':'AI','sourceIndexList':[0]}
            ]
    import channel_handlers
    prgs=[{'id':10001, 'handler':channel_handlers.programm_1, 'args':{'ch1':{'id':4208,'arg':'result'},'result':{'id':4209,'arg':'resultIn'}}, 'stored':{'a':0}}]
    cb=ChannelBaseInit(nodes, prgs) 
    print(cb)
    cb.get(4208).result=44
    cb.execute(10001)
    print(cb)
    cb.get(4208).result=50
    cb.execute(10001)
    print(cb)
    cb.executeAll()
    print(cb.channelsExecTime)