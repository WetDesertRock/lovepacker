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
            filename = "love-%s-%s.zip"%(version, osname)

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
