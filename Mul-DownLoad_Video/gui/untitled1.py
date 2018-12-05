# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from video_download import *
import requests, sys
from urllib import request
import urllib,os,time
import configparser as CP

class Ui_Form(object):
    def __init__(self):
        config = CP.ConfigParser()
        config.read('config.ini')
        self.proxy_url = config.get('url','proxy_url')
        self.target_url = config.get('url','target_url')
        self.video_download = VideoCrawler()
        self.filename = 'test'
        self.mergename = 'video'
        self.m3u8_url = 'http://cache.utovr.com/201508270528174780.m3u8'
        self.download_path = r'C:\Users\v_liucshliu\PycharmProjects\learn\GUI-DownLoad_Video\\video'
        self.final_path = r'C:\Users\v_liucshliu\PycharmProjects\learn\GUI-DownLoad_Video'

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(501, 540)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(160, 300, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 10, 113, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(80, 210, 401, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 220, 54, 12))
        self.label.setObjectName("label")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 260, 401, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 270, 54, 12))
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(80, 160, 401, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 170, 54, 12))
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(100, 110, 381, 31))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 120, 81, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(Form)
        self.lineEdit_6.setGeometry(QtCore.QRect(100, 60, 381, 31))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 70, 81, 16))
        self.label_6.setObjectName("label_6")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(10, 350, 481, 181))
        self.textEdit.setObjectName("textEdit")

        self.lineEdit_2.setText(self.filename)
        self.lineEdit_3.setText(self.m3u8_url)
        self.lineEdit_6.setText(self.download_path)
        self.lineEdit_5.setText(self.final_path)

        self.pushButton.clicked.connect(self.on_DownLoad)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "DownLoad"))
        self.label_2.setText(_translate("Form", "FileName:"))
        self.label.setText(_translate("Form", "Proxy_Url:"))
        self.label_3.setText(_translate("Form", "M3u8_Url:"))
        self.label_4.setText(_translate("Form", "Target_Url:"))
        self.label_5.setText(_translate("Form", "Final_Path:"))
        self.label_6.setText(_translate("Form", "Download_Path:"))

    def on_DownLoad(self, From):
        self.get_parameter()
        url_list = self.video_download.parse_m3u8()
        for i in range(len(url_list)):
            self.textEdit.append(url_list[i])

        time.sleep(3)

        filename_num = 0
        for j in range(len(url_list)):
            filename_num = filename_num + 1
            file_name = self.download_path + '\\' + self.filename + str(filename_num) + '.ts'
            # self.textEdit.append('下载中:')
            # print('%s下载中:' % file_name)
            urllib.request.urlretrieve(url=url_list[j], filename=file_name, reporthook=self.Schedule)
        self.textEdit.append('下载完成:')
        print('\n下载完成！')
        self.merge()
        self.remove()
        # self.video_download.video_download(url_list)
        #self.video_download.merge()

    def Schedule(self, a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 1
        message =  "  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r'
        self.textEdit.append(message)
        sys.stdout.write( "  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r' )
        sys.stdout.flush()

    def merge(self):
        os.system( 'copy/b %s\\*.ts %s\\%s.mp4' % (self.download_path, self.final_path,self.mergename) )
        self.textEdit.setText( '合并完成' )
        print( '合并完成!' )

    def remove(self):
        files = os.listdir( self.download_path )
        for filena in files:
            del_file = self.download_path + '\\' + filena
            os.remove( del_file )
        self.textEdit.setText( '已移除文件' )
        print( '已移除文件')

    def get_parameter(self):
        self.filename = self.lineEdit_2.text()
        self.m3u8__url = self.lineEdit_3.text()
        self.download_path = self.lineEdit_6.text()
        self.final_path = self.lineEdit_5.text()

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())

