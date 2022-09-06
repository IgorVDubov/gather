from operator import attrgetter
import classes 
import channel_handlers



class Node:
    def __init__(self,id,result) -> None:
        self.id=id
        self.result = result
        self.resultOut = None
    def __str__(self) -> str:
        return f'Node {self.id=}, {self.result=}, {self.resultOut=}'




def handler1(vars, stored):
    print (f'in handler: {vars.ch1=}, {vars.result=}, {stored.a=}')
    vars.result=vars.ch1
    stored.a=5
    print (f'exit handler: {vars.ch1=}, {vars.result=}, {stored.a=}')
    return stored







