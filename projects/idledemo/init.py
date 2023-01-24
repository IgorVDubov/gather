import importlib

import globals
from channels.channelbase import ChannelsBase
from channels.channels import Channel

logics=importlib.import_module('projects.'+globals.PROJECT['path']+'.logics')
project_globals=importlib.import_module('projects.'+globals.PROJECT['path']+'.projectglobals')

def init(channel_base:ChannelsBase):
    logics.load_machines_idle()