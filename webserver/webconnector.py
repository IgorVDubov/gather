import os.path
from webserver.tornado.tornadoserv import TornadoHTTPServerInit

def setHTTPServer(params, data):
    return TornadoHTTPServerInit(params, data)
