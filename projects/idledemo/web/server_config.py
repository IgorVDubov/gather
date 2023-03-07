import os.path


def get_config(params):
    project_path=params.get('path')
    print (f' in  server app {project_path}')
    settings = {
        'static_path':  os.path.join(project_path, 'web' ,'webdata'),
        'template_path': os.path.join(project_path, 'web' ,'webdata'),
        # 'template_path': os.path.join(params.get('path'), 'webserver','webdata','templates'),
        'debug': True,
        #'debug': False,
        'cookie_secret':"61ofdgETxcvGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",    #TODO при необходимости вынести в envvar
        'wsParams':params.get('wsserver','ws://localhost:8888/ws')
        }
    return settings