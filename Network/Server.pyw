#coding=utf-8

import sys
import time
import copy
import socket
import threading
import logging
from PyQt4 import QtGui,QtCore

class DuckLog(object):
    """Duck Log"""
    def __init__(self):
        self.name = "Duck Log"
        self.content = ""

    def write(self,content):
        self.content += content

    def read(self):
        return self.content

    def close(self):
        pass

logger = logging.getLogger("Socket Logging")
formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(lineno)-4d %(message)s', '%Y%b%d %a %H:%M:%S',)

file_handler = logging.FileHandler("SocketServer.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

duck = DuckLog()

duck_handler = logging.StreamHandler(duck)
duck_formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%Y%b%d %a  %H:%M:%S',)
duck_handler.setFormatter(duck_formatter)

logger.addHandler(duck_handler)

logger.setLevel(logging.DEBUG)

class MainServer(QtGui.QWidget):
    """This is the main thread for gui"""
    def __init__(self):
        super(MainServer, self).__init__()

        self.boxSize = 1
        self.hasSend = 0
        self.justSend = 0
        self.sendThread = self.boxSize
        self.log = unicode(duck.read(),"utf-8")
        self.event = threading.Event()
        self.event.set()
        self.locker = threading.Lock()
        self.host = "127.0.0.1"
        self.port = 8090
        self.information = self.inputInfo()
        self.infoLength = len(self.information)
        self.sendData = self.getInfo()
        self.storeData = {}
        self.servers = []
        self.sn = 0
        self.sf = 0

        self.getBoxMaxNum()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Data Communication And NetWork")
        self.setWindowIcon(QtGui.QIcon("Server.ico"))
        self.setFixedSize(400,400)
        self.center()

        self.boxsizeButton = QtGui.QPushButton("Box Size",self)
        self.boxsizeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.boxsizeButton.move(50,20)
        self.boxsizeLabel = QtGui.QLabel(str(self.boxSize),self)
        self.boxsizeLabel.setGeometry(160,25,20,15)

        self.connect(self.boxsizeButton,QtCore.SIGNAL("clicked()"),self.setBoxsize)

        self.startButton = MyButton("Start","Stop",self)
        self.startButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.startButton.setGeometry(80,100,80,40)
        self.pauseButton = MyButton("Pause","Play",self)
        self.pauseButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pauseButton.setGeometry(240,100,80,40)

        self.connect(self.startButton,QtCore.SIGNAL("clicked()"),self.start)
        self.connect(self.pauseButton,QtCore.SIGNAL("clicked()"),self.pause)

        self.edit = QtGui.QTextEdit(self.log,self)
        self.edit.setGeometry(30,230,350,160)
        self.edit.setReadOnly(True)
        self.edit.setFont(QtGui.QFont("Arial",8))

    def setBoxsize(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input BoxSize','Input BoxSize(1-15):')
        if ok:
            if int(text) < 1 or int(text) > 15 :
                logger.warning("BoxSize Is Illegal !")
                self.update()
                QtGui.QMessageBox.warning(self,'Warning',"<center><b>Warning</b></center> <br>Your Input Is Illegal !")
            else:
                self.boxSize = int(text)
                logger.info("Change BoxSize To : "+str(self.boxSize))
                self.getBoxMaxNum()
                self.boxsizeLabel.setText(str(self.boxSize))
                self.update()

    def getBoxMaxNum(self):
        self.sendThread = self.boxSize
        if self.boxSize == 1:
            self.boxMaxNum = 2
        elif self.boxSize < 4:
            self.boxMaxNum = 4
        elif self.boxSize < 8:
            self.boxMaxNum = 8
        elif self.boxSize < 16:
            self.boxMaxNum = 16
        else:
            self.boxMaxNum = 16

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

    def paintEvent(self, e):

        painter = QtGui.QPainter(self)

        self.edit.clear()
        self.log = unicode(duck.read(),"utf-8")
        self.edit.append(self.log)

        # Draw Blank Box
        painter.setPen(QtGui.QColor(0,0,0))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255,255,255)))
        for x in range(16):
            painter.drawRect(45+20*x,60,15,15)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(255,255,0)))
        for x in xrange(0,self.infoLength):
            painter.drawRect(45+20*x,60,15,15)

        # if self.justSend:
        for x in xrange(self.justSend):
            painter.setBrush(QtGui.QColor(0,255,0))
            painter.drawRect(45+20*(self.hasSend+x),60,15,15)

        # Draw Data
        painter.setPen(QtGui.QColor(0,0,0))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255,255,255)))
        for x in xrange(0,self.hasSend):
            painter.drawRect(45+20*x,60,15,15)

        # Draw Box
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QColor(255,0,255))
        painter.drawRect(42.5+20*self.hasSend,55,20*self.boxSize,25)

        painter.setPen(QtGui.QColor(0,0,0))
        painter.setFont(QtGui.QFont("Arial",8))
        i  = 0
        for x in range(16):
            i = i if i != self.boxMaxNum else 0
            painter.drawText(48+20*x,72,str(i))
            i = i+1

        painter.setPen(QtGui.QColor(0,0,0))
        painter.setFont(QtGui.QFont("Arial",12))
        painter.drawText(60,180,"Information : %s"%self.information)

    def start(self):
        self.transmitServer = TransmitServer(self)
        self.transmitServer.start()

    def pause(self):
        if self.event.isSet():
            self.event.clear()
        else:
            self.event.set()

    def inputInfo(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Information','Input Information (less than 16):')
        if ok:
            if len(text)<1 or len(text)>16:
                # pass
                QtGui.QMessageBox.warning(self,'Warning',"<center><b>Warning</b></center> <br>Your Input Is Illegal !")
                return self.inputInfo()
            else:
                logger.info("Information is : "+text)
                return unicode(text,"utf-8")
        else:
            sys.exit(0)

    def getInfo(self):
        for i in self.information:
            yield i

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class TransmitServer(threading.Thread):
    """TransmitServer"""
    def __init__(self,gui):
        super(TransmitServer, self).__init__()

        self.servers = []
        self.storeData = {}
        self.sendAll = False
        self.gui = gui

    def run(self):
        for x in range(self.gui.sendThread):
            logger.info("Server Thread %d Start"%x)
            s = Server(self.gui)
            s.start()
            self.servers.append(s)
            time.sleep(1)
        t = Timer(self.gui)
        t.start()
        for i in self.servers:
            i.join()
            time.sleep(0.1)

    def canSend(self):
        return False if self.storeData else True

class Timer(threading.Thread):
    """Timer"""
    def __init__(self, gui):
        super(Timer, self).__init__()
        self.gui = gui

    def run(self):
        while 1:
            if self.gui.transmitServer.sendAll:
                break
            for i in self.gui.transmitServer.servers:
                if i.isAlive():
                    pass
                else:
                    self.gui.transmitServer.storeData  = copy.copy(self.gui.storeData)
                    logger.info("%s is death"%(str(i.name)))
                    time.sleep(1)
                    i.run()
        logger.info("Timer is death")

class Server(threading.Thread):
    """Server"""
    def __init__(self,gui):
        super(Server, self).__init__()
        self.gui = gui

    def run(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.s.settimeout(5)

        logger.info("Server Start Connect To "+str(self.gui.host)+":"+str(self.gui.port)+"... ")
        self.s.connect((self.gui.host,self.gui.port))

        try:
            while 1:
                self.gui.event.wait()
                try:
                    if self.gui.transmitServer.canSend():
                        self.data = self.gui.sendData.next()
                        self.gui.storeData[self.gui.sn] = self.data
                    else:
                        self.gui.justSend -= 1
                        self.gui.update()
                        self.gui.sn = self.gui.storeData.items()[0][0]
                        self.data = self.gui.storeData.items()[0][1]
                        self.gui.transmitServer.storeData.pop(self.gui.sn)
                        logger.info("%s Resend %s"%(str(self.name),str(self.data)))
                except Exception,e:
                    if len(self.gui.storeData) == 0 and e.message == "":
                        logger.info("Send All Data ")
                        self.gui.transmitServer.sendAll = True
                    logger.info("%s is close"%str(self.name))
                    break
                logger.info("%s Send Data %04d%s"%(str(self.name),int(bin(self.gui.sn)[2:]),str(self.data)))
                with self.gui.locker:
                    self.s.sendall("%04d%s" %(int(bin(self.gui.sn)[2:]),str(self.data)))
                    self.gui.sn = (self.gui.sn+1)%(self.gui.boxMaxNum)
                    self.gui.justSend += 1
                    self.gui.update()
                self.ack = self.s.recv(1024)
                logger.info("%s Receive Ack  %04s"%(str(self.name),self.ack))
                if self.ack:
                    for i in range(self.gui.boxMaxNum):
                        self.gui.hasSend += i
                        time.sleep(0.5)
                        self.gui.justSend -= i
                        self.gui.update()
                        if (self.gui.sf+i)%self.gui.boxMaxNum == int(self.ack,2):
                            self.gui.sf = (self.gui.sf+i)%self.gui.boxMaxNum
                            break
                        self.gui.storeData.pop((self.gui.sf+i)%self.gui.boxMaxNum)
                    else:
                        break
                if len(self.gui.storeData) >= self.gui.boxSize - 1:
                    break
        except Exception, e:
            logger.error("%s ERROR  %s"%(str(self.name),e.message))
            logger.info("This server is close")

class MyButton(QtGui.QPushButton):
    """This is my Button Class"""

    def __init__(self, title, temp, parent):
        super(MyButton, self).__init__(title, parent)
        self.title = title
        self.temp = temp

    def mousePressEvent(self, e):
        QtGui.QPushButton.mousePressEvent(self, e)
        if e.button() == QtCore.Qt.LeftButton:
            if self.text() == self.title:
                self.setText(self.temp)
            else:
                self.setText(self.title)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    server = MainServer()
    server.show()
    sys.exit(app.exec_())
