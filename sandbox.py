from dataclasses import dataclass

@dataclass
class A():
    i:int
    s:str

@dataclass    
class B(A):
    c:int


a=B(s='xsd',i=1,c=44)
print(a)