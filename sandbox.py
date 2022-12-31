from  mutualcls import EList, SubscriptChannelArg
import channels.channels
class A():
    def __init__(self,a) -> None:
        self.a=a
    def __repr__(self) -> str:
        return '.a='+str(self.a)



l=EList()
ll=[]
c1=channels.channels.Channel(1)
c2=channels.channels.Channel(2)
# c1=A(1)
# c2=A(2)
print(hash(c1))
print(hash(c2))
print(c2==c1)
a1=SubscriptChannelArg(c1, 'result')
a2=SubscriptChannelArg(c2, 'result')
l.append_subscription(a1)
l.append_subscription(a1)
l.append_subscription(a2)
ll.append(c1)
ll.append(c2)
print(l)
print(l.index(a2))
print(l.index(a1))
l.del_subscription(a2)
l.del_subscription(a1)
print(l)