import classes
class A:
    pass

a=A()
a.a=1
a.id=155
b=A()
b.a=5
b.id=156

v=classes.BindVars()
v1=classes.BindVars()

v.add('v1',a,'a')
v1.add('v2',b,'a')

print(a.a)
print(v)
print(v.v1)
print(v1)
print(v1.v2)
print('-----')

v3=classes.Vars()
v4=classes.Vars()

v3.add('v1',1)
v4.add('v2',2)

print(v3.v1)
print(v4.v2)
print(v3)