import requests

r=requests.post('http://192.168.1.3/AJAX'
                ,headers={'Security-Hint':'F1EF8DA4A3C036D9016722536BBD7598'} 
                ,data='GETVARS:AI,18,0,1,1,1'
)
# r=requests.Request('POST','http://192.168.1.200:8880/AJAX'
#                 ,headers={'Security-Hint':'A9BBCE7D65B724A0F4CCEF83CFB2C331'} 
#                 ,data={'GETVARS':'AI,18,0,1,1,1'}
     
#                     )
# prepared = r.prepare()
# r=requests.Request('POST','http://192.168.1.3/AJAX'
#                 ,headers={'Security-Hint':'A9BBCE7D65B724A0F4CCEF83CFB2C331'} 
#                 ,data={'GETVARS':'AI,18,0,1,1,1'}
     
#                     )
# prepared = r.prepare()


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """

    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

# pretty_print_POST(prepared)

# prepared.body='GETVARS:AI,18,0,1,1,1'
# s=requests.Session()
# pretty_print_POST(prepared)
# resp = s.send(prepared, timeout=2)

print(r)
print(r.content.decode('utf-8'))


# print(resp)

pass