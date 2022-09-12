import classes
class C:
    a=1
    b=2

c=C()


v=classes.Vars()
v.add('a',5)
print (v.a)
v1=classes.Vars()
v1.add('b',1)
print (v1.b)
# v=classes.BindVars()
# v.add('aa',c, 'a')
# print (v.aa)
# v1=classes.BindVars()
# v1.add('bb',c,'b')
# print (v1.bb)
