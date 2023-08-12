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

def cli():
    import argparse
    # Create ArgumentParser object
    parser = argparse.ArgumentParser()
    # Add an argument named 'c' with a short option '-c'.
    # This argument takes one value.
    parser.add_argument('input', nargs='+', help='The input string')
    parser.add_argument('-c', '--cmd', action='store_true', help="Call the commandline helper plugin.")
    args = parser.parse_args()
    if args.cmd:
        # use the commandline helper shortcut
        print('cmd', args.input)
    else:
        # echo, do nothing
        print(args.input)

