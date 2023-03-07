import importlib

import config
from channels.channelbase import ChannelsBase
from channels.channels import Channel

logics=importlib.import_module('projects.'+config.PROJECT['path']+'.logics')
project_globals=importlib.import_module('projects.'+config.PROJECT['path']+'.projectglobals')

def init(channel_base:ChannelsBase):
    logics.load_machines_idle()