from abc import ABC, abstractmethod
from typing import List

from mutualcls import WSClient
from webserver.tornado.tornadoserv import TornadoHTTPServerInit


class WebServer(ABC):
    ws_clients:List[WSClient]=[]

class TornadoInterface(WebServer):
    @property
    def ws_clients(self):
        return self.request_callback.wsClients

def setHTTPServer(params, data):
    return TornadoHTTPServerInit(params, data)
