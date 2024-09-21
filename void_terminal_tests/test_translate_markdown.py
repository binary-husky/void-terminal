import os
if not os.environ["LLM_MODEL"]:
    raise ValueError("Please set the environment variables such as API_KEY, API_URL_REDIRECT and LLM_MODEL (You can refer to config.py in GPT-Academic Repo).")

# silence all the console outputs from void_terminal
from loguru import logger
logger.disable("void_terminal")

import void_terminal as vt
from rich.live import Live
from rich.markdown import Markdown

plugin = vt.get_plugin_handle(
    'void_terminal.crazy_functions.Markdown_Translate->TranslateMarkdownToSpecifiedLanguage'
)
plugin_kwargs = vt.get_plugin_default_kwargs()
plugin_kwargs['main_input'] = '/home/fuqingxu/void-terminal/README.md'
my_working_plugin = plugin(**plugin_kwargs)

with Live(Markdown(""), auto_refresh=False) as live:
    for cookies, chat, hist, msg in my_working_plugin:
        md_str = vt.chat_to_markdown_str(chat)
        md = Markdown(md_str)
        live.update(md, refresh=True)