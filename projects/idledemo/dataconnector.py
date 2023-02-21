import importlib

import dbqueries as dbc
settings=importlib.import_module('projects.'+globals.PROJECT['path']+'.settings')


def get_causes(id:int)->dict[int:str]:
    return settings.IDLE_CAUSES
    # return dbc.querry_causes(id)