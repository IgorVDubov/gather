from  mutualcls import EList

class A():
    def __init__(self,a) -> None:
        self.a=a
    def __repr__(self) -> str:
        return '.a='+str(self.a)


l=EList()
a1=A(1)
a2=A(2)
a=l.append_subscription(a1)
l.append_subscription(a1)
l.append_subscription(a2)
print(l)
print(l.get_by_attr('a',1))
a.a=5
print(l)
print(l.get_by_attr('a',1))
l.del_subscription(a1)
l.del_subscription(a1)
print(l)
l.del_subscription(a1)
print(l)