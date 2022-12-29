from dataclasses import dataclass
from typing import Any, List

from channels.channelbase import ChannelsBase
from channels.channels import Channel, parse_attr_params

class EList(list):
    def __init__(self):
        self.members=dict()
        super().__init__()
    
    def get_by_attr(self,attr_name, attr_val):
        return next((i for i in self if getattr(i, attr_name) == attr_val), None)
    
    def exist(self, filters:dict):
        result=False
        result=0
        for item in self:
            for key, val in filters.items():
                if getattr(item, key)== val:
                    result+=1
            if result==len(filters.keys()):
                return item
            else:
                return None
            
    def append_subscription(self,member):
        refs=self.members.get(id(member),0)
        if not refs:
            self.append(member)
        self.members.update({id(member):(refs+1)})
        return member
    
    def del_subscription(self,member):
        if refs:=self.members.get(id(member),0):
            refs-=1
            self.members[id(member)]=refs
            if refs<=0:
                self.remove(member)
                self.members.__delitem__(id(member))
            return member
        else:
            return None
    
    def _get_by_id(self,id):
        return next((i for i in self if id(i) == id), None)
    
    def _get_refs(self, member):
        return next((refs for m_id,refs in self.members.items() if m_id == id(member)), None)
    
    def __repr__(self):
        s=''
        for _ in self:
            s+=f'{_}'+f'({self._get_refs(_)}) '
        return s

class WSClient():
    '''
    web socket client 
    '''
    def __init__(self, ws_client) -> None:
        self.client=ws_client
        self.subscriptions=[]

@dataclass
class SubscriptChannelArg:
    def __init__(self,channel, channel_arg:str) -> None:
        self.argument:str=channel_arg
        self.channel:Channel=channel
        self.prev_value=None

    @property
    def value(self):
        return self.channel.get_arg(self.argument)  
    def to_dict(self):
        return {str(self.channel.id)+'.'+self.argument:self.value}
    def __repr__(self) -> str:
        return f'{self.channel.id}.{self.argument}'


@dataclass
class Data():
    '''
    class for HTTP server data exchanging
    '''
    users:List
    channelBase:ChannelsBase
    subsriptions:List[SubscriptChannelArg]
    ws_clients:dict()
