# -*- coding: utf-8 -*-

class CAppInit(object):
    def __init__(self):
        self._initSysPath()

    def _initSysPath(self):
        import os
        import sys
        lstPath = [
            "..\\Scripts",
            "..\\Scripts\\main",
            "..\\Scripts\\qrcpy",
        ]
        for sPath in lstPath:
            sys.path.append(sPath)

CAppInit()

def Start():
    import dlgmain
    dlgmain.Start()

Start()