import classes
import time

class C:
    a=1
    b=2

c=C()


# v=classes.Vars()
# v.add('a',5)
# print (v.a)
# v1=classes.Vars()
# v1.add('b',1)
# v1.add('c',2)
# v1.add('d',3)
# print (v1.b)
# print (v1.c)
# print (v1.d)
v=classes.Vars()
v.addVar('a',1)
v.addVar('b',1)
v.addVar('c',1)
v.addVar('b',1)

def func1(arg,v):
    pass
    return v

def func2(arg):
    a=1
    b=1
    c=1
    d=1


TIMES = 10000000
begin=time.time()
for _ in range(TIMES):
    v=func1(1,v)
print(time.time()-begin)
begin=time.time()
for _ in range(TIMES):
    func2(1)
print(time.time()-begin)
