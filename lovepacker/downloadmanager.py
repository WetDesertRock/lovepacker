import os
import urllib.request
import shutil
import logging

logger = logging.getLogger(__name__)

class DownloadManager:
    def __init__(self, options):
        self.cachepath = options['cachepath']

    def getFile(self, dest, filename=None, osname=None, version=None):
        if filename == None:
            fileNamingInfo = self.getFileNamingInfo(version)
            filename = fileNamingInfo[osname]

        # Check if it exists in the cache
        filecachepath = os.path.join(self.cachepath, filename)
        if not os.path.isfile(filecachepath):
            self.downloadFile(filename)
        else:
            logger.debug("Using existing cached file: %s", filecachepath)

        # Copy it over to the target
        shutil.copy(filecachepath, dest)

        return filename

    def downloadFile(self, filename):
        url = "https://bitbucket.org/rude/love/downloads/%s"%filename
        filecachepath = os.path.join(self.cachepath, filename)

        logger.info("Downloading %s", url)

        # TODO: Use report hook for updating download display
        return urllib.request.urlretrieve(url, filename=filecachepath)


    def getFileNamingInfo(self, versionStr):
        """
        Returns a dict of filenames to download
        Can parse two versions of the version string, minor.patch and major.minor.patch
        """

        #Parse the version string
        versionSplit = versionStr.split(".")
        if len(versionSplit) == 2:
            (minor,patch) = versionSplit
            major = "0"
        elif len(versionSplit) == 3:
            (major,minor,patch) = versionSplit
        else:
            raise ValueError("Unknown version string: %s"%versionStr)

        fullVersionStr = "%s.%s.%s"%(major,minor,patch)
        weirdFullVersionStr = "%s.%s.0"%(minor,patch)
        shortVersionStr = "%s.%s"%(minor,patch)

        # Start with the default:
        downloadPaths = {
            "mac": "love-%s-macosx-x64.zip"%(fullVersionStr),
            "win32": "love-%s-win32.zip"%(fullVersionStr),
            "win64": "love-%s-win64.zip"%(fullVersionStr),
        }

        # At 11.0 vesion naming changed
        if int(minor) >= 11:
            downloadPaths["mac"] = "love-%s-macos.zip"%weirdFullVersionStr
            downloadPaths["win32"] = "love-%s-win32.zip"%weirdFullVersionStr
            downloadPaths["win64"] = "love-%s-win64.zip"%weirdFullVersionStr

        # At 11.1 it changed again
        if int(minor) >= 11 and int(patch) >= 1:
            downloadPaths["mac"] = "love-%s-macos.zip"%shortVersionStr
            downloadPaths["win32"] = "love-%s-win32.zip"%shortVersionStr
            downloadPaths["win64"] = "love-%s-win64.zip"%shortVersionStr


        return downloadPaths
