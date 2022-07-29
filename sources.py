import consts
ModuleList=[ #{'id':'e41e0a011adc','type':'ModbusTcp','ip':'192.168.1.99','port':'502','unit':0x1, 'address':51, 'regNumber':2, 'function':4, 'period':0.5},
            #{'id':'000de065a65f','type':'ModbusTcp','ip':'192.168.1.98','port':'502','unit':0x1, 'address':0, 'regNumber':16, 'function':2, 'period':0.5}
            #{'id':'Test1','type':'ModbudRS','ip':'','port':'2','unit':0x1, 'address':0, 'regNumber':16, 'function':2, 'period':0.5},
            {'id':'ModuleA','type':'ModbusTcp','ip':'192.168.1.200','port':502,'unit':0x1, 'address':1, 'count':2, 'function':3, 'format':consts.DI, 'period':0.5,'preprocess':''},
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
format->str: di - массив бит, ai - массив чисел длинной count
period->float: период опроса в сек
preprocess->str: функция предобработки данных 

''' 
