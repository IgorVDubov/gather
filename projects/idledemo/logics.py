import importlib
import json
import pickle
from dataclasses import dataclass, asdict
from datetime import datetime

import channels.channelbase
import globals
from channels.channels import Channel

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

def load_machines_idle():
    with open('idles.txt', 'r') as file:
        if saved:=file.read():
            if data:=json.loads(saved):
                rec={data.get('id'):Idle(data.get('state'),
                                        datetime.strptime(data.get('begin_time'), '%Y-%m-%dT%H:%M:%S') if data.get('begin_time') else None, 
                                        data.get('cause'),
                                        datetime.strptime(data.get('cause_time'), '%Y-%m-%dT%H:%M:%S') if data.get('cause_time') else None, 
                                        data.get('length')
                        )}
                project_globals.machines_idle.update(rec)


def save_machines_idle():

    with open('idles.txt', 'w') as file:
        for machine_id, idle in project_globals.machines_idle.items():
            if idle:
                data=dict({'id':machine_id,
                            'state':idle.state,
                            'begin_time':idle.begin_time.strftime('%Y-%m-%dT%H:%M:%S') if idle.begin_time else None,
                            'cause':idle.cause,
                            'cause_time':idle.cause_time.strftime('%Y-%m-%dT%H:%M:%S') if idle.cause_time else None,
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
    return settings.IDLE_CAUSES

@convert_none_2_str
def get_current_state(channel_base, machine_id:int)->dict['machine':id, 'state':int, 'begin_time':str, 'couse_id':int]:
    channel=channel_base.get(machine_id)
    if idle:=project_globals.machines_idle.get(machine_id):
        saved_state=idle.state
        saved_state_time= idle.begin_time.strftime('%Y-%m-%dT%H:%M:%S') if idle.begin_time else None
        saved_current_cause= idle.cause
        saved_current_cause_time= idle.cause_time.strftime('%Y-%m-%dT%H:%M:%S') if idle.cause_time else None
    else:
        saved_state=None
        saved_state_time=None
        saved_current_cause=None
        saved_current_cause_time=None
    state=channel.get_arg(settings.STATE_ARG)
    # if state==saved_state:
    if state in settings.IDLE_STATES and idle:
        state=saved_state
        begin_time=saved_state_time
        cause_id=saved_current_cause
        cause_time=saved_current_cause_time
    else:
        begin_time=channel.get_arg(settings.STATE_TIME_ARG).strftime('%Y-%m-%dT%H:%M:%S')
        cause_id=str(None)
        cause_time=str(None)

    return {'machine':machine_id, 'state':state, 'begin_time':begin_time, 'cause_id':cause_id, 'cause_time':cause_time}

@dataclass
class Idle():
    state:int
    begin_time:datetime
    cause:int=None
    cause_time:datetime=None
    length:int=0

def current_idle_get(machine_id):
    return project_globals.machines_idle.get(machine_id)

def current_idle_set(machine_id,state):
    print(f'set idle to {machine_id} with state {state}')
    begin_time=datetime.now()
    project_globals.machines_idle.update({machine_id:Idle(state,begin_time)})
    save_machines_idle()

def current_idle_add_cause(machine_id, cause_id, cause_time):
    if project_globals.machines_idle.get(machine_id):
        print(f'add cause idle to {machine_id} cause:{cause_id}')
        project_globals.machines_idle.get(machine_id).cause=cause_id
        project_globals.machines_idle.get(machine_id).cause_time=cause_time
        save_machines_idle()
    else:
        raise KeyError(f'no machine {machine_id} in project globals.machines_idle')

def current_idle_reset(machine_id):
    print(f'reset idle {machine_id} ')
    project_globals.machines_idle.update({machine_id:None})
    save_machines_idle()

def current_idle_store(machine_id):
    if  idle:=project_globals.machines_idle.get(machine_id):
        project_globals.machines_idle.get(machine_id).length=(datetime.now()-idle.begin_time).total_seconds()
        print(f'Store machime {machine_id} Idle to DB: {idle.state}, cause: {project_globals.idle_causes.get(idle.cause,"Не подтверждена")}, length {idle.length}')
        print(idle)
        ... # store to DB here

