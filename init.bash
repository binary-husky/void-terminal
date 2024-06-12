#!/bin/bash
set -e

py=python3
repo_url="https://github.com/binary-husky/gpt_academic.git"
branch="master"
project_dir="void_terminal"
project_dir_tmp="${project_dir}_tmp"

# 检查依赖项
command -v git >/dev/null 2>&1 || { echo >&2 "需要安装git但未找到。正在退出..."; exit 1; }
command -v $py >/dev/null 2>&1 || { echo >&2 "需要安装Python但未找到。正在退出..."; exit 1; }


rm -rf void_terminal
echo "正在克隆仓库..."
git clone --depth=1 $repo_url -b $branch $project_dir

cd $project_dir
$py -m pip install -r requirements.txt
CACHE_ONLY=True $py multi_language.py

cd ..
cp -r $project_dir $project_dir_tmp
rm -rf $project_dir
cp -r $project_dir_tmp/multi-language/English/ $project_dir
rm -rf $project_dir/.git
rm -rf $project_dir_tmp

$py -m pip install .
