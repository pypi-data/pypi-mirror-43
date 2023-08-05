Developer
virtualenv venv
ls venv/
. venv/bin/activate
which python
rm -rf ./build && rm -rf ./dist
python setup.py sdist bdist_wheel
ls build/
pip install -e .
check-manifest --create
git add MANIFEST.in
pip install  . -vvv | grep 'adding'
python setup.py bdist_wheel sdist
ls dist/
tar tzf dist/python-ucp-cli-0.1.7.tar.gz

twine upload dist/*

pip uninstall python-ucp-cli
pip install --no-cache-dir python-ucp-cli==0.1.7 --user
pip show python-ucp-cli


### Get Started

For usage and help content, pass in the `-h` parameter, for example: