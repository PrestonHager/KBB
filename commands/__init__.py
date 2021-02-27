from .time_command import *
from .bf_command import *
from .view_command import *
from .flirt_command import *
from .marry_command import *
from .talk_command import *

def command(cmd, self, message):
    cmd_string = cmd + "_command"
    if cmd_string in __all__:
        exec("global return_val; return_val = " + cmd_string + "(self, message)")
        return return_val
    else:
        raise ValueError(f"No command with the name {cmd} found.")

__all__ = ["time_command", "bf_command", "view_command", "flirt_command", "marry_command", "talk_command", "command"]
