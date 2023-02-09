from dataclasses import dataclass
from channelbase import ChannelsBase
from typing import List

@dataclass
class Data():
    '''
    class for HTTP server data exchanging
    '''
    users:List
    channelBase:ChannelsBase
    subscribe_channels:List

class WSClient():
    '''
    web socket client 
    '''
    def __init__(self, ws_client) -> None:
        self.client=ws_client
        self.subscribe=[]