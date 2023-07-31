import sys, os
sys.path.append(os.path.dirname(__file__))

from toolbox import get_conf
from toolbox import set_conf
from toolbox import set_multi_conf
from toolbox import get_plugin_handle
from toolbox import get_plugin_default_kwargs
from toolbox import get_chat_handle
from toolbox import get_chat_default_kwargs


def chat_to_markdown_str(chat):
    result = ""
    for i, cc in enumerate(chat):
        result += f'\n\n{cc[0]}\n\n{cc[1]}'
        if i != len(chat)-1:
            result += '\n\n---'
    return result

