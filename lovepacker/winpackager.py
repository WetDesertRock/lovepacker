import zipfile2
import os
import shutil
import subprocess
import plistlib
import logging

from .downloadmanager import DownloadManager

logger = logging.getLogger(__name__)

class WinPackager:
    def __init__(self, windowsbits, options):
        self.options = options
        self.cache = DownloadManager(options)
        self.windowsbits = windowsbits

    def package(self):
        # Get the package
        osname = "win%d"%self.windowsbits
        winzipname = self.cache.getFile(self.options['destdir'], osname=osname, version=self.options['loveversion'])

        winzippath = os.path.join(self.options['destdir'],winzipname)
        finaldirpath = os.path.join(self.options['destdir'],"%s-win%d"%(self.options['gamename'], self.windowsbits))
        exefilepath = os.path.join(finaldirpath,"love.exe")
        gameexepath = os.path.join(finaldirpath,"%s.exe"%self.options['gamename'])
        gamezippath = os.path.join(self.options['destdir'],"%s.love"%self.options['gamename'])
        finalpath = os.path.join(self.options['destdir'], "%s-win%d.zip"%(self.options['gamename'], self.windowsbits))

        # Remove old files if they exists
        logger.debug("Cleaning out old file: %s", finaldirpath)
        shutil.rmtree(finaldirpath, ignore_errors=True)

        try:
            logger.debug("Cleaning out old file: %s", finalpath)
            os.remove(finalpath)
        except FileNotFoundError:
            pass

        #Unzip the package
        winfile = zipfile2.ZipFile(winzippath, 'r')
        windirpath = os.path.commonpath(winfile.namelist())
        windirpath = os.path.join(self.options['destdir'], windirpath)
        winfile.extractall(self.options['destdir'])
        winfile.close()

        # Move love.exe to game.exe
        os.rename(windirpath,finaldirpath)
        os.rename(exefilepath,gameexepath)

        # Concat love.exe and game.love
        logger.info("Making executable: %s", gameexepath)
        exefile = open(gameexepath, "ab")
        lovefile = open(gamezippath, "rb")
        exefile.write(lovefile.read())
        exefile.close()
        lovefile.close()

        # Write zipped file for distribution
        logger.info("Making zip file: %s", finalpath)
        finalzipfile = zipfile2.ZipFile(finalpath, 'w')
        finalzipfile.add_tree(finaldirpath, include_top=True)
        finalzipfile.close()

        os.remove(winzippath)
