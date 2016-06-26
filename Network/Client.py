#coding=utf-8

import sys
import time
import select
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

file_handler = logging.FileHandler("SocketClient.log")
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

class MainClient(QtGui.QWidget):
    """MainClient"""
    def __init__(self):
        super(MainClient, self).__init__()
        self.boxSize = 1
        self.hasReveive = 0
        self.information = ""
        self.infoLength = len(self.information)
        self.log = unicode(duck.read(),"utf-8")
        self.event = threading.Event()
        self.event.set()
        self.locker = threading.Lock()
        self.host = "127.0.0.1"
        self.port = 8090
        self.receiveNext = False
        self.hasStart = False
        self.stopFlag = False
        self.throwFlag = False
        self.sn = 0

        self.getBoxMaxNum()
        self.initUI()
        self.start()

    def initUI(self):
        self.setWindowTitle("Data Communication And Network")
        self.setWindowIcon(QtGui.QIcon("gnome.png"))
        self.setFixedSize(400,400)
        self.center()

        self.boxsizeButton = QtGui.QPushButton("Box Size",self)
        self.boxsizeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.boxsizeButton.move(50,20)
        self.boxsizeLabel = QtGui.QLabel(str(self.boxSize),self)
        self.boxsizeLabel.setGeometry(160,25,20,15)

        self.connect(self.boxsizeButton,QtCore.SIGNAL("clicked()"),self.setBoxsize)

        self.refuseButton = MyButton("Refuse","Cancel",self)
        self.refuseButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.refuseButton.setGeometry(80,100,80,40)
        self.throwButton = MyButton("Throw","Cancel",self)
        self.throwButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.throwButton.setGeometry(240,100,80,40)

        self.connect(self.refuseButton,QtCore.SIGNAL("clicked()"),self.refuse)
        self.connect(self.throwButton,QtCore.SIGNAL("clicked()"),self.throw)

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

        # Draw Data
        painter.setPen(QtGui.QColor(0,0,0))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(255,255,0)))
        for x in xrange(0,self.hasReveive):
            painter.drawRect(45+20*x,60,15,15)

        if self.receiveNext:
            painter.setBrush(QtGui.QColor(0,0,255))
            painter.drawRect(45+20*(self.hasReveive-1),60,15,15)

        painter.setPen(QtGui.QColor(0,0,0))
        painter.setFont(QtGui.QFont("Arial",8))
        i  = 0
        for x in range(16):
            i = i if i != self.boxMaxNum else 0
            painter.drawText(48+20*x,72,str(i))
            i = i+1

        # Draw Box
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QColor(255,0,255))
        painter.drawRect(42.5+20*self.hasReveive,55,20*self.boxSize,25)

        painter.setPen(QtGui.QColor(0,0,0))
        painter.setFont(QtGui.QFont("Arial",12))
        painter.drawText(60,180,"All Received : "+self.information)

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

    def start(self):
        if not self.hasStart:
            self.hasStart = True
            self.transmitClient = TransmitClient(self)
            self.transmitClient.start()
        else:
            self.hasStart = False
            self.transmitClient.s.shutdown(socket.SHUT_RDWR)

    def refuse(self):
        if not self.stopFlag:
            self.stopFlag = True
        else:
            self.stopFlag = False
            t = threading.Thread(target=startAgain,args=((self.transmitClient,)))
            t.start()

    def throw(self):
        if not self.throwFlag:
            self.throwFlag = True
        else:
            self.throwFlag = False

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.start()
            event.accept()
        else:
            event.ignore()

def startAgain(transmitClient):
    transmitClient.run()

class TransmitClient(threading.Thread):
    """TransmitClient"""
    def __init__(self,gui):
        super(TransmitClient, self).__init__()
        self.gui = gui

        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.s.bind((self.gui.host,self.gui.port))
        self.s.listen(100)

    def run(self):
        logger.info("Socket Is Start %s:%d ... "%(self.gui.host,self.gui.port))
        self.gui.update()
        inputs = [self.s]
        outputs = []
        clients = {}
        while True:
            if self.gui.stopFlag:
                logger.info("StopFlag Is True , Stop TransmitClient Soon")
                self.gui.update()
                break
            try:
                readable,writeable,exceptional = select.select(inputs,outputs,[])
                for sock in readable:
                    if sock == self.s:
                        logger.info("One Client Connect")
                        self.gui.update()
                        clientsock,clientaddr = sock.accept()
                        inputs.append(clientsock)
                        outputs.append(clientsock)
                    else:
                        self.gui.update()
                        try:
                            if self.gui.stopFlag:
                                break
                            receiveData = sock.recv(1024)
                            if receiveData :
                                logger.info("Received From client : %s "%receiveData)
                                self.gui.hasReveive += 1
                                self.gui.receiveNext = True
                                self.gui.update()
                                logger.info("Received One More")
                                time.sleep(0.2)
                                if (int(receiveData[:4],2))%self.gui.boxMaxNum == self.gui.sn:
                                    if not self.gui.throwFlag:
                                        sendData = (int(receiveData[:4],2)+1)%self.gui.boxMaxNum
                                        self.gui.receiveNext = False
                                        self.gui.information += receiveData[-1:]
                                        logger.info("All Received %s"%self.gui.information)
                                        self.gui.update()
                                        time.sleep(1)
                                        logger.info("Received Right Data , Ask For Next")
                                        sock.sendall("%04d" %int(bin(sendData)[2:]))
                                        logger.info("Send %04d" %int(bin(sendData)[2:]))
                                        self.gui.update()
                                        with self.gui.locker:
                                            self.gui.sn = (self.gui.sn+1)%self.gui.boxMaxNum
                                    else:
                                        self.gui.hasReveive -= 1
                                        self.gui.receiveNext = False
                                        self.gui.update()
                                        logger.info("Throw Received Data")
                                        self.gui.update()
                                else:
                                    self.gui.hasReveive -= 1
                                    self.gui.receiveNext = False
                                    self.gui.update()
                                    logger.info("This One Is Wrong Delete It")
                                    if not self.gui.throwFlag:
                                        if (int(receiveData[:4],2))%self.gui.boxMaxNum != self.gui.sn:
                                            logger.info("Received Ack Is Wrong , Ask For Right Next")
                                            self.gui.update()
                                            sock.sendall("%04d" %int(bin(self.gui.sn)[2:]))
                                            logger.info("Send %04d" %int(bin(self.gui.sn)[2:]))
                                            self.gui.update()
                            else:
                                try:
                                    inputs.remove(sock)
                                    logger.info("Close Sock Success")
                                    self.gui.update()
                                    break
                                except Exception,e:
                                    logger.info("failed"+str(e))
                                    logger.info("message"+e.message)
                                    self.gui.update()
                        except Exception,e:
                            logger.info("failed"+str(e))
                            logger.info("message"+e.message)
                            self.gui.update()
                            if hasattr(e,"errno") and (e.errno == 9 or e.errno == 104):
                                logger.warning("Client Is Leaved")
                                self.gui.update()
                                break
                            else:
                                logger.error("Clients Error"+str(e))
                                self.gui.update()
                                break
            except KeyboardInterrupt:
                logger.warning("KeyBoard Stop Server")
                self.gui.update()
                self.s.close()
                break
                sys.exit(0)
            except Exception,e:
                logger.info("failed"+str(e))
                logger.info("message"+e.message)
                self.gui.update()
                if hasattr(e,"errno") and e.errno == 9:
                    logger.warning("Client Is Leaved")
                    self.gui.update()
                    continue
                else:
                    break
                    sys.exit(0)

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
    mainClient = MainClient()
    mainClient.show()
    sys.exit(app.exec_())
