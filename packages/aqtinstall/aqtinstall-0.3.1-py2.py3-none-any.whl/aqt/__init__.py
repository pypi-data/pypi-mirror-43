#!/usr/bin/env python
#
# Copyright (C) 2018 Linus Jahn <lnj@kaidan.im>
# Copyright (C) 2019 Hiroshi Miura <miurahr@linux.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import sys

from aqt.archives import QtArchives
from aqt.installer import QtInstaller


def main():
    parser = argparse.ArgumentParser(prog='aqtinst', description='Install Qt SDK.',
                                     formatter_class=argparse.RawTextHelpFormatter, add_help=True)
    parser.add_argument("qt_version", help="Qt version in the format of \"5.X.Y\"")
    parser.add_argument('host', choices=['linux', 'mac', 'windows'], help="host os name")
    parser.add_argument('target', choices=['desktop', 'android', 'ios'], help="target sdk")
    parser.add_argument('arch', nargs='?', help="\ntarget linux/desktop: gcc_64"
                                                "\ntarget mac/desktop:   clang_64"
                                                "\ntarget mac/ios:       ios"
                                                "\nwindows/desktop:      win64_msvc2017_64, win64_msvc2015_64"
                                                "\n                      in32_msvc2015, win32_mingw53"
                                                "\nandroid:              android_x86, android_armv7")
    args = parser.parse_args()
    arch = args.arch
    target = args.target
    os_name = args.host
    if arch is None:
        if os_name == "linux" and target == "desktop":
            arch = "gcc_64"
        elif os_name == "mac" and target == "desktop":
            arch = "clang_64"
        elif os_name == "mac" and target == "ios":
            arch = "ios"
    if arch == "":
        print("Please supply a target architecture.")
        args.print_help()
        exit(1)
    qt_version = args.qt_version

    QtInstaller(QtArchives(os_name, qt_version, target, arch)).install()

    sys.stdout.write("\033[K")
    print("Finished installation")
