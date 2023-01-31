import json
import os.path
import importlib

import tornado.web
import tornado.websocket
from loguru import logger

import globals
from globals import CHECK_AUTORIZATION, PROJECT
from mutualcls import WSClient, SubscriptChannelArg
from channels.channels import parse_attr_params

logics=importlib.import_module('projects.'+globals.PROJECT['path']+'.logics')
settings=importlib.import_module('projects.'+globals.PROJECT['path']+'.settings')

RequestHandlerClass=tornado.web.RequestHandler
StaticFileHandler=tornado.web.StaticFileHandler
RequestHandler=tornado.web.RequestHandler
WebSocketHandler=tornado.websocket.WebSocketHandler



class BaseHandler(RequestHandlerClass):
    user=None
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def getUser(self):
        '''
        return dict with user data if user belongs to project with projectId or None
        '''
        if not self.current_user:
            return None
        try:
            userId = int(tornado.escape.xhtml_escape(self.current_user))
            # user=[user for user in self.application.data.users if user['id']==userId][0]
            if  user:=next(filter(lambda user: user['id'] == userId, self.application.data.users)):  
                # logger.debug('user '+user['login']+' ok')
                return user
            else:
               return None
        except TypeError or ValueError:
            return None
    
    def check_user(check_authorization=True): 
        def decorator(handler_func):
            def wrapper(self, *args, **kwargs):
                user={}
                if not check_authorization or (user:=self.getUser()):
                    self.user=user
                    handler_func(self, *args, **kwargs)
                else:
                    self.redirect("/login")
            return wrapper
        return decorator    

class MainHtmlHandler(BaseHandler):
    @BaseHandler.check_user(CHECK_AUTORIZATION)
    def get(self):
        # print (f'in MainHtmlHandler, project {PROJECT["name"]}, user {self.user} ')
        try:
            machine_id=logics.get_machine_from_user(self.user.get('login'))
        except ValueError:
            logger.log('ERROR', f'wrong machine id in client login {self.user.get("login")} do get_ch from ip:{self.request.remote_ip}.')
            self.redirect("/login")
       
        self.render('index.html', 
                    user=self.user.get('login'),
                    machine=machine_id,
                    state_channel=str(machine_id)+'.'+settings.STATE_ARG,
                    tech_idle=logics.get_channel_arg(self.application.data.channelBase,machine_id,settings.TECH_IDLE_ARG),
                    causeid_arg= logics.get_causeid_arg(self.application.data.channelBase.get(machine_id)),
                    idle_couses=json.dumps(logics.get_machine_causes(machine_id), default=str),
                    current_state=logics.get_current_state(self.application.data.channelBase,machine_id),
                    wsserv=self.application.settings['wsParams'],
                    server_time=logics.get_server_time(),
                    version=settings.CLIENT_VERSION,
                    )
class AdminHtmlHandler(BaseHandler):
    @BaseHandler.check_user(CHECK_AUTORIZATION)
    def get(self):
        # print (f'in MainHtmlHandler, project {PROJECT["name"]}, user {self.user} ')
        # try:
        #     machine_id=logics.get_machine_from_user(self.user.get('login'))
        # except ValueError:
        #     logger.log('ERROR', f'wrong machine id in client login {self.user.get("login")} do get_ch from ip:{self.request.remote_ip}.')
        #     self.redirect("/login")
       
        self.render('idleadm.html', 
                    user=self.user.get('login'), 
                    project=2,
                    idle_couses=json.dumps(logics.get_causes(), default=str),
                    version=0.1,
                    )

        
    
class RequestHtmlHandler(BaseHandler):
    @BaseHandler.check_user(CHECK_AUTORIZATION)
    def post(self):
        self.set_header("Content-Type", "application/json")
        request=json.loads(self.request.body)
        print (request)
        if request.get('type')=='get_ch':
            logger.log('MESSAGE',f'client {self.user.get("login")} do get_ch from ip:{self.request.remote_ip}.')
            self.write(json.dumps(self.application.data.channelBase.get(request.get('id')).toDict(), default=str))

class AdmRequestHtmlHandler(BaseHandler):
    @BaseHandler.check_user(CHECK_AUTORIZATION)
    def post(self):
        self.set_header("Content-Type", "application/json")
        request=json.loads(self.request.body)
        print (request)
        if request.get('type')=='get_ch':
            logger.log('MESSAGE',f'client {self.user.get("login")} do get_ch from ip:{self.request.remote_ip}.')
            self.write(json.dumps(self.application.data.channelBase.get(request.get('id')).toDict(), default=str))

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
            logger.info(f'Web Socket open, IP:{self.request.remote_ip} ')
            if self not in [client.client for client in self.application.data.ws_clients]:
                self.application.data.ws_clients.append(WSClient(self))
                logger.info(f'add, websocket IP:{self.request.remote_ip} Online {len(self.application.data.ws_clients)} clients')
        
    def on_message(self, message):
        try:
            jsonData = json.loads(message)
            print(jsonData)
        except json.JSONDecodeError:
            logger.error ("json loads Error for message: {0}".format(message))
        else:
            if jsonData['type']=="allStateQuerry":
                logger.debug ("ws_message: allStateQuerry")
                msg = {'type':'mb_data','data': None}
                json_data = json.dumps(msg, default=str)
                self.write_message(json_data)
            elif jsonData['type']=="subscribe":
                for arg in jsonData['data']:
                    channel_id, argument=parse_attr_params(arg)
                    channel=self.application.data.channelBase.get(channel_id)
                    new_subscription=SubscriptChannelArg(channel, argument)
                    subscription=self.application.data.subsriptions.add_subscription(new_subscription)
                    self.application.data.ws_clients.get_by_attr('client',self).subscriptions.append(subscription)
            elif jsonData.get('type')=="set":
                if arg:=jsonData.get('arg'):
                    channel_id, argument=parse_attr_params(arg)
                    channel=self.application.data.channelBase.get(channel_id)
                    value=jsonData.get('val')
                    self.application.data.channelBase.get(channel_id).set_arg(argument, value)
                    self.application.data.channelBase.get(channel_id).set_arg('args.set_cause_flag', True)
                    logger.debug (f"set arg: {jsonData.get('arg')} to {value}")
            
            else:
                logger.debug('Unsupported ws message: '+message)        
 
    def on_close(self):
        if client:=self.application.data.ws_clients.get_by_attr('client',self):
            for subscr in client.subscriptions:
                self.application.data.subsriptions.del_subscription(subscr)
            self.application.data.ws_clients.remove(client)

class MEmulHtmlHandler(BaseHandler):
    @BaseHandler.check_user(CHECK_AUTORIZATION)
    def get(self):
        print (f'in MainHtmlHandler, project {PROJECT["name"]}, user {self.user} ')
        
        self.render('memul.html', 
                    user=self.user.get('login'),
                    data=json.dumps(self.application.data.channelBase.toDict(), default=str),
                    wsserv=(self.application.settings['wsParams'])+'_me')
class MEmul1HtmlHandler(BaseHandler):
    @BaseHandler.check_user(CHECK_AUTORIZATION)
    def get(self):
        print (f'in MainHtmlHandler, project {PROJECT["name"]}, user {self.user} ')
        
        self.render('memul1.html', 
                    user=self.user.get('login'),
                    data=json.dumps(self.application.data.channelBase.toDict(), default=str),
                    wsserv=self.application.settings['wsParams'])

class MEmulRequestHtmlHandler(BaseHandler):
    @BaseHandler.check_user(CHECK_AUTORIZATION)
    def post(self):
        self.set_header("Content-Type", "application/json")
        request=json.loads(self.request.body)
        print (request)
        if request.get('type')=='get_ch':
            logger.log('MESSAGE',f'client {self.user.get("login")} do get_ch from ip:{self.request.remote_ip}.')
            self.write(json.dumps(self.application.data.channelBase.get(request.get('id')).toDict(), default=str))
        elif request.get('type')=='get_ch_arg':
            logger.log('MESSAGE',f'client {self.user.get("login")} do get_ch_arg from ip:{self.request.remote_ip}.')
            print(f"result: {self.application.data.channelBase.get(request.get('id')).get_arg(request.get('arg'))}")
            self.write(json.dumps(self.application.data.channelBase.get(request.get('id')).get_arg(request.get('arg')), default=str))
        elif request.get('type')=='set_ch':
            logger.log('MESSAGE',f'client {self.user.get("login")} do set_ch from ip:{self.request.remote_ip}.')
            print(request)
            self.application.data.channelBase.get(request.get('id')).set_arg(request.get('arg'),request.get('value'))
            self.write(json.dumps(200, default=str))
    
    
    def get(self):
        self.set_header("Content-Type", "application/x-www-form-urlencoded")
        requestHeader=self.request.headers
        print (f'GET request!!!!!!!!!!!!!')
        print (f'requestHeader:{requestHeader}')
        requestBody=self.request.body
        print (f'requestBody:{requestBody}')



class MEWSHandler(tornado.websocket.WebSocketHandler):
    # def initialize(self, clbk):
    #     self.callback=clbk
    # def __init__(self, *args, **kwargs):
    #     self.id = None
    #     super(WSHandler, self).__init__(*args, **kwargs)
    
    # def check_origin(self, origin: str) -> bool:
        #print(f'origin:{origin}')
        # сюда можно проверку хостов с которых запросы
        #return self.current_user != None  #ws запросы только если кто-то залогинился перед этим
        # return True
        #return super().check_origin(origin)

    def open(self):
            logger.info(f'Web Socket open, IP:{self.request.remote_ip} ')
            # if self.request.headers['User-Agent'] != 'UTHMBot':  #не логгируем запросы от бота и не включаем его в список ws рассылки
            #     #if tornado.escape.xhtml_escape(self.get_secure_cookie("user")) in [_ for _ in allUsers(users)]:
            if self not in [client.client for client in self.application.data.ws_clients]:
                self.application.data.ws_clients.append(WSClient(self))
                logger.info(f'add, websocket IP:{self.request.remote_ip} Online {len(self.application.data.ws_clients)} clients')
            #         user=[user for user in globals.users if user['id']==int(tornado.escape.xhtml_escape(self.get_secure_cookie("user")))][0]
            #         logger.info(f'Web Socket open, IP:{self.request.remote_ip},  user:{user.get("login")}, Online {len(globals.wss)} clients')
            #     else:
            #         logger.log ('LOGIN',f'websocket user {tornado.escape.xhtml_escape(self.get_secure_cookie("user"))} not autirized , IP:{self.request.remote_ip}')
            #         self.close()
        
    def on_message(self, message):
        try:
            jsonData = json.loads(message)
            print(jsonData)
        except json.JSONDecodeError:
            logger.error ("json loads Error for message: {0}".format(message))
        else:
            if jsonData.get('type')=="allStateQuerry":
                logger.debug ("ws_message: allStateQuerry")
                msg = {'type':'mb_data','data': None}
                json_data = json.dumps(msg, default=str)
                self.write_message(json_data)
            elif jsonData.get('type')=="subscribe":
                for arg in jsonData['data']:
                    channel_id, argument=parse_attr_params(arg)
                    channel=self.application.data.channelBase.get(channel_id)
                    new_subscription=SubscriptChannelArg(channel, argument)
                    subscription=self.application.data.subsriptions.add_subscription(new_subscription)
                    self.application.data.ws_clients.get_by_attr('client',self).subscriptions.append(subscription)
                # print (f'in ws:{self.application.data.subsriptions}')
            elif jsonData.get('type')=="msg":
                logger.debug (f"ws_message: {jsonData.get('data')}")
            elif jsonData.get('cmd')=="ws_reload":
                logger.debug (f"get command: reload websocket clients")
                for client in self.application.data.ws_clients:
                    client.write_message(json.dumps({'cmd':'reload'}))

            else:
                logger.debug('Unsupported ws message: '+message)        
 
    def on_close(self):
        # if self.request.headers['User-Agent'] != 'UTHMBot':  #не логгируем запросы от бота
        #     user=[user for user in globals.users if user['id']==int(tornado.escape.xhtml_escape(self.get_secure_cookie("user")))][0]
        #     logger.info(f' User {user.get("login")} close WebSocket. Online {len(self.application.wsC_cients)-1} clients')
        if client:=self.application.data.ws_clients.get_by_attr('client',self):
            for subscr in client.subscriptions:
                self.application.data.subsriptions.del_subscription(subscr)
            self.application.data.ws_clients.remove(client)

            
        # if len(globals.wss)==0:
            # print('No online users, callback stops')
            # self.callback.stop()


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument("name", "")
        
        for user in self.application.data.users:
            if user['login']==username:
                logger.log('DEBUG',f"Try login {username}, user ok, ip:{self.request.remote_ip}")
                #self.set_secure_cookie("user", username, expires_days=180)
                self.set_secure_cookie("user", str(user.get('id') ), expires_days=400)
                self.redirect("/")
                return
        # no such user
        logger.log('DEBUG',f"Try login {username}, user wrong , ip:{self.request.remote_ip}")
        self.redirect("/login")

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")

print( 'in handlers '+globals.PATH_TO_PROJECT)
print( 'in handlers full '+os.path.join(globals.PATH_TO_PROJECT, 'web' ,'webdata', 'js'))
handlers=[
        (r"/", MainHtmlHandler),
        (r"/request",RequestHtmlHandler),
        (r"/adm",AdminHtmlHandler),
        (r"/arequest",AdmRequestHtmlHandler),
        (r'/ws', WSHandler),
        (r"/me", MEmulHtmlHandler),
        (r"/me1", MEmul1HtmlHandler),
        (r"/merequest",MEmulRequestHtmlHandler),
        (r"/login",LoginHandler),
        (r"/logout",LogoutHandler),
        (r'/ws_me', MEWSHandler),
        (r"/static/(.*)", StaticFileHandler, {"path": os.path.join(globals.PATH_TO_PROJECT, 'web' ,'webdata')}),
        (r'/js/(.*)', StaticFileHandler, {'path': os.path.join(globals.PATH_TO_PROJECT, 'web' ,'webdata', 'js')}),
        (r'/css/(.*)', StaticFileHandler, {'path': os.path.join(globals.PATH_TO_PROJECT, 'web' ,'webdata', 'css')}),
        (r'/images/(.*)', StaticFileHandler, {'path': os.path.join(globals.PATH_TO_PROJECT, 'web' ,'webdata', 'images')}),
        ]
