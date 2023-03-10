from projects.empty.handlers import handlers as handlers
from handlerslib.bitstoword import bits_to_word


from consts import AI, DI

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
            {'id':'machine1','type':'ModbusTcp','ip':'127.0.0.1','port':'2000','unit':0x1, 'address':0, 'regCount':16, 'function':2, 'format':DI, 'period':0.5},
            {'id':'machine2','type':'ModbusTcp','ip':'127.0.0.1','port':'2001','unit':0x1, 'address':0, 'regCount':16, 'function':2, 'format':DI, 'period':0.5},
            {'id':'machine3','type':'ModbusTcp','ip':'127.0.0.1','port':'2002','unit':0x1, 'address':0, 'regCount':16, 'function':2, 'format':DI, 'period':0.5},
            {'id':'machine4','type':'ModbusTcp','ip':'127.0.0.1','port':'2003','unit':0x1, 'address':0, 'regCount':16, 'function':2, 'format':DI, 'period':0.5},
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
        # {'id':1001},
    ],
    # 'nodes_exmpl':[  
    #             #{'id':4207,'moduleId':'ModuleA','type':'DI','sourceIndexList':[0,1],'handler':'func_1'},
    #             # {'id':4208,'moduleId':'ModuleB','type':'AI','sourceIndexList':[0]},
    #             {'id':4208,'moduleId':'test2','type':'DI','sourceIndexList':[0,1]},
    #             {'id':4209,'moduleId':'test3','type':'AI','sourceIndexList':[0], 
    #                         'handler':None,
    #                         'args':{'resultIn':'resultIn',
    #                                 'resultOut':'4209.result',
    #                                 'deque':None,
    #                                 'MAX_VALUES':10
    #                                 }}
    # ],
    'nodes':[  
                {'id':4001,'moduleId':'machine1','type':'DI','sourceIndexList':[0]},
                {'id':4002,'moduleId':'machine2','type':'DI','sourceIndexList':[0]},
                {'id':4003,'moduleId':'machine3','type':'DI','sourceIndexList':[0]},
                {'id':4004,'moduleId':'machine4','type':'DI','sourceIndexList':[0]},
    ],
    'programms':[

        # {'id':13001,  'handler':daySheduller,
        #         'args':{'writeInit':False, 'v1':'1005.result','v2':'1006.result','v3':'1004.result'}},
        
    ],
    'dbquie':[
        # {'id':12001},
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
            'di':[{'id':4208, 'attr':'result', 'addr':0, 'len':16}
                  #,{'id':4208,'addr':3,'len':5}
                ],
            'ir':[{'id':4209, 'attr':'result', 'addr':0, 'type':'float'}
                  #,{'id':4210,'addr':1,'type':'float'}
                ]
            }
    }]


MBServerAdrMap=mb_server_addr_map
channelsConfig=channels_config
ModuleList=module_list
