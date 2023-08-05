## A Docker Universal Control Plane CLI 


[![asciicast](https://asciinema.org/a/05qkp37lroHzKcfxRfu60scGD.png)](https://asciinema.org/a/05qkp37lroHzKcfxRfu60scGD)


This `ucp-cli login` command will download your user bundle and auth token into the ~/.ucp directory.
With `eval $(ucp-cli env)` you can then access the docker or kubectl context.

Reference: https://docs.docker.com/ee/ucp/user-access/cli/


## Installation

Run the following to install:

```
$ pip install python-ucp-cli
```


### Get Started

For usage and help content, pass in the `--help` parameter, for example:

```bash

$ ucp-cli --help

Usage: ucp-cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help Show this mesage and exit

Commands:
  env
  login
  org
  team
  user
```

## Login to UCP

```bash
$ pip install python-ucp-cli
...
$ ucp-cli login --username user1 --password password --url ucp-manager.local
Login Succeeded

$ eval $(ucp-cli env)
~
Cluster "ucp_ucp-manager.local:6443_user1" set.
User "ucp_ucp-manager.local:6443_user1" set.
Context "ucp_ucp-manager.local:6443_user1" created.
~
$ docker node ls
ID                          HOSTNAME          STATUS          AVAILABILITY          MANAGER STATUS    ENGINE VERSION 
1nsupdtjmsfsndvm7rsg52cho   ucp-manager.local Ready           Active                                  18.09.0

$ kubectl get node
NAME                  STATUS        ROLES       AGE         VERSION
ucp-manager.local     Ready         master      103d        v1.11.5-docker-4
```


## Manage organizations

```bash