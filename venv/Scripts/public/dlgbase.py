# -*- coding: utf-8 -*-


class CDlgBase(object):
    # 界面按钮消息
    def onBtnMsg(self, *args):
       pass

    # 可勾选消息
    def onBoxMsg(self, *args):
       pass

    # 菜单按钮消息
    def onActionMsg(self, *args):
       pass

    # 居中
    def Center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 窗口置顶
    def setWindowTop(self, bTop):
        if bTop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.Widget)
            self.show()

    def openUrl(self, sUrl):
        QDesktopServices.openUrl(
            QUrl(sUrl)
        )