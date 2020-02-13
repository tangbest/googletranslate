# -*- coding: utf-8 -*-

class CAppInit(object):
    def __init__(self):
        print("App Init...")
        self._initSysPath()

    def _initSysPath(self):
        import os
        import sys
        lstPath = [
            "qrcpy",  # 要写这个，否则qrc导出的py，import时找不到模块
        ]
        sBase = os.path.abspath(".")
        print("code base path: ", sBase)
        for sPath in lstPath:
            sFullPath = os.path.join(sBase, sPath)
            print("AppendPath: ", sFullPath)
            sys.path.append(sFullPath)

CAppInit()

def Start():
    print("App Start...")
    from view import dlgmain
    dlgmain.Start()


Start()