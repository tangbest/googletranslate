# -*- coding: utf-8 -*-

# 打开网页
def openUrl(self, sUrl):
    from PyQt5.QtGui import QDesktopServices
    QDesktopServices.openUrl(
        QUrl(sUrl)
    )