rm -rf build
rm -rf dist
rm -rf void_terminal/fake_gradio
python setup.py sdist bdist_wheel
twine upload dist/*