
# BeepDrive

![PyPI](https://img.shields.io/pypi/v/beepdrive.svg?label=Version)
![GitHub All Releases](https://img.shields.io/github/downloads/amecava/beepdrive/total.svg?label=GitHub%20downloads)
![PyPI - Downloads](https://img.shields.io/pypi/dm/beepdrive.svg?label=PyPi%20downloads)

BeepDrive, automated PoliMi BeeP folders download.

## Dependencies

[Chrome Browser](https://www.google.com/intl/it_ALL/chrome/) v71-73 (or Chromium)

## Install

### MacOS, Windows
MacOS and Windows users can download the latest GUI releases from https://github.com/amecava/beepdrive/releases.

### Alternatively, using pip3
Using the `PyPi` repositories and the package manager `pip3` (`python3` required), open the terminal and type:

```python
pip3 install beepdrive
```

>  **Warning:** 
For Linux users, beepdrive will be installed by default in the ``~/.local/bin`` directory. 
The ``PATH`` will have to be set accordingly.
One way of doing this is by adding the following line to the ``~/.bashrc`` file:
>
>  ``export PATH=$PATH:$HOME/.local/bin`` 

To update beepdrive from the `PyPi` repositories, open the terminal and type:
```
pip3 install --upgrade beepdrive
```

## Usage

### GUI version

Unzip the OS specific zip file and launch the application. </br>

Alternatively, if you installed beepdrive from the package manager `pip3`, open the terminal and type:

```python
beepdrive
```

### Console version

You can directly specify the output folder path using the `--path` flag, this will launch a console version of beepdrive:

 ```
beepdrive --path /output/folder/path/
```

## Authors

*  **Team 2 Quinti**
