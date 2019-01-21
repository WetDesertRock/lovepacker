import zipfile2
import os
import shutil
import subprocess
import plistlib
import logging

from .downloadmanager import DownloadManager

logger = logging.getLogger(__name__)

class MacPackager:
    def __init__(self, options):
        self.options = options
        self.cache = DownloadManager(options)

    def package(self):
        # Get the package
        osxfile = self.cache.getFile(self.options['destdir'], osname="mac", version=self.options['loveversion'])

        # Calculate paths
        osxpath = os.path.join(self.options['destdir'],osxfile)
        loveapp = os.path.join(self.options['destdir'], "love.app")
        gameapp = os.path.join(self.options['destdir'], "%s.app"%self.options['gamename'])
        gamezip = os.path.join(self.options['destdir'], "%s.love"%self.options['gamename'])
        finalpath = os.path.join(self.options['destdir'], "%s-macOS.zip"%self.options['gamename'])

        # Remove old files if they exists
        logger.debug("Cleaning out old file: %s", gameapp)
        shutil.rmtree(gameapp, ignore_errors=True)

        try:
            logger.debug("Cleaning out old file: %s", finalpath)
            os.remove(finalpath)
        except FileNotFoundError:
            pass

        #Unzip the package
        osxzipfile = zipfile2.ZipFile(osxpath, 'r')
        osxzipfile.extractall(self.options['destdir'], preserve_permissions=zipfile2.PERMS_PRESERVE_ALL)
        osxzipfile.close()

        os.rename(loveapp, gameapp)

        #Copy the love file into the app bundle
        logger.info("Making .app: %s", gameapp)
        shutil.copy(gamezip, os.path.join(gameapp, "Contents", "Resources") )

        self.editPlist(gameapp)

        # Write zipped file for distribution
        logger.info("Making zip file: %s", finalpath)
        finalzipfile = zipfile2.ZipFile(finalpath, 'w')
        finalzipfile.add_tree(gameapp, include_top=True)
        finalzipfile.close()

        # Clean up
        os.remove(osxpath)

    def editPlist(self, apppath):
        plistpath = os.path.join(apppath, "Contents", "Info.plist")
        plist = plistlib.readPlist(plistpath)
        plist['CFBundleIdentifier'] = self.options['identifier']
        plist['CFBundleName'] = self.options['gamename']
        del plist['UTExportedTypeDeclarations']

        plistlib.writePlist(plist,plistpath)
