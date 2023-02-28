import importlib
import globals

import dbqueries as dbc
settings=importlib.import_module('projects.'+globals.PROJECT['path']+'.settings')


def get_causes(id:int)->dict[int:str]:
    return settings.IDLE_CAUSES
    # return dbc.querry_causes(id)

def get_allowed_machines():
    if globals.DEMO_DB:
        return settings.ALLOWED_MACHINES
    else:
        pass # get data from db
def get_operators():
    if globals.DEMO_DB:
        return settings.OPERATORS