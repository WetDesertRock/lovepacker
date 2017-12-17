import os
import subprocess
import fnmatch
import zipfile
import logging

logger = logging.getLogger(__name__)

""" Class to bundle game code into a zip file """
class Bundler:
    def __init__(self, options):
        self.options = options

        lovefile = "%s.love"%self.options['gamename']
        zippath = os.path.join(self.options['destdir'],lovefile)

        # Remove old file if it exists
        try:
            os.remove(zippath)
        except FileNotFoundError:
            pass

        self.zipfile = zipfile.ZipFile(zippath, mode='w')

    """ Finds files, compiles them if needed, then zips them into a .love file"""
    def bundle(self):
        for root, dirs, files in os.walk(self.options['basepath'], followlinks = self.options['followlinks']):
            localdir = root[len(self.options['basepath'])+1:]

            for fname in files:
                abspath = os.path.join(root,fname)
                localpath = os.path.join(localdir,fname)

                ignore = False
                for pattern in self.options['ignorepatterns']:
                    if fnmatch.fnmatch(localpath, pattern):
                        ignore = True
                        break

                if abspath.startswith(self.options['buildpath']):
                    ignore = True
                    break


                if not ignore:
                    logger.debug("Adding file: %s", localpath)
                    filepath = self.process(abspath, localpath)
                    self.zipfile.write(filepath, arcname=localpath)

        self.zipfile.close()

    """ Processes the specified file, returns the new path """
    def process(self, abspath, localpath):
        outfile = os.path.join(self.options['buildpath'],'luac',localpath)
        outdir = os.path.dirname(outfile)
        relpath = os.path.relpath(abspath)

        os.makedirs(outdir, exist_ok=True)
        if localpath.endswith(".lua") and "luac" in self.options['processors']:
            logger.debug("Compiling %s with luac", localpath)
            proc = subprocess.run(['luajit','-bg',relpath,outfile])
            #TODO: Check for errors
            return outfile
        else:
            return abspath
