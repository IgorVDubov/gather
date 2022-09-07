from asyncio.log import logger
import classes 
from myexceptions import ChannelException
from time import time

CHANNELS_EXEC_ORDER=[classes.Node,classes.Programm]

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
                            print (f'insert channel {channel.id} ' )
                            self.channels.insert(self.channels.index(ch),channel)
                            return
                except ValueError:
                    logger.warn(f'cant find order on CHANNELS_EXEC_ORDER for channel {channel.id}, move to end')
            self.channels.append(channel)
            print (f'append channel {channel.id} ' )
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

    def __str__(self) -> str:
        return ''.join(channel.__str__()+'\n' for channel in self.channels )

def ChannelBaseInit(nodes=None, programms=None):
    chBase=ChannelsBase()
    for node in nodes:
        chBase.add(classes.Node(**node))
    for prg in programms:
        args=classes.BindVars()
        stored=classes.Vars()
        for name, objParams   in prg['args'].items():

            channel=chBase.get(objParams['id'])
            # print(channel)
            args.add(name, channel, objParams['arg'])
        for name, value   in prg['stored'].items():
            stored.add(name, value)
        programm=classes.Programm(prg['id'], prg['handler'], args, stored)
        chBase.add(programm)
    

    return chBase

def bindChannelAttr(channelBase, id:int,attrNmae:str)->classes.BindVars:
    '''
    id- channel id
    attrname:str - channel attribute mane 
    '''
    if channel:=channelBase.get(id):
        bindVar=classes.BindVars()
        bindVar.add('value',channel,attrNmae)
        return bindVar
    else:
        raise Exception(f'Cant find channel {id} in channelBase')

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