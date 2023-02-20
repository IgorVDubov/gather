container=[{'k1':v, 'k2':None} for v in range(10)]
print (container)
search_val=5
try:
    found = next(rec for rec in container if rec.get('k1')==search_val)
except StopIteration:
    found=None
print (found)
def searcher(search_val):
    for rec in container:
        if rec.get('k1')==search_val:
            return rec
    return None
print (searcher(search_val))