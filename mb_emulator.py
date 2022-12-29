#!/usr/bin/env python3
'''
Modbus Server эмулятор устройств отдающих данные по протоколу модбас
реализовано:
    +
данные по адресному пространству: scada_config.MBServerAdrMap
алгоритм в STATES {'N/A':{'result':(A,B),'length':(C,D)}...
                 { состояние:{значение_датчика:int random в диапазоне A,B, длительность_отрезка:int random в диапазоне C,D}}
обновление данных UPDATE_PERIOD секунд
'''
import asyncio
import sys
from random import randint

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  #Если запускаем из под win    

import importlib

import globals
from classes.channels import Node

scada_config=importlib.import_module('projects.'+globals.PROJECT['path']+'.scadaconfig')
from exchangeserver import ModbusExchangeServer

STATES={    'N/A':{'result':(None,None),'length':(20,200)},
            'Off':{'result':(0,0),'length':(5,20)},
            'Stand':{'result':(10,20),'length':(5,50)},
            'Work':{'result':(70,90),'length':(20,100)}
        }
UPDATE_PERIOD:float= 1 #update period in seconds

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
        # print(node)
    return nodes

def MBServerInit(MBServerParams, MBServerAdrMap):
    print('Address mapping:')
    for unit in MBServerAdrMap:
        print (f'Unit:{unit.get("unit")}')
        for name, regs in unit.get('map').items():
            print(f'    {name}')
            for reg in regs:
                print(f'        id:{reg.get("id")}, address:{reg.get("addr")}, type:{reg.get("type")}')
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
                    newStateIndex=randint(1,3)
                    while abs(newStateIndex-list(STATES.keys()).index(node.state))>1:
                        newStateIndex=randint(1,3)
                    node.state=list(STATES.keys())[newStateIndex]
                    node.length=randint(STATES.get(node.state)['length'][0], STATES.get(node.state)['length'][1])
                MBServer.setValue(node.id, node.result)
            asyncio.run(aSleep(UPDATE_PERIOD))
    except KeyboardInterrupt:
        print ('server stoping...')
        MBServer.stop()
        print ('server stops')
        return

def main():
    print ('*'*40)
    print ('*'+' '*38+'*')
    print ('*'+' '*12+''+'Modbus EMULATOR'+' '*11+'*')
    print ('*'+' '*38+'*')
    print ('*'*40)
    print (f"ip:{globals.MBServerParams_E['host']}, port:{globals.MBServerParams_E['port']}")

    nodes = nodesInit(scada_config.ModuleList, scada_config.channelsConfig.get('nodes'))
    MBServer = MBServerInit(globals.MBServerParams_E,scada_config.MBServerAdrMap)
    mainLoop(nodes, MBServer)

if __name__=='__main__':
    main()