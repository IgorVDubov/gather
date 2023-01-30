import importlib
import json
import pickle
from dataclasses import dataclass, asdict
from datetime import datetime

from channels.channelbase import ChannelsBase
import globals
from channels.channels import Channel
import colors

project_globals=importlib.import_module('projects.'+globals.PROJECT['path']+'.projectglobals')
settings=importlib.import_module('projects.'+globals.PROJECT['path']+'.settings')

def convert_none_2_str(func):
    '''
    convert None in function result to 'None'
    work with result type: single var, dict, list
    '''
    def wrapper(*args,**kwargs):
        result=func(*args,**kwargs)
        if isinstance(result, dict):
            for key, val in result.items():
                if val==None:
                    result.update({key:str(val)})
        elif isinstance(result, list):
            for val in result:
                if val==None:
                    val=str(val)
        elif isinstance(result, type(None)):
            result=str(None)
        return result
    return wrapper

def get_server_time():
    return datetime.now().strftime(settings.TIME_FORMAT)

def load_machines_idle():
    with open('idles.txt', 'r') as file:
        if saved:=file.read():
            if data:=json.loads(saved):
                rec={data.get('id'):Idle(data.get('state'),
                    data.get('tech_idle'),
                    datetime.strptime(data.get('begin_time'), settings.TIME_FORMAT) if data.get('begin_time') else None, 
                    data.get('cause'),
                    datetime.strptime(data.get('cause_time'), settings.TIME_FORMAT) if data.get('cause_time') else None, 
                    datetime.strptime(data.get('cause_set_time'), settings.TIME_FORMAT) if data.get('cause_set_time') else None, 
                    data.get('length')
                        )}
                project_globals.machines_idle.update(rec)

def save_machines_idle():
    with open('idles.txt', 'w') as file:
        for machine_id, idle in project_globals.machines_idle.items():
            if idle:
                data=dict({'id':machine_id,
                            'state':idle.state,
                            'tech_idle':idle.tech_idle,
                            'begin_time':idle.begin_time.strftime(settings.TIME_FORMAT) if idle.begin_time else None,
                            'cause':idle.cause,
                            'cause_time':idle.cause_time.strftime(settings.TIME_FORMAT) if idle.cause_time else None,
                            'cause_set_time':idle.cause_set_time.strftime(settings.TIME_FORMAT) if idle.cause_set_time else None,
                            'length':idle.length})
                file.write(json.dumps(data))

def get_machine_from_user(user:str)->int:
    # try:
        return int(user[2:])
    # except ValueError:
    #     raise ValueError

def get_causeid_arg(machine_ch:Channel)->int:               
    return str(machine_ch.get_arg(settings.IDLE_HANDLERID_ARG)) + '.' + settings.CAUSEID_ARG

def get_machine_causes(id:int)->dict[int:str]:               # TODO refact with DB
    return settings.IDLE_CAUSES  #пока так, отделяем зарезервированные причины (id < 0 ) от доступных

@convert_none_2_str
def get_channel_arg(channel_base:ChannelsBase, machine_id:int, arg:str):
    result= channel_base.get(machine_id).get_arg(arg)
    return result

@convert_none_2_str
def get_current_state(channel_base, machine_id:int)->dict['machine':id, 'state':int, 'begin_time':str, 'couse_id':int]:
    channel=channel_base.get(machine_id)
    if idle:=project_globals.machines_idle.get(machine_id):
        saved_state=idle.state
        saved_state_time= idle.begin_time.strftime(settings.TIME_FORMAT) if idle.begin_time else None
        saved_current_cause= idle.cause
        saved_current_cause_time= idle.cause_time.strftime(settings.TIME_FORMAT) if idle.cause_time else None
        saved_current_cause_set_time= idle.cause_set_time.strftime(settings.TIME_FORMAT) if idle.cause_set_time else None
    else:
        saved_state=None
        saved_state_time=None
        saved_current_cause=None
        saved_current_cause_time=None
        saved_current_cause_set_time=None
    state=channel.get_arg(settings.STATE_ARG)
    # if state==saved_state:
    if state in settings.IDLE_STATES and idle:
        state=saved_state
        begin_time=saved_state_time
        cause_id=saved_current_cause
        cause_time=saved_current_cause_time
        cause_set_time=saved_current_cause_set_time
    else:
        begin_time=channel.get_arg(settings.STATE_TIME_ARG).strftime(settings.TIME_FORMAT)
        cause_id=str(None)
        cause_time=str(None)
        cause_set_time=str(None)

    return {'machine':machine_id, 'state':state, 'begin_time':begin_time, 'cause_id':cause_id, 'cause_time':cause_time, 'cause_set_time':cause_set_time}

@dataclass
class Idle():
    state:int                       # текущее состояние
    tech_idle:int                   # техпростой, сек
    begin_time:datetime             # начало текущего состояния
    cause:int=None                  # причина простоя
    cause_time:datetime=None        # начало действия причины (может быть не равно begin_time если сменв причины без смены состояния)
    cause_set_time:datetime=None    # время установки причины
    length:int=0                    # длительность нахождения в текущей причине простоя

def current_idle_get(machine_id):
    return project_globals.machines_idle.get(machine_id)

def current_idle_set(machine_id, state, tech_idle):
    print(f'set idle to {machine_id} with state {state}')
    begin_time=datetime.now() 
    project_globals.machines_idle.update({machine_id:Idle(state, tech_idle, begin_time, )})
    save_machines_idle()

def current_idle_add_cause(machine_id, cause_id, cause_set_time):
    
    if current_idle:=project_globals.machines_idle.get(machine_id):
        if current_idle.cause!=None: 
            print(f'change cause idle to {machine_id} from {current_idle.cause} to {cause_id}')
            if current_idle.cause!=0:   #если причина была сброшена через causeid=0 время причины оставляем от сосента сброса
                current_idle_store(machine_id)
                project_globals.machines_idle.get(machine_id).cause_time = datetime.now() 
            elif current_idle.cause==settings.TECH_IDLE_ID:
                if (datetime.now()-current_idle.cause_time).seconds > current_idle.tech_idle:
                    project_globals.machines_idle.get(machine_id).cause_time = current_idle.cause_time + datetime.timedelta(0,current_idle.tech_idle)
        else:
            project_globals.machines_idle.get(machine_id).cause_time=current_idle.begin_time

        print(f'add cause idle to {machine_id} cause:{cause_id}')
        project_globals.machines_idle.get(machine_id).cause=cause_id
        project_globals.machines_idle.get(machine_id).cause_set_time=cause_set_time
        save_machines_idle()
    else:
        print(project_globals.machines_idle)
        raise KeyError(f'no machine {machine_id} in project globals.machines_idle')

def current_idle_reset(machine_id):
    print(f'reset idle {machine_id} ')
    project_globals.machines_idle.update({machine_id:None})
    save_machines_idle()

def current_idle_store(machine_id):
    if  idle:=project_globals.machines_idle.get(machine_id):
        project_globals.machines_idle.get(machine_id).length=int(round((datetime.now()-idle.cause_time).total_seconds()))
        print(f'{colors.CGREENBG}Store machime {machine_id} Idle to DB: {settings.STATES[idle.state]}, cause: {settings.IDLE_CAUSES.get(idle.cause,0)}, length {idle.length} {colors.CEND}')
        print(idle)
        ... # store to DB here

