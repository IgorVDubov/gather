from time import time

def programm_1(vars,stored):
    print (f'in handler: {vars.ch1=}, {vars.result=}, {stored.a=}')
    vars.result=vars.ch1
    stored.a=5
    print (f'exit handler: {vars.ch1=}, {vars.result=}, {stored.a=}')
    return stored