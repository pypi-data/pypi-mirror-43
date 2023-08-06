# mobtimer

![https://pypi.python.org/pypi/mobtimer/](https://img.shields.io/pypi/v/mobtimer.svg)

A simple timer for mob programming in your OS status bar.

![Screenshot](https://raw.githubusercontent.com/andreif/mobtimer/master/screenshot.png)

Currently supported operating systems:
* macOS


### Install

```bash
# Install with systems Python 2.7 interpreter
$ sudo /usr/bin/python -m pip install mobtimer

# or using pyenv
$ pyenv shell system
$ sudo pip install mobtimer
```

### Usage

```bash
# Start timer for 20 minute mobs  
$ nohup mobtimer &

# or for 25 minute mobs
$ nohup mobtimer 25 &
```

```
$ mobtimer -h
usage: mobtimer [-h] [minutes]

A simple timer for mob programming.

positional arguments:
  minutes     Duration of each mob in minutes. Default: 20

optional arguments:
  -h, --help  show this help message and exit
```
