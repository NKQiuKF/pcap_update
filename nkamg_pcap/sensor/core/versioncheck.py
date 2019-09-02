#!/usr/bin/env python
# coding=utf-8

import sys

py_version = sys.version.split()[0]
exit_msg = "[CRITICAL] Incompatible Python version detected {py_version}." \
              "For successfully running AntiMal you'll have to use version 2.6 or 2.7.".format(py_version=py_version)
if py_version >= "3" or py_version < "2.6":
    exit(exit_msg)
