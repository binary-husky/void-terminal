import os
if not os.environ.get("LLM_MODEL", None):
    raise ValueError("Please set the environment variables such as API_KEY, API_URL_REDIRECT and LLM_MODEL (You can refer to config.py in GPT-Academic Repo).")

import void_terminal as vt
from rich.live import Live
from rich.markdown import Markdown

plugin = vt.get_plugin_handle(
    'void_terminal.crazy_functions.SourceCode_Analyse->ParsePythonProject'
)
plugin_kwargs = vt.get_plugin_default_kwargs()
path = os.path.abspath('../setup_import')
plugin_kwargs['main_input'] = path
my_working_plugin = plugin(**plugin_kwargs)

with Live(Markdown(""), auto_refresh=False) as live:
    for cookies, chat, hist, msg in my_working_plugin:
        md_str = vt.chat_to_markdown_str(chat)
        md = Markdown(md_str)
        live.update(md, refresh=True)