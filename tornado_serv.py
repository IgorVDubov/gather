import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
#from tornado.options import define, options
#from tornado.template import Template

class MainHtmlHandler(tornado.web.RequestHandler):
    def get(self):
        print (f'GET / request!!!!!!!!!!!!!')
        print(f'headers:{self.request.headers}')
        #self.write( 'test ')
        # self.write('<html><body ><div>  test  </div></body></html>')
        self.write('<html><body ><form style="margin:100px auto" align = center action="/" method="post">'
                   'Логин: <input type="text" name="name">'
                   '<input type="Submit" value="Вход">'
                   '</form></body></html>')
        #self.flush()
    
    def post(self):
            pass
            print (f'POST request!!!!!!!!!!!!!')
            print (f'requestHeader:{self.request.headers}')
            print (f'requestBody:{self.request.body}')
    
class RequestHtmlHandler(tornado.web.RequestHandler):
    
    def post(self):
        pass
        self.set_header("Content-Type", "application/x-www-form-urlencoded")
        requestHeader=self.request.headers
        print (f'POST request!!!!!!!!!!!!!')
        print (f'requestHeader:{requestHeader}')
        requestBody=self.request.body
        print (f'requestBody:{requestBody}')
    
    
    def get(self):
        pass
        self.set_header("Content-Type", "application/x-www-form-urlencoded")
        requestHeader=self.request.headers
        print (f'GET request!!!!!!!!!!!!!')
        print (f'requestHeader:{requestHeader}')
        requestBody=self.request.body
        print (f'requestBody:{requestBody}')





settings = {'debug': True}
handlers=[
    (r"/AJAX", RequestHtmlHandler),
    (r"/", MainHtmlHandler)
    ]
application = tornado.web.Application(handlers,**settings)
# http_server = tornado.httpserver.HTTPServer(application,ssl_options={"certfile": ".\ssl\device.crt","keyfile":".\ssl\device.key"})
http_server = tornado.httpserver.HTTPServer(application)
# http_server = tornado.httpserver.HTTPServer(application,ssl_options={"certfile": "utrack_test_1.p12","keyfile":"root_cert.crt"})
http_server.listen(8880)
main_loop = tornado.ioloop.IOLoop.current()
main_loop.make_current()
a_loop=main_loop.asyncio_loop
import asyncio

loop=asyncio.get_event_loop()
print(a_loop==loop)

from source_pool import SourcePool
from globals import ModuleList

pool=SourcePool(ModuleList,a_loop)
pool.start()

try:
    print('server satrt')
    main_loop.start()
except: #KeyboardInterrupt:
    main_loop.stop ()
    
