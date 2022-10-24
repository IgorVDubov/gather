from time import time, sleep
from random import randint, random
import asyncio
from classes import Node
import globals
import scada_config
from exchange_server import ModbusExchangeServer, MBServerAdrMapInit

STATES={    'N/A':{'result':(None,None),'length':(20,200)},
            'Off':{'result':(0,0),'length':(20,200)},
            'Stand':{'result':(1,5),'length':(30,150)},
            'Work':{'result':(20,30),'length':(20,300)}
        }

class Source():
    def __init__(self,id,addr,regCount,format,function) -> None:
        self.id=id
        self.addr =addr
        self.regCount =regCount
        self.format =format
        self.function =function
    def __str__(self) -> str:
        return self.id

class NodeEmulator(Node):
    state:int = None
    length:int = None
    counter:int = 0
    def __str__(self):
        return super().__str__() + f'state:{self.state} len:{self.length}'

def nodesInit(configSources, configNodes):
    sources=[Source(source['id'],
                    # ip=source['ip'],
                    source['address'],
                    source['regCount'],
                    source['format'],
                    # port=source['port'],
                    source['function']
                    ) for source in configSources]

    nodes=[NodeEmulator(id=node['id'],moduleId=node['moduleId'],type=node['type'],sourceIndexList=node['sourceIndexList']) for node in configNodes]
    for node in nodes:
        node.state=list(STATES.keys())[randint(1,3)]
        node.length=randint(STATES.get(node.state)['length'][0], STATES.get(node.state)['length'][1])
        try:
            node.source=next(filter(lambda source:source.id==node.sourceId, sources))
        except StopIteration:
            node.source=None
        print(node)
    return nodes

def MBServerInit(MBServerParams, MBServerAdrMap):
    return ModbusExchangeServer(MBServerAdrMap, MBServerParams['host'], MBServerParams['port'])

async def aSleep(pause):
    await asyncio.sleep(pause)

def mainLoop(nodes, MBServer): 
    print ('loop start')
    MBServer.start()
    try:
        while True:
            for node in nodes:
                node.result=randint(STATES.get(node.state)['result'][0], STATES.get(node.state)['result'][1])
                node.counter+=1
                if node.counter>= node.length:
                    node.counter=0
                    node.state=list(STATES.keys())[randint(1,3)]
                    node.length=randint(STATES.get(node.state)['length'][0], STATES.get(node.state)['length'][1])
                MBServer.setValue(node.id, node.result)
            asyncio.run(aSleep(0.5))
    except KeyboardInterrupt:
        MBServer.stop()
        print ('loop stop')
        return

def main():
    nodes = nodesInit(scada_config.ModuleList, scada_config.channelsConfig.get('nodes'))
    MBServer = MBServerInit(globals.MBServerParams_E,scada_config.MBServerAdrMap)
    mainLoop(nodes, MBServer)

if __name__=='__main__':
    main()