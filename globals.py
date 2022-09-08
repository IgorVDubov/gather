
# HTTPServerParams={'host':'192.168.1.200','port':8888}
# from tornado_serv import TornadoHTTPServerInit
# HTTPServer=TornadoHTTPServerInit(HTTPServerParams['port'])
HTTPServer=None


MBServerParams={'host':'localhost','port':5021}
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

