import os.path
from webserver.tornado.tornado_serv import TornadoHTTPServerInit

def setHTTPServer(params, data):
    return TornadoHTTPServerInit(params, data)