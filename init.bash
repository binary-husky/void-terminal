rm -rf void_terminal
git clone --depth=1 https://github.com/binary-husky/gpt_academic.git -b frontier void_terminal
cd void_terminal
CACHE_ONLY=True python multi_language.py
cd ..
cp -r void_terminal void_terminal_tmp
rm -rf void_terminal
cp -r void_terminal_tmp/multi-language/English/ void_terminal
rm -rf void_terminal/.git
rm -rf void_terminal_tmp
pip install .