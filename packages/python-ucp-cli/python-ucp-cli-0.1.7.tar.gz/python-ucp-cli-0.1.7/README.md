# A Docker Universal Control Plane CLI 

[![asciicast](https://asciinema.org/a/05qkp37lroHzKcfxRfu60scGD.png)](https://asciinema.org/a/05qkp37lroHzKcfxRfu60scGD)


This `ucp-cli login` command will download your user bundle and auth token into the ~/.ucp directory.
With `eval $(ucp-cli env)` you can then access the docker or kubectl context.

Reference: https://docs.docker.com/ee/ucp/user-access/cli/


## Installation

Run the following to install:

```
$ pip install python-ucp-cli
```

## Usage

```bash

$ ucp-cli login --username user1 --password password --url ucp-manager.local

$ eval $(ucp-cli env)

$ docker node ls
...

$ kubectl get node
...

```


## Developer

```
virtualenv venv
ls venv/
. venv/bin/activate
which python
```

```
rm -rf ./build && rm -rf ./dist
python setup.py sdist bdist_wheel
ls build/
pip install -e .
```

```
check-manifest --create
git add MANIFEST.in
```

```
pip install  . -vvv | grep 'adding'
```

```
python setup.py bdist_wheel sdist
ls dist/
tar tzf dist/python-ucp-cli-0.1.7.tar.gz

twine upload dist/*

pip uninstall python-ucp-cli
pip install --no-cache-dir python-ucp-cli --user
pip show python-ucp-cli


### Get Started

For usage and help content, pass in the `-h` parameter, for example:

