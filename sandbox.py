import classes
import time

# class Channel:
#     id=1
#     result=2

# c=Channel()
# c.id=44


# v=classes.Vars()
# v.addVar('a',55)
# print(v)
# v.addBindVar('a',c,'result')
# print (v.a)
# print(v)
# v.a=500
# print(c.result)


v=classes.Vars()
v.addVar('a',1)
v.addVar('b',1)
v.addVar('c',1)
v.addVar('b',1)

def func1(arg,v):
    v.a=arg
    # return v

def func2(arg):
    a=1
    b=1
    c=1
    d=1

print(v)
func1(50,v)
print(v)
# TIMES = 10_000_000
# begin=time.time()
# for _ in range(TIMES):
#     v=func1(1,v)
# print(time.time()-begin)
# begin=time.time()
# for _ in range(TIMES):
#     func2(1)
# print(time.time()-begin)
