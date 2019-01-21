#!/usr/bin/env python3

import sys
from distutils.core import setup

def main():
    if sys.version_info[0] != 3:
        sys.exit("This script requires Python 3")

    setup(
        name = "lovepacker",
        packages = ["lovepacker"],
        version = "1.0.5",
        description = "Packages up LOVE games for distribution. Currently handles MacOS, Windows, and .love files.",
        author = "WetDesertRock",
        author_email = "wetdesertrock@gmail.com",
        url = "https://github.com/WetDesertRock/lovepacker",
        download_url = "https://github.com/WetDesertRock/lovepacker/archive/1.0.4.tar.gz",
        keywords = ["love", "love2d", "packager", "package"],
        classifiers = [],
        install_requires = ['zipfile2>=0.0.12'],
        scripts=['bin/lovepacker']
    )


if __name__ == "__main__":
    main()
