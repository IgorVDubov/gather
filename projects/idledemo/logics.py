import globals


def get_machine_from_user(user:str)->int:
    # try:
        return int(user[2:])
    # except ValueError:
    #     raise ValueError

def get_machine_causes(id:int)->dict[int:str]:               # TODO refact
    return globals.idle_causes

def get_current_state(id:int)->dict['machine':id, 'state':int, 'begin_time':str, 'couse_id':int]:
    state=2
    begin_time='2023-01-10 08:20:00'
    cause_id=1
    return {'machine':id, 'state':state, 'begin_time':begin_time, 'cause_id':cause_id}