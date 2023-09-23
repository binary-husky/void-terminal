import sys, os
sys.path.append(os.path.dirname(__file__))

from toolbox import get_conf
from toolbox import set_conf
from toolbox import set_multi_conf
from toolbox import get_plugin_handle
from toolbox import get_plugin_default_kwargs
from toolbox import get_chat_handle
from toolbox import get_chat_default_kwargs
from functools import wraps

def chat_to_markdown_str(chat):
    result = ""
    for i, cc in enumerate(chat):
        result += f'\n\n{cc[0]}\n\n{cc[1]}'
        if i != len(chat)-1:
            result += '\n\n---'
    return result

def silence_stdout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        for q in func(*args, **kwargs):
            sys.stdout = _original_stdout
            yield q
            sys.stdout = open(os.devnull, 'w')
        sys.stdout.close()
        sys.stdout = _original_stdout
    return wrapper

def silence_stdout_fn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        result = func(*args, **kwargs)
        sys.stdout.close()
        sys.stdout = _original_stdout
        return result
    return wrapper

class VoidTerminal():
    def __init__(self) -> None:
        pass
    
vt = VoidTerminal()

vt.get_conf = silence_stdout_fn(get_conf)
vt.set_conf = silence_stdout_fn(set_conf)
vt.set_multi_conf = silence_stdout_fn(set_multi_conf)
vt.get_plugin_handle = silence_stdout_fn(get_plugin_handle)
vt.get_plugin_default_kwargs = silence_stdout_fn(get_plugin_default_kwargs)
vt.get_chat_handle = silence_stdout_fn(get_chat_handle)
vt.get_chat_default_kwargs = silence_stdout_fn(get_chat_default_kwargs)
vt.chat_to_markdown_str = chat_to_markdown_str

get_conf = vt.get_conf
set_conf = vt.set_conf
set_multi_conf = vt.set_multi_conf
get_plugin_handle = vt.get_plugin_handle
get_plugin_default_kwargs = vt.get_plugin_default_kwargs
get_chat_handle = vt.get_chat_handle
get_chat_default_kwargs = vt.get_chat_default_kwargs
chat_to_markdown_str = vt.chat_to_markdown_str


def chat_to_markdown_str(chat):
    result = ""
    for i, cc in enumerate(chat):
        result += f'\n\n{cc[0]}\n\n{cc[1]}'
        if i != len(chat)-1:
            result += '\n\n---'
    return result

def add_env_variable(variable:str, value:str):
    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, "r") as bashrc_file:
        env_lines = bashrc_file.readlines()
    found_conflict = False
    for i, line in enumerate(env_lines):
        if line.startswith(f"export {variable}="):
            old_value = line.split("=")[1].strip()
            print(f"Conflict detected with {variable}={old_value}. Resolve conflict.")
            env_lines[i] = f"export {variable}={value}  # Void-Terminal\n"
            found_conflict = True
        if not env_lines[i].endswith('\n'): env_lines[i] += '\n'
    # If the variable is not found, append it to .bashrc
    if not found_conflict:
        env_lines.append(f"export {variable}={value}  # Void-Terminal\n")
    with open(bashrc_path, "w") as bashrc_file:
        bashrc_file.writelines(env_lines)
    os.environ[variable] = value

def plugin_shortcut(main_input, plugin, advanced_arg=None):
    from rich.live import Live
    from rich.markdown import Markdown

    plugin = vt.get_plugin_handle(plugin)
    plugin_kwargs = vt.get_plugin_default_kwargs()
    plugin_kwargs['main_input'] = main_input
    if advanced_arg is not None:
        plugin_kwargs['plugin_kwargs'] = advanced_arg
    my_working_plugin = silence_stdout(plugin)(**plugin_kwargs)
    with Live(Markdown(""), auto_refresh=False, vertical_overflow="visible") as live:
        for cookies, chat, hist, msg in my_working_plugin:
            md_str = vt.chat_to_markdown_str(chat)
            md = Markdown(md_str)
            live.update(md, refresh=True)
def cli():
    import argparse
    # Create ArgumentParser object
    parser = argparse.ArgumentParser()
    # Add an argument named 'c' with a short option '-c'.
    # This argument takes one value.
    parser.add_argument('input', nargs='+', help='The input string')
    parser.add_argument('-c', '--cmd', action='store_true', help="Call the commandline helper plugin.")
    parser.add_argument('-a', '--ask', action='store_true', help="A shortcut to ask currently selected llm.")
    parser.add_argument('-s', '--set_conf', action='store_true', help="Set permanent configuration in .bashrc")
    args = parser.parse_args()
    if args.set_conf:
        assert len(args.input) == 2, '参数数量错误，示例 ` vt --set_conf API_KEY "sk-abcdefghijklmn" `'
        add_env_variable(args.input[0], args.input[1])
    if args.ask:
        inputs = " ".join(args.input)
        LLM_MODEL, = vt.get_conf('LLM_MODEL')
        plugin_shortcut(inputs, plugin='crazy_functions.询问多个大语言模型->同时问询_指定模型', advanced_arg={"advanced_arg": LLM_MODEL})
    elif args.cmd:
        # use the commandline helper shortcut
        inputs = " ".join(args.input)
        plugin_shortcut(inputs, plugin='crazy_functions.命令行助手->命令行助手')
    else:
        # echo, do nothing
        print(args.input)



