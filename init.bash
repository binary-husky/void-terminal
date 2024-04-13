# py=C:/Users/fqxma/AppData/Local/Programs/Python/Python39/python.exe
py=python3

rm -rf void_terminal
git clone --depth=1 https://github.com/binary-husky/gpt_academic.git -b frontier void_terminal
cd void_terminal
$py -m pip install -r requirements.txt
CACHE_ONLY=True $py multi_language.py
cd ..
cp -r void_terminal void_terminal_tmp
rm -rf void_terminal
cp -r void_terminal_tmp/multi-language/English/ void_terminal
rm -rf void_terminal/.git
rm -rf void_terminal_tmp
$py -m pip install .