import importlib

import globals

handlers=importlib.import_module('projects.'+globals.PROJECT['path']+'.handlers')
import handlerslib
# r_level_tout=importlib.import_module('projects.'+globals.PROJECT['path']+'.handlers.r_level_tout')
from consts import AI, DI
from handlerslib.bitstoword import bits_to_word

grWork=30
grStand=1
dostTimeout=5
minLength=5

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
module_list=[ 
            # {'id':'machine1','type':'ModbusTcp','ip':'127.0.0.1','port':'2000','unit':0x1, 'address':0, 'regCount':16, 'function':2, 'format':DI, 'period':0.5},
            ]    
  

'''
словарь конфигурации каналов:
{'id':4209,'moduleId':'test3','type':'AI','sourceIndexList':[0], 
            'handler':channel_handlers.middle10,
            'args':{'name':val,...}}
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
        'argName1':'self.v1' в args создается аргумент с именем argName1 и привязкой к аргументу v1 этого канала 
}
'''   
channels_config={
    'channels':[
        {'id':1001, 'args':{
                        'grWork':30,
                        'grStand':1,
                        'dostTimeout':5,
                        'minLength':5,
                    }
        },
    ],
    'nodes':[  
        {'id':4001,'moduleId':None,'type':'AI','sourceIndexList':[], 'handler':handlers.prog1,'args':{'result_in':'4001.result',
                                                                                                        'result_link_ch':'5001.result',}},
        {'id':5001,'moduleId':None,'type':'AI','sourceIndexList':[], 'handler':handlers.r_level_timeout,'args':{
                        'channel':'4001',
                        'dbChannel':None,
                        'writeInit':'13001.args.writeInit',
                        'statusCh_b1':'11001.args.b1',
                        'statusCh_b2':'11001.args.b2',
                        'grWork':'1001.args.grWork',
                        'grStand':'1001.args.grStand',
                        'dostTimeout':'1001.args.dostTimeout',
                        'minLength':'1001.args.minLength',
                        'notDost':0,
                        'NAStatusBefore':False,
                        'currentState':0,
                        'currentStateTime':0,
                        'currentInterval':0,
                        'buffered':False,
                        'statusDB':0,
                        'lengthDB':0,
                        'timeDB':0,
                        'init':True,
                        'dbQuie':'12001',
                        }},
    ],
    'programms':[
        {'id':11001,  'handler':handlerslib.bits_to_word,
                'args':{'result':'1001.result',
                        'b1':0,'b2':0,'b3':0,'b4':0,'b5':0,'b6':0,'b7':0,'b8':0,'b9':0,'b10':0,
                        'b11':0,'b12':0,'b13':0,'b14':0,'b15':0,'b16':0
                        }},
        {'id':13001,  'handler':handlers.day_sheduller,
                'args':{'writeInit':False}},
        
    ],
    'dbquie':[
        {'id':12001},
        ]
}


#
# разметка адресов Модбас сервера для внешнего доступа
# unit->int: номер unit-а по умолчанию 1
# map ->dict: общее:
#                 id->int: id объекта контроля
#                 addr->int: адрес (смещение) первого регистра

#             di - discrete_inputs чтение функцией 2
#                 len->int: кол-во регистров
#             hr - holding_registers чтение функцией 3
#             ir - input_registers чтение функцией 4
#                 type->str:      float - 2xWord CD-AB(4Byte);
#                                 int - 1xWord (2Byte)
                                
                                
mb_server_addr_map=[
    {'unit':0x1, 'map':{
        # 'di':[{'id':4001, 'attr':'result', 'addr':0, 'len':16}
        #     ],
        'ir':[{'id':4001, 'attr':'result', 'addr':0, 'type':'int'}
        #       ,{'id':4210,'addr':1,'type':'float'}
        ]
        }
    }]


MBServerAdrMap=mb_server_addr_map
channelsConfig=channels_config
ModuleList=module_list
