import importlib
from datetime import datetime

import globals

# from ..logics import current_idle_store, current_idle_reset, current_idle_add_cause
logics=importlib.import_module('projects.'+globals.PROJECT['path']+'.logics')
settings=importlib.import_module('projects.'+globals.PROJECT['path']+'.settings')

def idle(vars):
    '''
        idle serving programm (обработка простоев)
        vars:
            state - current state
            machine_id - id станка
            cause_id - id причины
            reset_idle_flag - принудительный сброс текущего простоя без записи
            set_cause_flag - флаг указания причины оператором
            restore_idle_flag - текущая причина записывается с временной меткой и создается такаяже длящаяся далее
    '''
    idle=logics.current_idle_get(vars.machine_id)
    # print(idle)
    if vars.set_cause_flag:
        print(f'set cause flag to {vars.machine_id} to {vars.cause_id}')
        vars.set_cause_flag=False
        logics.current_idle_add_cause(vars.machine_id, vars.cause_id, datetime.now())
    
    if vars.restore_idle_flag:
        vars.restore_idle_flag=False
        logics.current_idle_store(vars.machine_id)
        logics.current_idle_add_cause(vars.machine_id, idle.cause_id, datetime.now())
    
    if vars.reset_idle_flag:
        vars.reset_idle_flag=False
        logics.current_idle_reset(vars.machine_id)

    if vars.state in settings.IDLE_STATES:
        if idle:             # простой уже зафиксирован 
            if not idle.cause: #но еще нет причины
                if (datetime.now()-idle.begin_time).total_seconds() >=settings.CAUSE_CHECK_TIMEOUT:
                    ...      # нe указана причина за отведенное время
        else:                # появился новый простой
            logics.current_idle_set(vars.machine_id,vars.state, vars.machine_tech_idle)
    else:
        if idle:             # если был простой и переход в работу
            if idle.cause:      # если указана причина
                pass
            else:   #если причина не указана
                logics.current_idle_add_cause(vars.machine_id, settings.NOT_CHEKED_CAUSE, datetime.now())
            logics.current_idle_store(vars.machine_id)
            logics.current_idle_reset(vars.machine_id)
        else:                 # работа - выход  
            return
