# <div align=center> Void Terminal (虚空终端)</div>

The CLI & python API for the well-known project [`gpt_academic`](https://github.com/binary-husky/gpt_academic.git).

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
chat_kwargs['inputs'] = '你好, 世界树。'
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

plugin = vt.get_plugin_handle('crazy_functions.批量Markdown翻译->Markdown翻译指定语言')
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
plugin = vt.get_plugin_handle('crazy_functions.询问多个大语言模型->同时问询_指定模型')
plugin_kwargs = vt.get_plugin_default_kwargs()
plugin_kwargs['main_input'] = '你好, 世界树。'
plugin_kwargs['plugin_kwargs'] = {"advanced_arg": llm_model}
my_working_plugin = plugin(**plugin_kwargs)

with Live(Markdown(""), auto_refresh=False) as live:
    for cookies, chat, hist, msg in my_working_plugin:
        md_str = vt.chat_to_markdown_str(chat)
        md = Markdown(md_str)
        live.update(md, refresh=True)
```



# Installation

```
pip install void-terminal
```

# Installation from source (Equal to running `init.bash`)

### 1. (if you have not clone **THIS** resp) Clone this project, **enter the workfolder** via `cd`.

```
git clone --depth=1 https://github.com/binary-husky/void_terminal.git
cd void_terminal
```

### 2. Clone the **mother project** `GPT-Academic` into a new **sub-folder** called `void_terminal`

```
git clone --depth=1 https://github.com/binary-husky/gpt_academic.git void_terminal
```

### 3. Run setup

```
pip install .
```
