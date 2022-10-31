from datetime import datetime
from time import time
import sys
import subprocess

TASK1_TIME='22:16'

def daySheduller(vars):
    '''
    execute tasks at shedulled day time
    TASK1_TIME format str '24h:m:s' or '24h:m' (00 sec) 
    external cmd files at ./cmd  dir
    '''
    # now=datetime.now()
    now=time.now()
    try:
        time1 = datetime.strptime(TASK1_TIME, '%H:%M:%S')
    except ValueError:
        time1 = datetime.strptime(TASK1_TIME, '%H:%M')
    print (f'now:{now.hour}:{now.minute}:{now.second} goal:{time1.hour}:{time1.minute}:{time1.second} eqw:{now==time1}')
    if time1.hour==now.hour and time1.minute==now.minute and time1.second==now.second:
        print('!!!!!!!!!!!!******************!!!!!!!!!!!!!!!!!!')
        subprocess.run("./cmd/echo.cmd", shell=True)

    vars.v1=0
    vars.v2=0
    vars.v3=0
