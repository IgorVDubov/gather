# from collections import namedtuple
# consts = namedtuple('contst',['MODBUS'])
# consts.MODBUS='ModBus'
import consts

HTTPServer=True


machinesList=[  
            #{'id':4205,'moduleId':'e41e0a011adc','type':'DI','bits':[0,1]},
            #{'id':4206,'moduleId':'e41e0a011adc','type':'DI','bits':[3]},
            {'id':4207,'moduleId':'ModuleA','type':'DI','sourceIndexList':[0,1],'handler':'func_1'},
            # {'id':4208,'moduleId':'ModuleB','type':'AI','sourceIndexList':[0]},
            #{'id':4208,'moduleId':'Test2','type':'DI','result':[2]},
            #{'id':4209,'moduleId':'Test2','type':'AI','result':[0]}
            ]
'''
список привязки входов к объекту контроля
id->int: id объекта контроля
moduleId->str: модуль с входами датчиков от  объекта контроля
type->str: di биты состояния, ai- аналоговые данные - одно значение, нет группового чтения
sourceIndexList->list: позиции (индексы с 0) данных массива результата чтения модуля moduleId
handler->str: имя функции обработчика результата (в модуле handler_funcs)
'''            
#
MBServerAdrMap=[
    {'unit':0x1, 'map':{
            'di':[{'id':4207,'addr':0,'len':16}
                  #,{'id':4208,'addr':3,'len':5}
                ],
            'ir':[{'id':4208,'addr':0,'type':'float'}
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

MBServerParams={'host':'192.168.1.200','port':5021}
'''
параметры Модбас сервера для внешнего доступа
host, port->str: An optional (interface, port) to bind to.
'''

MySQLServerParams={
    'host': '192.168.1.200',
    'database': 'utrack_db',
    'user': 'utrack',                       #TODO зашифровать!!!!!
    'password' : 'Adm_db78'
}
'''
параметры MySQLServer
'''

