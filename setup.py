import setuptools, glob, os, fnmatch, shutil

try:
    shutil.copyfile('__init__.py', 'void_terminal/__init__.py')
    shutil.copyfile('__init__.py', 'void_terminal/__init__.py')
except:
    msg = "You must first clone the mother project with `git clone --depth=1 https://github.com/binary-husky/gpt_academic.git void_terminal`."
    for i in range(1000): print(msg)
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
    version="0.0.3",
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