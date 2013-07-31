#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
activate_this = PROJECT_PATH + '/venv/Scripts/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from PySide import QtGui, QtCore
import sys

class MainWindow(QtGui.QMainWindow):
    def __init__(self, *args):
        apply(QtGui.QMainWindow.__init__, (self,) + args)
        
        self.createActions()
        self.createTrayIcon()
        self.setIcon()
        self.trayIcon.show()
        
        self.resize(220, 100)
        self.setWindowTitle('Shinpuru Timer')
        self.setWindowIcon(QtGui.QIcon('resources/icons/clock.png'))
        
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        
        self.gridLayoutWidget = QtGui.QWidget(self.centralWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(1, 1, 219, 89)) #( x, y, w, h)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtGui.QTextBrowser(self.gridLayoutWidget)
        self.textBrowser.setReadOnly(False)
        self.textBrowser.setOverwriteMode(False)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.centralWidget)
        self.progressBar.setGeometry(QtCore.QRect(1, 90, 219, 10))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.setCentralWidget(self.centralWidget)
        
        self.textBrowser.setHtml(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">Shinpuru Timer</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))



        
    def createActions(self):
        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=self.quit, icon=QtGui.QIcon('resources/icons/quit.png'))

    def setIcon(self):
        icon = QtGui.QIcon('resources/icons/clock.png')
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        
        self.trayIcon.setToolTip("Shinpuru Timer")

    def quit(self):
        QtGui.qApp.quit()
        
    @QtCore.Slot(QtGui.QSystemTrayIcon.ActivationReason)
    def on_trayIcon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            settings = QtCore.QSettings("reedcourty", "Shinpuru")
            self.move(settings.value("pos"))
            self.restoreGeometry(settings.value("geometry"))
            self.restoreState(settings.value("windowState"))
            self.showNormal()

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        
        self.trayIcon.activated.connect(self.on_trayIcon_activated)
        
    def changeEvent(self, event):
        if (event.type() == QtCore.QEvent.WindowStateChange):
            if (self.windowState() and QtCore.Qt.WindowMinimized):
                
                settings = QtCore.QSettings("reedcourty", "Shinpuru")
                settings.setValue("pos", self.pos())
                settings.setValue("geometry", self.saveGeometry())
                settings.setValue("windowState", self.saveState())
                
                event.ignore()
                QtCore.QTimer.singleShot(0, self.close)                
                return
            super(MainWindow, self).changeEvent(event)
    
    def closeEvent(self, event):
        event.ignore()
        self.hide()

def main(args):

    app = QtGui.QApplication(args)
    # Akár a felület stílusát is módosíthatjuk:
    style = QtGui.QStyleFactory.keys()[6]
    # 6 - Cleanlooks
    # 5 - Plastique
    # 4 - CDE
    # 3 - Motif
    # 2 - WindowsVista
    # 1 - WindowsXP
    # 0 - Windows
    app.setStyle(style)
    
    # Ellenőrizzük, hogy támogatott-e az ablakkezelőben a Systray funkció:
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Shinpuru Timer",
                "Az alkalmazás nem indítható el.")
        sys.exit(1)

    app.setQuitOnLastWindowClosed(False)
    
    win = MainWindow()
    win.show()
    app.connect(app, QtCore.SIGNAL("lastWindowClosed()"),
                app, QtCore.SLOT("quit()"))
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)