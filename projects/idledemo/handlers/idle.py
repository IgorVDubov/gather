import importlib
import globals

# from ..logics import current_idle_store, current_idle_reset, current_idle_add_cause
logics=importlib.import_module('projects.'+globals.PROJECT['path']+'.logics')

def idle(vars):
    logics.current_idle_store(1,1)