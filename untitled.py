# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from video_download import *
from Log_packet import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
from PyQt5 import uic
import requests,sys,socket
from urllib import request
import urllib,os,time
import threading
import configparser as CP

log = CreateLog()
logger = log.get_loggger()

#设置超时时间为30秒
socket.setdefaulttimeout(50)

#下载超时文件列表keys-value
failed_list ={}

def down_video(url, file_name,Schedule):
    try:
        urllib.request.urlretrieve( url=url, filename=file_name, reporthook=Schedule )
    except socket.timeout:
        count = 1
        while count <= 5:
            try:
                urllib.request.urlretrieve(url=url, filename=file_name, reporthook=Schedule )
                break
            except socket.timeout:
                err_info = 'Reloading for %d time' % count if count == 1 else 'Reloading for %d times' % count
                print(err_info)
                count += 1
        if count > 5:
            failed_list[file_name] = url
            print( "downloading file fialed!" )

def Schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 1
    sys.stdout.write("  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r')
    sys.stdout.flush()
    logger.info("  " + "%.2f%% 已经下载的大小:%ld 文件大小:%ld" % (per, a * b, c) + '\r')

class EmittingStream(QtWidgets.QWidget,QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)
    def write(self,text):
        self.textWritten.emit(str(text))

class myThread( threading.Thread ):
    def __init__(self, url, filename,text):
        threading.Thread.__init__( self )
        self.url = url
        self.filename = filename
        self.text = text

    def run(self):
        for i in range(len(self.url)):
            print('%s文件开始下载...' % self.filename[i])
            self.text.append('%s文件开始下载...' % self.filename[i])
            QtGui.QGuiApplication.processEvents()
            time.sleep( 0.1 )
            logger.info( '%s文件开始下载...' % self.filename[i] )
            down_video(self.url[i],self.filename[i],Schedule)
            print('%s文件下载已完成.'%self.filename[i])
            self.text.append('%s文件下载已完成.'%self.filename[i])
            logger.info('%s文件下载已完成.'%self.filename[i])

class Ui_Form(object):
    def __init__(self):
        config = CP.ConfigParser()
        config.read('config.ini')
        self.proxy_url = config.get('url','proxy_url')
        self.target_url = config.get('url','target_url')
        self.file_num = config.get('num','file_start')
        self.thread_num = config.get('num', 'thread_num')
        self.file_type = config.get('type','file_type')

        self.video_download = VideoCrawler()
        self.filename = 'test'
        self.mergename = 'video'
        self.m3u8_url = 'http://cache.utovr.com/201508270528174780.m3u8'
        self.download_path = r'C:\Users\v_liucshliu\PycharmProjects\learn\Mul-DownLoad_Video\\video'
        self.final_path = r'C:\Users\v_liucshliu\PycharmProjects\learn\Mul-DownLoad_Video'

        # sys.stdout = EmittingStream(textWritten=self.normalOutputWritten )

    # def __del__(self):
    #     #Restore sys.stdout
    #     sys.stdout = sys.__stdout__

    def normalOutputWritten(self,text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition( QtGui.QTextCursor.End )
        cursor.insertText( text )
        self.textEdit.setTextCursor( cursor )
        self.textEdit.ensureCursorVisible()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(501, 479)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(90, 200, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(80, 10, 131, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(80, 160, 401, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 170, 54, 12))
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(310, 10, 171, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(240, 20, 61, 16))
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
        self.textEdit.setGeometry(QtCore.QRect(10, 240, 481, 291))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 200, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.lineEdit_2.setText( self.filename )
        self.lineEdit_3.setText( self.m3u8_url )
        self.lineEdit_4.setText( self.mergename )
        self.lineEdit_6.setText( self.download_path )
        self.lineEdit_5.setText( self.final_path )

        self.pushButton.clicked.connect( self.on_DownLoad)
        self.pushButton_2.clicked.connect( self.on_format_ts)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "DownLoad"))
        self.label_2.setText(_translate("Form", "FileName:"))
        self.label_3.setText(_translate("Form", "M3u8_Url:"))
        self.label_4.setText(_translate("Form", "MergeName:"))
        self.label_5.setText(_translate("Form", "Final_Path:"))
        self.label_6.setText(_translate("Form", "Download_Path:"))
        self.pushButton_2.setText(_translate("Form", "ForMat"))

    def on_DownLoad(self, From):
        self.get_parameter()
        url_list = self.video_download.parse_m3u8()
        filename_list = []
        filename_num = int(self.file_num)
        length = int( self.file_num )
        start = time.time()
        threads = []
        for i in range(filename_num,len(url_list)):
            filename_num = filename_num+1
            file_name = self.download_path + '\\' + self.filename + str( filename_num ) + '.ts'
            filename_list.append(file_name)
        #self.textEdit.append('文件总数：%d ' % len( url_list ))
        logger.info('文件总数：%d ' % len( url_list ))
        print('文件总数：%d ' % len( url_list ))
        thread_num = int(self.thread_num)
        step = int(len(url_list)/thread_num)+1
        url_list_th = [url_list[i:i + step] for i in range(length,len(url_list),step)]
        filename_list_th = [filename_list[i:i+step] for i in range(length,len(filename_list),step)]
        # print(url_list_th)
        for i in range(int(self.thread_num)):
            t = myThread(url_list_th[i],filename_list_th[i],self.textEdit)
            threads.append(t)

        for i in range(int(self.thread_num)):
            threads[i].start()

        for i in range(int(self.thread_num)):
            threads[i].join()
        end = time.time()
        if(len(failed_list) != 0):
            print("%d try again..."%len(failed_list))
            for keys,value in failed_list.items():
                down_video(url=value,filename=keys,Schedule=Schedule)
            failed_list.clear()
            print("all faile file down success!")
        self.textEdit.append( '所有文件下载完成. 耗时:%f'%(end-start))
        logger.info( '所有文件下载完成. 耗时:%f'%(end-start))
        print('\n下载完成！')

    def merge(self):
        # 获取当前时间
        time_now = int(time.time())
        # 转换成localtime
        time_local = time.localtime( time_now )
        # 转换成新的时间格式(2016-05-09 18:59:20)
        dt = time.strftime("%S",time_local)
        os.system( 'copy/b %s\\*.ts %s\\%s.%s' % (self.download_path,self.final_path,self.mergename+str(dt),self.file_type))
        self.textEdit.append( '合并完成' )
        print( '合并完成!' )

    def remove(self):
        files = os.listdir( self.download_path )
        for filena in files:
            del_file = self.download_path + '\\' + filena
            os.remove( del_file )
            self.textEdit.setText('%s文件已移除'%filena)
            QtGui.QGuiApplication.processEvents()
            time.sleep(0.1)
        self.textEdit.setPlainText( '合并已完成,所有已移除文件.' )
        print( '合并已完成,所有已移除文件.')
        logger.info('合并已完成,所有已移除文件.')

    def get_parameter(self):
        self.filename = self.lineEdit_2.text()
        self.m3u8__url = self.lineEdit_3.text()
        self.download_path = self.lineEdit_6.text()
        self.final_path = self.lineEdit_5.text()
        self.mergename = self.lineEdit_4.text()

    def on_format_ts(self):
        self.merge()
        self.remove()
        #ffmpeg -i media.ts -vcodec copy -acodec copy media.mp4

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.resize(500,535)
    widget.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    widget.setFixedSize(widget.width(),widget.height())
    widget.show()
    sys.exit(app.exec_())
