from operator import attrgetter
import classes 
import channel_handlers



class Node:
    def __init__(self,id,result) -> None:
        self.id=id
        self.result = result
        self.resultOut = None
    def __str__(self) -> str:
        return f'Node {self.id=}, {self.result=}, {self.resultOut=}'




def handler1(vars, stored):
    print (f'in handler: {vars.ch1=}, {vars.result=}, {stored.a=}')
    vars.result=vars.ch1
    stored.a=5
    print (f'exit handler: {vars.ch1=}, {vars.result=}, {stored.a=}')
    return stored




def ChannelBaseInit():
    nodes=[Node(1,10),Node(2,20),Node(3,30)]
    chBase=classes.ChannelsBase()
    for node in nodes:
        chBase.add(node)
    print('chBase')
    print(chBase)

    prg={'id':10001, 'handler':handler1, 'args':{'ch1':(2,'result'),'result':(1,'resultOut')}, 'stored':{'a':0}}
    args=classes.BindVars()
    stored=classes.Vars()
    for name, (id, arg)   in prg['args'].items():
        channel=chBase.getId(id)
        # print(channel)
        args.add(name, channel, arg)
    for name, value   in prg['stored'].items():
        stored.add(name, value)
    programm=classes.Programm(prg['id'], prg['handler'], args, stored)
    programm()
    print(chBase)
    nodes[1].result=44
    programm
    print(chBase)


if __name__ == '__main__':
    ChannelBaseInit()


