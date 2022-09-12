import collections

q = collections.deque([],3)

def pq(q):
    s=''
    for _ in q:
       s+=str(q)+' ' 
q.append(1)
print (q, [i for i in q])
q.append(2)
print (q)
q.append(3)
print (q)
q.append(4)
print (q,sum(q))
# pq(q1)
