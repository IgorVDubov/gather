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
a1=SubscriptChannelArg(c1, 'result')
a2=SubscriptChannelArg(c1, 'result')
print(hash(a1))
print(hash(a2))
print(a2==a1)
l.append_subscription(a1)
l.append_subscription(a1)
l.append_subscription(a2)
print(l)
print(l.index(a2))
print(l.index(a1))
print(a2 in l)
l.del_subscription(a2)
l.del_subscription(a1)
print(l)