import importlib
from dataclasses import dataclass
from datetime import datetime

import channels.channelbase
import globals

settings=importlib.import_module('projects.'+globals.PROJECT['path']+'.settings')


def get_machine_from_user(user:str)->int:
    # try:
        return int(user[2:])
    # except ValueError:
    #     raise ValueError

def get_machine_causes(id:int)->dict[int:str]:               # TODO refact with DB
    return globals.idle_causes

def get_current_state(channel_base, id:int)->dict['machine':id, 'state':int, 'begin_time':str, 'couse_id':int]:
    channel=channel_base.get(id)

    state=channel.get_arg(settings.STATE_ARG)
    begin_time=channel.get_arg(settings.STATE_TIME_ARG).strftime('%Y-%m-%dT%H:%M:%S')
    cause_id=0
    cause_time=begin_time
    return {'machine':id, 'state':state, 'begin_time':begin_time, 'cause_id':cause_id, 'cause_time':cause_time}

@dataclass
class Idle():
    state:int
    begin_time:datetime
    cause:int=None
    cause_time:datetime=None
    length:int=0

def current_idle_get(machine_id):
    return globals.machines_idle.get(machine_id)

def current_idle_set(machine_id,state):
    print(f'set idle to {machine_id} with state {state}')
    begin_time=datetime.now()
    globals.machines_idle.update({machine_id:Idle(state,begin_time)})

def current_idle_add_cause(machine_id, cause_id, cause_time):
    if globals.machines_idle.get(machine_id):
        print(f'add cause idle to {machine_id} cause:{cause_id}')
        globals.machines_idle.get(machine_id).cause=cause_id
        globals.machines_idle.get(machine_id).cause_time=cause_time
    else:
        raise KeyError(f'no machine {machine_id} in globals.machines_idle')

def current_idle_reset(machine_id):
    print(f'reset idle {machine_id} ')
    globals.machines_idle.update({machine_id:None})

def current_idle_store(machine_id):
    if  idle:=globals.machines_idle.get(machine_id):
        globals.machines_idle.get(machine_id).length=(datetime.now()-idle.begin_time).total_seconds()
        print(f'Store machime {machine_id} Idle to DB: {idle.state}, cause: {globals.idle_causes.get(idle.cause,"Не подтверждена")}, length {idle.length}')
        print(idle)
        ... # store to DB here

