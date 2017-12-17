import os
import argparse
import json
import logging

import bundler
import macpackager
import winpackager

# Set up logging
logging.basicConfig(format='%(levelname)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger("main")

def main():
    parser = argparse.ArgumentParser(description='Package a LOVE game into OS specific packages')
    parser.add_argument('basepath', type=str, help='The root directory of your game (should be playable by $ love <basepath>)')
    parser.add_argument('-n', '--gamename', type=str, help='The name of the game.')
    parser.add_argument('-o', '--output', dest='buildpath', type=str, help='What directory to use in building the packages')
    parser.add_argument('-l', '--loveversion', type=str, help='LOVE version string to use')
    parser.add_argument('-L', '--followlinks', action='store_true', help='Follow symlinks in your source code')
    parser.add_argument('-i', '--identifier', type=str, help='Identifies the package on MacOS.')
    parser.add_argument('-c', '--cache', dest='cachepath', type=str, help='Directory to store cache files. Defaults to .lovepacker/cache in your home dir.')
    parser.add_argument('--ignore', nargs='*', dest='ignorepatterns', type=str, help='Patterns of file paths to ignore.')
    parser.add_argument('--processors', nargs='*', type=str, help='List of processors to use when building the lovefile.')
    parser.add_argument('--config', type=str, help='Config path to a .json config file. By default will use <basepath>/build.conf.json if avaliable.')
    parser.add_argument('--loglevel', type=str, choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"], default="INFO", help='Sets the logging level.')

    options = getDefaultOptions()

    args = parser.parse_args()

    args.loglevel
    logging.getLogger().setLevel(args.loglevel)

    if args.config != None:
        loadConfig(options, args.config)
    else:
        configpath = os.path.join(args.basepath, "lovepacker.json")
        if os.path.isfile(configpath):
            loadConfig(options, configpath)

    # Merges the commandline arguments into the options
    mergeIntoDict(options, vars(args))

    finalizeOptions(options)
    initPaths(options)


    logger.info("Building to path: %s"%options['buildpath'])

    bundle = bundler.Bundler(options)
    bundle.bundle()

    mac = macpackager.MacPackager(options)
    mac.package()

    win = winpackager.WinPackager(32,options)
    win.package()

    win = winpackager.WinPackager(64,options)
    win.package()


#### Functions ####

def loadConfig(options, configpath):
    logger.info("Loading config: %s"%configpath)
    data = json.load(open(configpath))
    mergeIntoDict(options, data)

def getDefaultOptions():
    return {
        "basepath": "",
        "buildpath": "build",
        "cachepath": "~/.lovepacker/cache",
        "followlinks": True,
        "ignorepatterns": ["*.DS_Store", "*.git*"],
        "processors": ['luac'],
        "loveversion": "0.10.2",
        "gamename": "unnamed_game",
        "identifier": "com.unnamed.game"
    }

""" Build directories used """
def initPaths(options):
    os.makedirs(options['buildpath'], exist_ok=True)
    os.makedirs(options['destdir'], exist_ok=True)
    os.makedirs(options['cachepath'], exist_ok=True)


""" finalizeOptions takes the options dict and normaizes paths and creates new variables"""
def finalizeOptions(options):
    options['basepath'] = normalizepath(options['basepath'])

    # Unless given a relative path or an absolute path, make it relative to the basepath
    buildpath = options['buildpath']
    if not buildpath.startswith("./") and not buildpath.startswith("/"):
        options['buildpath'] = os.path.join(options['basepath'], options['buildpath'])

    options['buildpath'] = normalizepath(options['buildpath'])
    options['cachepath'] = normalizepath(options['cachepath'])
    options['destdir'] = os.path.join(options['buildpath'],'final')


""" For each key in newdict, if it is not None, add it to basedict """
def mergeIntoDict(basedict, newdict):
    for k in newdict:
        if k in basedict:
            if newdict[k] != None:
                basedict[k] = newdict[k]

""" Take a path and normalize it to an absolute path, resolve the user and clean it up """
def normalizepath(path):
    path = os.path.normpath(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path


if __name__ == "__main__":
    main()
