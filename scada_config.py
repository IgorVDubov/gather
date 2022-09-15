from channel_handlers import *
from consts import AI, DI

ModuleList=[ #{'id':'e41e0a011adc','type':'ModbusTcp','ip':'192.168.1.99','port':'502','unit':0x1, 'address':51, 'regNumber':2, 'function':4, 'period':0.5},
            #{'id':'000de065a65f','type':'ModbusTcp','ip':'192.168.1.98','port':'502','unit':0x1, 'address':0, 'regCount':16, 'function':2,'format':DI, 'period':0.5},
            {'id':'test2','type':'ModbusTcp','ip':'test2','port':'2','unit':0x1, 'address':0, 'regCount':16, 'function':2, 'format':DI, 'period':0.5},
            {'id':'test3','type':'ModbusTcp','ip':'test5','port':'2','unit':0x1, 'address':0, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            #{'id':'ModuleA','type':'ModbusTcp','ip':'192.168.1.200','port':502,'unit':0x1, 'address':1, 'count':2, 'function':3, 'format':consts.DI, 'period':0.5,'handler':''},
            # {'id':'ModuleB','type':'ModbusTcp','ip':'192.168.1.200','port':520,'unit':0x1, 'address':0, 'count':2, 'function':4, 'format':consts.AI,'period':0.5}
            ]    
'''
Список опрашиваемых модулей
id->str: для идентификации
type->str: тип устройства, реализовано: ModbusTcp
ip->str: ip или testN, тест - эммулятор сигнала с алгоритмом работы задающимся N
port->int: порт модуля
unit->int: номер устройства (в ТСР обычно 1, если ТСР конвертер в 485 - номер в 485-й сети)
address->int: с какого адреса начинаес читать данные
count->int: кол-во адресов для чтения
function->int: модбас функция: реализованы: 2-read_discrete_inputs, 3-read_holding_registers, 4-read_input_registers  
format->str: AI - массив бит, DI - массив чисел длинной count
period->float: период опроса в сек
handler->callable: функция предобработки данных из channel_handlers 

''' 
Channels=[
    {'id':100,}
]
nodes=[  
            #{'id':4207,'moduleId':'ModuleA','type':'DI','sourceIndexList':[0,1],'handler':'func_1'},
            # {'id':4208,'moduleId':'ModuleB','type':'AI','sourceIndexList':[0]},
            {'id':4208,'moduleId':'test2','type':'DI','sourceIndexList':[0,1]},
            {'id':4209,'moduleId':'test3','type':'AI','sourceIndexList':[0], 
                        'handler':middle,
                        'args':{'resultIn':'4209.resultIn',
                                'resultOut':'4209.result',
                                'deque':None,
                                'MAX_VALUES':10
                                }}
            ]
'''
список привязки входов к объекту контроля
{'id':4209,'moduleId':'test3','type':'AI','sourceIndexList':[0], 
            'handler':channel_handlers.middle10,
            'args':{('name':val),...}}
id->int: id объекта контроля
moduleId->str: модуль с входами датчиков от  объекта контроля
type->str: di биты состояния, ai- аналоговые данные - одно значение, нет группового чтения
sourceIndexList->list: позиции (индексы с 0) данных массива результата чтения модуля moduleId
handler->str: имя функции обработчика результата (в модуле handler_funcs)
args: запись аргументов: 
    'args':{
        'argName1':value[число] в args создается аргумент с именем argName1 и значением value 
        'argName1':'id' в args создается аргумент с именем argName1 и привязкой к объекту канала id 
        'argName1':'id.arg' в args создается аргумент с именем argName1 и привязкой к аргументу arg объекта канала id 
        'argName1':'id.arg.v1' в args создается аргумент с именем argName1 и привязкой к аргументу arg.v1 объекта канала id 
}
'''        
programms=[
    {'id':10001, 'handler':progSheduller, 'args':{'writeInit':False}},
    {'id':10002, 'handler':progVEK, 
                'args':{
                    'chIn':'4209.result',
                    'chIn':(4209,'result'),
                    'dost':(4209,'dost'),
                    'writeInit':(10001,'args.writeInit'),
                    'statusCh':(100,'result'),
                    'statusBit2':(10001,'args.writeInit'),

                    'grStand':1,
                    'grWork':8,
                    'dostTimeout':5,
                    'minLength':20,
                    }
    },
]

#
MBServerAdrMap=[
    {'unit':0x1, 'map':{
            'di':[{'id':4208, 'attr':'result', 'addr':0, 'len':16}
                  #,{'id':4208,'addr':3,'len':5}
                ],
            'ir':[{'id':4209, 'attr':'result', 'addr':0, 'type':'float'}
                  #,{'id':4210,'addr':1,'type':'float'}
                ]
            }
    }]
'''
разметка адресов Модбас сервера для внешнего доступа
unit->int: номер unit-а по умолчанию 1
map ->dict: общее:
                id->int: id объекта контроля
                addr->int: адрес (смещение) первого регистра

            di - discrete_inputs чтение функцией 2
                len->int: кол-во регистров
            hr - holding_registers чтение функцией 3
            ir - input_registers чтение функцией 4
                type->str:      float - 2xWord CD-AB(4Byte);
                                int - 1xWord (2Byte)
                                
                                
'''
