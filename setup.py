import setuptools, glob, os, fnmatch, shutil, shlex
from setup_import.fix_import import main
# main(('--application-directories', '.:void_terminal', 'void_terminal/crazy_functions/Langchain知识库.py',))
# main(('void_terminal/crazy_functions/Langchain知识库.py',))

def pack_up_fix_import():
    source_list = glob.glob('./void_terminal/**/*.py', recursive=True)
    confuse_list = [os.path.basename(t).rsplit('.py')[0] for t in glob.glob('./void_terminal/*.py')]
    from setup_import.fix_import import main
    for fp in source_list:
        main(('--application-directories', '.:void_terminal', fp,))
        with open(fp, 'r', encoding='utf-8', newline='') as fd:
            buf = fd.read()
        buf = buf.replace("importlib.import_module('config')",
            "importlib.import_module('void_terminal.config')")
        buf = buf.replace("importlib.import_module('config_private')",
                    "importlib.import_module('void_terminal.config_private')")
        buf = buf.replace(r"""AssertionError("你提供了错误的API_KEY。\n\n1. 临时解决方案：直接在输入区键入api_key，然后回车提交。\n\n2. 长效解决方案：在config.py中配置。")""",
                          r"""AssertionError("You have not provide an API_KEY. \n\n1. In python, run `void_terminal.set_conf('API_KEY', value='sk-abcd')` to load api key\n\n2. In bash, run `vt --set_conf API_KEY 'sk-abcd'`")""")
        with open(fp, 'w', encoding='utf-8', newline='') as fd:
            fd.write(buf)
    return

pack_up_fix_import()

try:
    shutil.copyfile('__init__.py', 'void_terminal/__init__.py')
    shutil.copyfile('__init__.py', 'void_terminal/__init__.py')
except:
    msg = "You must first clone the mother project with `git clone --depth=1 https://github.com/binary-husky/gpt_academic.git void_terminal`."
    for i in range(100): print(msg)
    raise RuntimeError(msg)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    
def _process_requirements():
    packages = open('void_terminal/requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        if pkg.startswith('./docs'):
            continue
        elif pkg.startswith('pydantic'):
            requires.append('pydantic<2')
        else:
            requires.append(pkg)
    return requires

def package_files(directory, black_list):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if not any([k in filename or k in path for k in black_list]):
                paths.append(os.path.join('..', path, filename))
            else:
                print('ignore', filename)
    return paths

extra_files = package_files('void_terminal', 
                            black_list=['multi-language', 'gpt_log', '.git', 'private_upload', 'multi_language.py', 'build', '.github', '.vscode', '__pycache__', 'venv'])

setuptools.setup(
    name="void-terminal",
    version="0.0.7",
    author="Qingxu",
    author_email="505030475@qq.com",
    description="LLM based APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/binary-husky/void-terminal",
    project_urls={
        "Bug Tracker": "https://github.com/binary-husky/void-terminal/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['vt=void_terminal:cli'],
    },
    package_dir={"": "."},
    package_data={"": extra_files},
    include_package_data=True,
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9",
    install_requires=_process_requirements(),
)