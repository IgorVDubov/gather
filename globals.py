from consts import Consts
import os.path
PROJECT={'path':'demomachines','comment':''}
project_path= os.path.join(PROJECT.get('path','/'),  'templates'),

HTTPServerParams={'host':'127.0.0.1','port':8870,'wsserver':'ws://127.0.0.1:8870/ws'}
# HTTPServerParams={'host':'127.0.0.1','port':8888,'wsserver':'ws://127.0.0.1:8888/ws'}

users=[{'id': 1, 'first_name': 'Igor', 'middle_name': '', 'second_name': 'Dubov', 'login': 'div', 'pass': '123'}]

DB_PERIOD=3    #период опроса очереди сообщений для БД DBQuie


CHANNELBASE_CALC_PERIOD=1 #период пересчета каналов в секундах (float) 

MBServerParams={'host':'127.0.0.1','port':5021}
'''
параметры Модбас сервера для внешнего доступа
host, port->str: An optional (interface, port) to bind to.
'''
MBServerParams_E={'host':'127.0.0.1','port':5022}
'''
параметры эмулятора Модбас сервера 
host:str, port:itn  An optional (interface, port) to bind to.
'''
DB_TYPE=Consts.MYSQL        #тип используемой СУБД (доступные в dbclassfactory)
MySQLServerParams={
    'host': '127.0.0.1',
    'database': 'utrack_demo',
    'user': 'utrack',                       #TODO в переменные окружения!!!!!
    'password' : 'Adm_db78'
}
'''
параметры MySQLServer
'''
DB_PARAMS=MySQLServerParams     #параметры для инициализации текущей СУБД
