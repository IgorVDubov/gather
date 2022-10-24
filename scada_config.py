from channel_handlers import *
from consts import AI, DI
from datetime import datetime

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
ModuleList_exmpl=[ #{'id':'e41e0a011adc','type':'ModbusTcp','ip':'192.168.1.99','port':'502','unit':0x1, 'address':51, 'regNumber':2, 'function':4, 'period':0.5},
            #{'id':'000de065a65f','type':'ModbusTcp','ip':'192.168.1.98','port':'502','unit':0x1, 'address':0, 'regCount':16, 'function':2,'format':DI, 'period':0.5},
            {'id':'test2','type':'ModbusTcp','ip':'test2','port':'2','unit':0x1, 'address':0, 'regCount':16, 'function':2, 'format':DI, 'period':0.5},
            {'id':'test3','type':'ModbusTcp','ip':'test5','port':'2','unit':0x1, 'address':0, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            #{'id':'ModuleA','type':'ModbusTcp','ip':'192.168.1.200','port':502,'unit':0x1, 'address':1, 'count':2, 'function':3, 'format':consts.DI, 'period':0.5,'handler':''},
            # {'id':'ModuleB','type':'ModbusTcp','ip':'192.168.1.200','port':520,'unit':0x1, 'address':0, 'count':2, 'function':4, 'format':consts.AI,'period':0.5}
            ]    
ModuleList=[ 
            {'id':'10001','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':0, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10002','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':2, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10003','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':4, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10004','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':6, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10005','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':8, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10006','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':10, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10007','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':12, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10008','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':14, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10009','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':16, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10010','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':18, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10011','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':20, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10012','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':22, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10013','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':24, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10014','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':26, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10015','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':28, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10016','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':30, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10017','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':32, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10018','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':34, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10019','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':36, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            {'id':'10020','type':'ModbusTcp','ip':'localhost','port':'5022','unit':0x1, 'address':38, 'regCount':2, 'function':4, 'format':AI, 'period':0.5},
            ]    

'''
словарь конфигурации каналов:
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
        'argName1':'self.v1' в args создается аргумент с именем argName1 и привязкой к аргументу v1 этого канала 
}
'''   
channelsConfig={
    'channels':[
        # {'id':100,'args':{
        #                 'chIn':'4209.result','chIn1':'4209.result'}
        # }
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
                #{'id':4207,'moduleId':'ModuleA','type':'DI','sourceIndexList':[0,1],'handler':'func_1'},
                # {'id':4208,'moduleId':'ModuleB','type':'AI','sourceIndexList':[0]},
                {'id':4001,'moduleId':'10001','type':'AI','sourceIndexList':[0]},
                {'id':4002,'moduleId':'10002','type':'AI','sourceIndexList':[0]},
                {'id':4003,'moduleId':'10003','type':'AI','sourceIndexList':[0]},
                {'id':4004,'moduleId':'10004','type':'AI','sourceIndexList':[0]},
                {'id':4005,'moduleId':'10005','type':'AI','sourceIndexList':[0]},
                {'id':4006,'moduleId':'10006','type':'AI','sourceIndexList':[0]},
                {'id':4007,'moduleId':'10007','type':'AI','sourceIndexList':[0]},
                {'id':4008,'moduleId':'10008','type':'AI','sourceIndexList':[0]},
                {'id':4009,'moduleId':'10009','type':'AI','sourceIndexList':[0]},
                {'id':4010,'moduleId':'10010','type':'AI','sourceIndexList':[0]},
                {'id':4011,'moduleId':'10011','type':'AI','sourceIndexList':[0]},
                {'id':4012,'moduleId':'10012','type':'AI','sourceIndexList':[0]},
                {'id':4013,'moduleId':'10013','type':'AI','sourceIndexList':[0]},
                {'id':4014,'moduleId':'10014','type':'AI','sourceIndexList':[0]},
                {'id':4015,'moduleId':'10015','type':'AI','sourceIndexList':[0]},
                {'id':4016,'moduleId':'10016','type':'AI','sourceIndexList':[0]},
                {'id':4017,'moduleId':'10017','type':'AI','sourceIndexList':[0]},
                {'id':4018,'moduleId':'10018','type':'AI','sourceIndexList':[0]},
                {'id':4019,'moduleId':'10019','type':'AI','sourceIndexList':[0]},
                {'id':4020,'moduleId':'10020','type':'AI','sourceIndexList':[0]},
     
    ],
    'programms':[
        # {'id':10001, 'handler':progSheduller, 'args':{'writeInit':False, 'writeInit1':False}},
        # {'id':10002, 'handler':progVEK, 
        #             'args':{
        #                 'channel':'4209',
        #                 'dbChannel':None,
        #                 'writeInit':'10001.args.writeInit',
        #                 'statusCh':'100.result',
        #                 'grStand':1,
        #                 'grWork':30,
        #                 'dostTimeout':5,
        #                 'minLength':5,
        #                 'notDost':0,
        #                 'NAStatusBefore':False,
        #                 'currentState':0,
        #                 'currentStateTime':0,
        #                 'currentInterval':0,
        #                 'buffered':False,
        #                 'statusDB':0,
        #                 'lengthDB':0,
        #                 'timeDB':0,
        #                 'buffered':False,
        #                 'init':True,
        #                 'dbQuie':'11001',

        #                 }
        # },
    ],
    'dbquie':[{'id':11001}]
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
                                
                                
MBServerAdrMap_exmpl=[
    {'unit':0x1, 'map':{
            'di':[{'id':4208, 'attr':'result', 'addr':0, 'len':16}
                  #,{'id':4208,'addr':3,'len':5}
                ],
            'ir':[{'id':4209, 'attr':'result', 'addr':0, 'type':'float'}
                  #,{'id':4210,'addr':1,'type':'float'}
                ]
            }
    }]
MBServerAdrMap=[
    {'unit':0x1, 'map':{
            # 'di':[{'id':4208, 'attr':'result', 'addr':0, 'len':16}
                  #,{'id':4208,'addr':3,'len':5}
                # ],
            'ir':[  {'id':4001, 'attr':'result', 'addr':0, 'type':'float'},
                    {'id':4002, 'attr':'result', 'addr':2, 'type':'float'},
                    {'id':4003, 'attr':'result', 'addr':4, 'type':'float'},
                    {'id':4004, 'attr':'result', 'addr':6, 'type':'float'},
                    {'id':4005, 'attr':'result', 'addr':8, 'type':'float'},
                    {'id':4006, 'attr':'result', 'addr':10, 'type':'float'},
                    {'id':4007, 'attr':'result', 'addr':12, 'type':'float'},
                    {'id':4008, 'attr':'result', 'addr':14, 'type':'float'},
                    {'id':4009, 'attr':'result', 'addr':16, 'type':'float'},
                    {'id':4010, 'attr':'result', 'addr':18, 'type':'float'},
                    {'id':4011, 'attr':'result', 'addr':20, 'type':'float'},
                    {'id':4012, 'attr':'result', 'addr':22, 'type':'float'},
                    {'id':4013, 'attr':'result', 'addr':24, 'type':'float'},
                    {'id':4014, 'attr':'result', 'addr':26, 'type':'float'},
                    {'id':4015, 'attr':'result', 'addr':28, 'type':'float'},
                    {'id':4016, 'attr':'result', 'addr':30, 'type':'float'},
                    {'id':4017, 'attr':'result', 'addr':32, 'type':'float'},
                    {'id':4018, 'attr':'result', 'addr':34, 'type':'float'},
                    {'id':4019, 'attr':'result', 'addr':36, 'type':'float'},
                    {'id':4020, 'attr':'result', 'addr':38, 'type':'float'},
                ]
            }
    }]

