from datetime import datetime
import sys
import subprocess

TASK1_TIME='19:28'

def daySheduller(vars):
    '''
    execute tasks at shedulled day time
    TASK1_TIME format str '24h:m:s' or '24h:m' (00 sec) 
    external cmd files at ./cmd  dir
    '''
    now=datetime.now()
    try:
        time1 = datetime.strptime(TASK1_TIME, '%H:%M:%S')
    except ValueError:
        time1 = datetime.strptime(TASK1_TIME, '%H:%M')
    print (f'now:{now.hour}:{now.minute}:{now.second} goal:{time1.hour}:{time1.minute}:{time1.second} eqw:{now==time1}')
    if time1==now:
        print('!!!!!!!!!!!!******************!!!!!!!!!!!!!!!!!!')
        subprocess.run("./cmd/echo.cmd", shell=True)

    vars.v1=0
    vars.v2=0
    vars.v3=0
