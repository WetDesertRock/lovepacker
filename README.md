# Love Packer
Packages up LOVE games for distribution. Currently handles MacOS, Windows, and .love files.

## Install
Either use:

```$ python setup.py install```

or

```$ pip install lovepacker```

## About
This is a simple Python 3.x program used to to quickly package games for distribution.

## Features
 * Builds complete and finalized MacOS, Windows, and .love files
 * LOVE file downloading and caching
 * Choose to package up luac compiled bytecode files
 * Config file to avoid endless command line arguments.
 
## Possible Improvements
I made this to fit my specific requirements. There are a few extra features I would eventually like to build into it.

 * Icon files (and creation?)
 * Android bundling.
 * Fancy .dmg creation (with pretty graphics and everything)

## How to use
```
$ lovepacker <target>
```

For the command line arguments, see lovepacker -v.

You can also use config files. If there is a file titled "lovepacker.json" in the root folder of your game, it will automatically get used. For config file format see below example:

```json
{
    "basepath": "~/Desktop/Development/lovegames/LD40/source", 
    "buildpath": "build", 
    "cachepath": "~/.lovepacker/cache", 
    "followlinks": true, 
    "gamename": "M", 
    "identifier": "com.wetdesertrock.m_game", 
    "ignorepatterns": [
        "*.DS_Store", 
        "*.git*"
    ], 
    "loveversion": "0.10.2", 
    "processors": [
        "luac"
    ]
}
```
