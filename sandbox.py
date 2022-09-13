import classes
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
v.addVar('aa')
# print (v.aa)

v1=classes.Vars()
v1.bindVar('bb',v,'aa')


v.bindVar('aa',c,'b')
print (v.aa)

print (v)

print (v1.bb)
print (v1)
v1.bb=455
print(c.b)

