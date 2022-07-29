names=['alfa','beta']
class O():
    def __init__(self,name) -> None:
        self.__name__=name
        self.x=1
objcts=[]       
for name in names:
    objcts.append(O(name))
print (objcts)


pass