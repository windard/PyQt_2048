#coding=utf-8
#Author:windard Yang
#Time :2016-2-5
#Email:1106911190@qq.com
import sys
import copy
from random import randint
from PyQt4 import QtGui,QtCore

class Game(QtGui.QWidget):
	def __init__(self):
		super(Game,self).__init__()
		self.setWindowTitle("Greed Snake")
		self.setWindowIcon(QtGui.QIcon('snake.ico'))
		self.timer = QtCore.QTimer(self)
		self.difficult = 300
		self.timer.setInterval(self.difficult)
		self.connect(self.timer,QtCore.SIGNAL('timeout()'),self.gameMove)
		self.gameInit()
		self.canCrossWalk = 0
		self.value = 1
		self.initUI()

	def initUI(self):
		self.setFixedSize(350,400)
		self.center()
		cb = QtGui.QCheckBox('Cross Walk', self)
		cb.move(30, 20)
		cb.toggle()
		cb.setCheckState(False)
		cb.setFocusPolicy(QtCore.Qt.NoFocus)
		cb.stateChanged.connect(self.changeState)
		# lbl = QtGui.QLabel("Difficult", self)
		# combo = QtGui.QComboBox(self)
		# combo.setFocusPolicy(QtCore.Qt.NoFocus)
		# combo.addItem("Low")
		# combo.addItem("Medium")
		# combo.addItem("High")
		# combo.move(180, 45)
		# lbl.move(190, 20)
		# combo.activated[str].connect(self.onActivated)
		slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		slider.setFocusPolicy(QtCore.Qt.NoFocus)
		slider.setGeometry(180, 45, 100, 30)
		self.connect(slider, QtCore.SIGNAL('valueChanged(int)'),
		    self.changeValue)
		self.label = QtGui.QLabel("Difficult:"+str(self.value),self)
		self.label.resize(100, 20)	
		self.label.move(190, 20)			
		self.show()

	def changeValue(self,value):
		self.difficult = 3*(100-value)
		self.value = value+1
		self.timer.setInterval(self.difficult)

	def onActivated(self, text):
		if text == "Low":
			self.difficult = 300
		elif text =="Medium":
			self.difficult = 300*0.7
		else :
			self.difficult = 300*0.5
		self.timer.setInterval(self.difficult)

	def changeState(self):
		self.canCrossWalk =0 if self.canCrossWalk else 1

	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def gameInit(self):
		self.location = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5]]
		self.direction = 3
		self.createFood()

	def createFood(self):
		while 1:
			i = randint(0,19)
			j = randint(0,19)
			if [i,j] in self.location :
				continue
			else:
				self.food = [i,j]
				break

	def paintEvent(self,e):
		painter = QtGui.QPainter()
		painter.begin(self)
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(QtGui.QBrush(QtGui.QColor(0,0,0)))
		painter.drawRect(28,78,299,299)
		painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
		for i in self.location :
			painter.drawRect(30+15*i[0],80+15*i[1],10,10)
		painter.drawRect(30+15*self.food[0],80+15*self.food[1],10,10)
		painter.end()
		self.update()

	def gameMove(self):
		head = self.location[-1]
		if self.direction == 0 :
			if self.canCrossWalk:
				self.location.append([(head[0]+1)%20,head[1]])
			else :
				self.location.append([head[0]+1,head[1]])
		elif self.direction == 1:
			if self.canCrossWalk:
				self.location.append([head[0],(head[1]-1)%20])
			else :
				self.location.append([head[0],head[1]-1])
		elif self.direction == 2 :
			if self.canCrossWalk:
				self.location.append([(head[0]-1)%20,head[1]])
			else :
				self.location.append([head[0]-1,head[1]])
		else :
			if self.canCrossWalk:
				self.location.append([head[0],(head[1]+1)%20])
			else:
				self.location.append([head[0],head[1]+1])
		if self.food in self.location :
			self.createFood()
		else:
			self.location.pop(0)
		if self.isOver():
			if QtGui.QMessageBox.question(self,'Message',"<center><b>Game Over</b></center> <br>Do You Want To Restart ?",QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.Yes)==QtGui.QMessageBox.Yes:
				self.gameInit()
			else :
				self.close()
		self.label.setText("Difficult:"+str(self.value))
		self.update()

	def isOver(self):
		for i,j in enumerate(self.location):
			temp = copy.deepcopy(self.location)
			temp.pop(i)
			if j in temp:
				return 1
		else:
			for i in self.location:
				if i[0]>19 or i[0]<0 or i[1]>19 or i[1]<0:
					return 1
			else:
				return 0

	def keyPressEvent(self,e):
		if e.key()==QtCore.Qt.Key_Space:
			self.gameStart()
		elif e.key()==16777220:
			self.gameEnd()
		elif e.key()==QtCore.Qt.Key_Escape:
			self.gameInit()
		elif e.key()==QtCore.Qt.Key_Up:
			if self.direction ==3:
				pass
			else :
				self.direction = 1
		elif e.key()==QtCore.Qt.Key_Down:
			if self.direction ==1:
				pass
			else :
				self.direction = 3
		elif e.key()==QtCore.Qt.Key_Left:
			if self.direction==0:
				pass
			else :
				self.direction = 2
		elif e.key()==QtCore.Qt.Key_Right:
			if self.direction == 2:
				pass
			else :
				self.direction = 0

	def gameStart(self):
		self.timer.start()

	def gameEnd(self):
		self.timer.stop()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	game = Game()
	app.exec_()