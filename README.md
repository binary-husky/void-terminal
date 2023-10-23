# <div align=center> Void Terminal</div>

The CLI & python API for the well-known project [`gpt_academic`](https://github.com/binary-husky/gpt_academic.git).

# Installation
1. Pip installation.
```
pip install void-terminal
```

2. source installation.
```
bash init.bash
```

# Usage (Commandline)

- Chat

```
vt -a "hello, world!"
```

- Ask about how to do a linux command 

```
vt -c "List all docker containers currently running on this system"
```


- Config (For all possible configurations, read [`config.py`](https://github.com/binary-husky/gpt_academic/blob/master/config.py) in the mother project.)
```
# Warning! This will write configuration into .bashrc and change your ENV variables !! Use with caution !! 警告，该命令会修改你的.bashrc文件，持久修改你的环境变量
vt --set_conf API_KEY "sk-123456789123456789123456789"
vt --set_conf LLM_MODEL "gpt-3.5-turbo"
vt --set_conf DEFAULT_WORKER_NUM "20"
```


# Usage (Python API)

- Chat without interaction

```python
import void_terminal as vt
# For more available configurations (including network proxy, api, using chatglm etc.), 
# see config.py of in the mother project:
# https://github.com/binary-husky/gpt_academic.git
vt.set_conf(key="API_KEY", value="sk-xxxxxxxxxxxxxx")   
vt.set_conf(key="LLM_MODEL", value="gpt-3.5-turbo")

chat_kwargs = vt.get_chat_default_kwargs()
chat_kwargs['inputs'] = 'Hello, world!'
result = vt.get_chat_handle()(**chat_kwargs)
print('\n*************\n' + result + '\n*************\n' )
```


- Using mother project's plugin (Example: translate THIS readme file to Chinese)

```python
import void_terminal as vt
from rich.live import Live
from rich.markdown import Markdown

vt.set_conf(key="API_KEY", value="sk-xxxxxxxxxxxxxx")
vt.set_conf(key="LLM_MODEL", value="gpt-3.5-turbo")

plugin = vt.get_plugin_handle('void_terminal.crazy_functions.BatchTranslateMarkdown->TranslateMarkdownToSpecifiedLanguage')
plugin_kwargs = vt.get_plugin_default_kwargs()
plugin_kwargs['main_input'] = './README.md'
my_working_plugin = plugin(**plugin_kwargs)

with Live(Markdown(""), auto_refresh=False) as live:
    for cookies, chat, hist, msg in my_working_plugin:
        md_str = vt.chat_to_markdown_str(chat)
        md = Markdown(md_str)
        live.update(md, refresh=True)
```

- Using mother project's plugin (Example: chat with multiple LLM models)

```python
import void_terminal as vt
from rich.live import Live
from rich.markdown import Markdown

llm_model = "gpt-3.5-turbo&gpt-4"
vt.set_conf(key="API_KEY", value="sk-xxxxxxxxxxxxxx")
vt.set_conf(key="LLM_MODEL", value=llm_model)
plugin = vt.get_plugin_handle('void_terminal.crazy_functions.InquiryMultipleLargeLanguageModels->SimultaneousInquiry')
plugin_kwargs = vt.get_plugin_default_kwargs()
plugin_kwargs['main_input'] = 'Hello, world!'
plugin_kwargs['plugin_kwargs'] = {"advanced_arg": llm_model}
my_working_plugin = plugin(**plugin_kwargs)

with Live(Markdown(""), auto_refresh=False) as live:
    for cookies, chat, hist, msg in my_working_plugin:
        md_str = vt.chat_to_markdown_str(chat)
        md = Markdown(md_str)
        live.update(md, refresh=True)
```






