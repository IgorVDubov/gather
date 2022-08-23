from time import time

def func_1(resultIn,globalParams):
    now=time()
    #print(globalParams)
    #print(param1)
    param1=resultIn[1]
    if param1!=globalParams.prevVal1:
        globalParams.changeEvent=True
        if now-globalParams.timeStamp>=1:
            globalParams.length=round(now-globalParams.timeStamp)
            globalParams.timeStamp=time()
            globalParams.prevVal1=param1
            globalParams.event=True
            #func_3()
    #print(param1,globalParams,event)
    return globalParams

def func_2(param,globalParams):
    return globalParams

def func_3():
    print('Change TADAAAAAAAAAAAAmmmmmm')

def programm_1(result,stored1):
    print('running programm 1')
    stored1+=1
    print(f'VAR {result=}, {stored1=}')
    return{'stored1':stored1}