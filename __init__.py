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

def plugin_shortcut(inputs, plugin):
    from rich.live import Live
    from rich.markdown import Markdown

    plugin = get_plugin_handle(plugin)
    plugin_kwargs = get_plugin_default_kwargs()
    plugin_kwargs['main_input'] = inputs
    my_working_plugin = plugin(**plugin_kwargs)

    with Live(Markdown(""), auto_refresh=False) as live:
        for cookies, chat, hist, msg in my_working_plugin:
            md_str = chat_to_markdown_str(chat)
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
    parser.add_argument('-s', '--set_conf', action='store_true', help="Set permanent configuration in .bashrc")
    args = parser.parse_args()
    if args.set_conf:
        assert len(args.input) == 2, '参数数量错误，示例 ` vt --set_conf API_KEY "sk-abcdefghijklmn" `'
        add_env_variable(args.input[0], args.input[1])
    elif args.cmd:
        # use the commandline helper shortcut
        inputs = " ".join(args.input)
        plugin_shortcut(inputs, plugin='crazy_functions.命令行助手->命令行助手')
    else:
        # echo, do nothing
        print(args.input)



