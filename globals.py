HTTPServerParams={'host':'localhost','port':8888,'wsserver':'ws://localhost:8888/ws'}
# HTTPServerParams={'host':'localhost','port':8888,'wsserver':'ws://192.168.1.200:8888/ws'}

users=[{'id': 1, 'first_name': 'Igor', 'middle_name': '', 'second_name': 'Dubov', 'login': 'div', 'pass': '123'}]

DB_PERIOD=30

MBServerParams={'host':'localhost','port':5021}
'''
параметры Модбас сервера для внешнего доступа
host, port->str: An optional (interface, port) to bind to.
'''
MBServerParams_E={'host':'localhost','port':5022}
'''
параметры эмулятора Модбас сервера 
host:str, port:itn  An optional (interface, port) to bind to.
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

