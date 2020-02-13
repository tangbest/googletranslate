# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from googletrans import Translator
from widgets import ui_googlemain

class CMainDlg(QMainWindow, ui_googlemain.Ui_MainWindow):
    def __init__(self):
        super(CMainDlg, self).__init__()
        self.setupUi(self)
        self.Center()
        self._initData()
        self._initLayer()
        self.show()

    def _initData(self):
        self.m_iLanType = 0
        self.m_sDestLan = "zh-CN"
        self.m_oCurLan = QTranslator()
        self.m_bIsRealTimeTrans = False  # 是否实时翻译
        self.m_oThreadTrans = None  # 翻译线程

    def _initLayer(self):
        self._initStyle()
        self.txtEditOri.setFocus(True)

    def _initStyle(self):
        qss_file = QFile(":Res/style.qss")
        qss_file.open(QFile.ReadOnly)
        qss = str(qss_file.readAll(), encoding='utf-8')
        qss_file.close()
        self.setStyleSheet(qss)
        return
        try:
            with open(sStylePath) as f:
                style = f.read()  # 读取样式表
                self.setStyleSheet("../Res/style.qss")
        except:
            print("open stylesheet error")

    # 界面按钮消息
    def onBtnMsg(self):
        pSender = self.sender()
        if pSender == self.btnTran:
            self._translateText()
        elif pSender == self.btnCopy:
            self._copyResultText()

    # 可勾选消息
    def onBoxMsg(self, *args):
        print(args)
        pSender = self.sender()
        if pSender == self.cBoxTop:
            bChecked = self.cBoxTop.isChecked()
            self.setWindowTop(bChecked)

    # 菜单按钮消息
    def onActionMsg(self, *args):
        pSender = self.sender()
        if pSender == self.actOpen:
            self.openFile()
        elif pSender == self.actExport:
            self.exportFile()
        elif pSender == self.actQuit:
            self.quitApp()
        elif pSender == self.actLanCN:
            self.changeCurLan(0)
        elif pSender == self.actLanEN:
            self.changeCurLan(1)
        elif pSender == self.actAbout:
            self.openUrl("https://www.baidu.com")
        elif pSender == self.actDestZhong:
            self.destinationLanguage(0)
        elif pSender == self.actDestYing:
            self.destinationLanguage(1)
        elif pSender == self.actDestRi:
            self.destinationLanguage(2)
        elif pSender == self.actDestHan:
            self.destinationLanguage(3)

    def destinationLanguage(self, lan):
        if lan == 0:
            self.m_sDestLan = "zh-CN"
        elif lan == 1:
            self.m_sDestLan = "en"
        elif lan == 2:
            self.m_sDestLan = "ja"
        elif lan == 3:
            self.m_sDestLan = "ko"
        else:
            self.m_sDestLan = "en"
        print("destination-language: ", self.m_sDestLan)

    def openUrl(self, sUrl):
        QDesktopServices.openUrl(
            QUrl(sUrl)
        )

    # 设置当前语言
    def changeCurLan(self, iSetLan):
        import os
        sBase = os.path.abspath(".")
        if iSetLan == 0 and self.m_iLanType != 0:
            self.m_iLanType = 0
            print("[ChangeLan] --> zh_CN")
            sPath = os.path.join(sBase, "../", "zh_CN.qm")
            self.m_oCurLan.load(sPath)
        elif iSetLan == 1 and self.m_iLanType != 1:
            self.m_iLanType = 1
            print("[ChangeLan] --> English")
            sPath = os.path.join(sBase, "../", "en.qm")
            bLoadResult = self.m_oCurLan.load(sPath)
            print("loadresult", bLoadResult)
        else:
            return
        _app = QApplication.instance()
        bResult = _app.installTranslator(self.m_oCurLan)
        print("installresult", bResult)
        self.retranslateUi(self)

    # 打开文件,读取数据
    def openFile(self):
        sFileName, sFileType = QFileDialog.getOpenFileName(self, "Open File", ".")
        if sFileName:
            print("Open: ", sFileName, sFileType)
            with open(sFileName, encoding="utf-8") as f:
                try:
                    self.txtEditOri.setPlainText(str(f.read()))
                except Exception as e:
                    self.txtEditOri.setPlainText(e.args[1])

    # 导出数据到文件
    def exportFile(self):
        sTransTxt = self.txtEditTrans.toPlainText()
        if not sTransTxt:
            return
        sFileName, sFileType = QFileDialog.getSaveFileName(self, "Save File", ".", "Text files(*.txt);;All files(*.*)")
        if sFileName:
            with open(sFileName, "w", encoding="utf-8") as f:
                try:
                    f.write(sTransTxt)
                except Exception as e:
                    self.txtEditTrans.setPlainText(e.args[1])

    def quitApp(self):
        qApp.quit()

    # 窗口置顶
    def setWindowTop(self, bTop):
        if bTop:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.Widget)
            self.show()

    def _translateText(self):
        sOriText = self.txtEditOri.toPlainText()
        if not sOriText:
            return
        self.txtEditTrans.setPlainText("")
        self.txtEditTrans.setPlaceholderText("...")
        self.m_oThreadTrans = CGoogleTransThread(self.m_sDestLan, sOriText)
        self.m_oThreadTrans.threadTrans.connect(self._finishedTrans)
        self.m_oThreadTrans.start()


    def _finishedTrans(self, sTransText):
        if sTransText:
            self.txtEditTrans.setPlainText(sTransText)
        else:
            self.txtEditTrans.setPlainText("error!")

    def _copyResultText(self):
        sText = self.txtEditTrans.toPlainText()
        if not sText:
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(sText)

    def Center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class CGoogleTransThread(QThread):
    threadTrans = pyqtSignal(str)

    def __init__(self, sDestTrans, sContent):
        super(CGoogleTransThread, self).__init__()
        self.m_sDestTrans = sDestTrans
        self.m_sContent = sContent

    def run(self):
        lstData = []
        sResultData = ""
        oTran = Translator(service_urls=["translate.google.cn"])
        # ts = T.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='zh-CN')
        try:
            oText = oTran.translate(self.m_sContent, dest=self.m_sDestTrans)
            if isinstance(oText.text, list):
                for i in oText:
                    lstData.append(i.text)
                sResultData = " ".join(lstData)
            else:
                sResultData = oText.text
        except:
            sResultData = "An error happended. Please retry..."
        self.threadTrans.emit(sResultData)  # emit signal once translatation is finfished

def Start():
    import sys
    app = QApplication(sys.argv)
    w = CMainDlg()
    sys.exit(app.exec_())