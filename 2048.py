#coding=utf-8
#Author:windard Yang
#Time :2016-2-4
#Email:1106911190@qq.com
import sys
import copy
from random import randint
from PyQt4 import QtGui,QtCore

class PyQtGame(QtGui.QWidget):
	def __init__(self):
		super(PyQtGame,self).__init__()
		self.setWindowIcon(QtGui.QIcon('2048.ico'))
		self.randomInit()
		self.colors = {
			0:QtGui.QColor(0xcdc1b4),
			2:QtGui.QColor(0xeee4da),
			4:QtGui.QColor(0xede0c8),
			8:QtGui.QColor(0xf2b179),
			16:QtGui.QColor(0xf59563),
			32:QtGui.QColor(0xf67c5f),
			64:QtGui.QColor(0xf65e3b),
			128:QtGui.QColor(0xedcf72),
			256:QtGui.QColor(0xedcc61),
			512:QtGui.QColor(0xedc850),
			1024:QtGui.QColor(0xedc53f),
			2048:QtGui.QColor(0xedc22e),
		}
		self.best = 0
		self.initUI()

	def randomInit(self):
		self.tiles = [[0]*4 for i in range(4)]
		for m in range(randint(2,3)):
			self.createColor(4)
		self.score = 0
		self.overed = 0			

	def randomColor(self,rate):
		i = randint(0,rate)
		return 2 if i<rate else 4

	def createColor(self,num):
		while 1:
			i = randint(0,3)
			j = randint(0,3)
			if self.tiles[i][j]==0 :
				self.tiles[i][j] = self.randomColor(num)
				break
			else:
				continue

	def isFull(self):
		for i in range(3):
			if 0 in self.tiles[i]:
				return 0
				break
		else:
			return 1

	def isOverd(self):
		self.rowOvre = 0
		self.colOver = 0
		self.colMove('right',False)
		self.rowMove('down',False)
		if self.rowOvre and self.colOver and self.isFull() :
			self.gameOver()
		if self.score>self.best :
			self.best = self.score

	def initUI(self):
		self.setFixedSize(350,400)
		self.center()
		self.setWindowTitle("2048 Game")
		self.show()

	def center(self):
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def keyPressEvent(self,e):
		if e.key() == QtCore.Qt.Key_Escape:
			self.resetGame()
		elif e.key() == QtCore.Qt.Key_Up:
			self.rowMove('up',True)
		elif e.key() == QtCore.Qt.Key_Down:
			self.rowMove('down',True)
		elif e.key() == QtCore.Qt.Key_Left:
			self.colMove('left',True)
		elif e.key() == QtCore.Qt.Key_Right:
			self.colMove('right',True)
		self.isOverd()
	
	def resetGame(self):
		self.randomInit()
		self.update()

	def mousePressEvent(self,e):
		self.lastPoint=e.pos()

	def mouseReleaseEvent(self,e):
		self.resetRect = QtCore.QRect(240,15,80,60)
		if self.resetRect.contains(e.pos().x(),e.pos().y()) and self.resetRect.contains(self.lastPoint.x(),self.lastPoint.y()):
			if QtGui.QMessageBox.question(self,'Message',"Are You Sure To Reset ?",QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.No)==QtGui.QMessageBox.Yes:
				self.randomInit()
		else :
			dx = e.pos().x()-self.lastPoint.x()
			dy = e.pos().y()-self.lastPoint.y()
			if abs(dx)>abs(dy) and abs(dx)>10:
				if dx>0:
					self.colMove('right',True)
				else:
					self.colMove('left',True)
			elif abs(dy)>10:
				if dy>0:
					self.rowMove('down',True)
				else:
					self.rowMove('up',True)		

	def rowMove(self,direction,temp):
		prevTile = copy.deepcopy(self.tiles)
		for i in range(4):
			firstNumLocation = -1
			firstZeroLocation = -1
			for j in range(4):
				if direction == 'down':
					bigEnd = 3-j
				else:
					bigEnd = j			
				if self.tiles[bigEnd][i]!=0:
					if firstNumLocation==-1 and firstZeroLocation==-1:
						firstNumLocation = bigEnd
						firstNumValue = self.tiles[bigEnd][i]
					elif firstNumLocation==-1 and firstZeroLocation!=-1:
						firstNumLocation = firstZeroLocation
						firstNumValue = self.tiles[bigEnd][i]
						self.tiles[firstZeroLocation][i] = firstNumValue
						self.tiles[bigEnd][i] =0
						if direction=='down' :
							firstZeroLocation -=1
						else :
							firstZeroLocation+=1
					elif firstNumLocation!=-1 and firstZeroLocation!=-1:
						if self.tiles[bigEnd][i] == firstNumValue:
							firstNumValue*=2
							if temp:
								self.score+=firstNumValue
							self.tiles[firstNumLocation][i] = firstNumValue
							self.tiles[bigEnd][i]=0
							firstNumLocation = -1	
						else :
							if direction == 'down' :
								firstNumLocation-=1
							else :
								firstNumLocation+=1
							firstNumValue = self.tiles[bigEnd][i]
							self.tiles[firstNumLocation][i]=firstNumValue
							self.tiles[bigEnd][i]=0       
							if direction =='down' :
								firstZeroLocation-=1		
							else :
								firstZeroLocation+=1
					else:
						if self.tiles[bigEnd][i] == firstNumValue:
							firstNumValue*=2
							if temp:
								self.score+=firstNumValue
							self.tiles[firstNumLocation][i] = firstNumValue
							self.tiles[bigEnd][i]=0
							if direction == 'down' :
								firstZeroLocation = firstNumLocation-1
							else :
								firstZeroLocation = firstNumLocation+1
							firstNumLocation = -1
						else :
							if direction == 'down' :
								firstNumLocation-=1
							else :
								firstNumLocation+=1
							firstNumValue = self.tiles[bigEnd][i]														
					pass
				else:
					if firstZeroLocation ==-1:
						firstZeroLocation = bigEnd
		if temp :
			if prevTile != self.tiles and not self.isFull():
				self.createColor(9)
			self.update()
		else :
			if prevTile == self.tiles :
				self.rowOvre = 1
			self.tiles = copy.deepcopy(prevTile)

	def colMove(self,direction,temp):
		prevTile = copy.deepcopy(self.tiles)
		for i in range(4):
			firstNumLocation = -1
			firstZeroLocation = -1
			for j in range(4):
				if direction == 'right':
					bigEnd = 3-j
				else:
					bigEnd = j			
				if self.tiles[i][bigEnd]!=0:
					if firstNumLocation==-1 and firstZeroLocation==-1:
						firstNumLocation = bigEnd
						firstNumValue = self.tiles[i][bigEnd]
					elif firstNumLocation==-1 and firstZeroLocation!=-1:
						firstNumLocation = firstZeroLocation
						firstNumValue = self.tiles[i][bigEnd]
						self.tiles[i][firstZeroLocation] = firstNumValue
						self.tiles[i][bigEnd] =0
						if direction=='right' :
							firstZeroLocation -=1
						else :
							firstZeroLocation+=1
					elif firstNumLocation!=-1 and firstZeroLocation!=-1:
						if self.tiles[i][bigEnd] == firstNumValue:
							firstNumValue*=2
							if temp:
								self.score+=firstNumValue
							self.tiles[i][firstNumLocation] = firstNumValue
							self.tiles[i][bigEnd]=0
							firstNumLocation = -1	
						else :
							if direction == 'right' :
								firstNumLocation-=1
							else :
								firstNumLocation+=1
							firstNumValue = self.tiles[i][bigEnd]
							self.tiles[i][firstNumLocation]=firstNumValue
							self.tiles[i][bigEnd]=0       
							if direction =='right' :
								firstZeroLocation-=1		
							else :
								firstZeroLocation+=1
					else:
						if self.tiles[i][bigEnd] == firstNumValue:
							firstNumValue*=2
							if temp:
								self.score+=firstNumValue
							self.tiles[i][firstNumLocation] = firstNumValue
							self.tiles[i][bigEnd]=0
							if direction == 'right' :
								firstZeroLocation = firstNumLocation-1
							else :
								firstZeroLocation = firstNumLocation+1
							firstNumLocation = -1
						else :
							if direction == 'right' :
								firstNumLocation-=1
							else :
								firstNumLocation+=1
							firstNumValue = self.tiles[i][bigEnd]															
					pass
				else:
					if firstZeroLocation ==-1:
						firstZeroLocation = bigEnd
		if temp :
			if prevTile != self.tiles and not self.isFull():
				self.createColor(9)
			self.update()
		else :
			if prevTile == self.tiles :
				self.colOver = 1
			self.tiles=copy.deepcopy(prevTile)
				
	def paintEvent(self,e):
		painter = QtGui.QPainter(self)
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(QtGui.QBrush(QtGui.QColor(0xbbada0)))
		painter.drawRect(self.rect())
		painter.setBrush(QtGui.QBrush(QtGui.QColor(0x776e65)))
		painter.drawRoundedRect(QtCore.QRect(20,15,80,60),5,5)
		painter.setFont(QtGui.QFont("Arial",12))
		painter.setPen(QtGui.QColor(0xcdc1b4))		
		painter.drawText(QtCore.QRectF(QtCore.QRect(20,20,80,60)),"SCORE",QtGui.QTextOption(QtCore.Qt.AlignHCenter))
		painter.setFont(QtGui.QFont("Arial",18))
		painter.setPen(QtGui.QColor(255,255,255))	
		painter.drawText(QtCore.QRectF(QtCore.QRect(20,15,80,55)),str(self.score),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom))
		painter.setPen(QtCore.Qt.NoPen)
		painter.drawRoundedRect(QtCore.QRect(130,15,80,60),5,5)
		painter.setFont(QtGui.QFont("Arial",12))
		painter.setPen(QtGui.QColor(0xcdc1b4))			
		painter.drawText(QtCore.QRectF(QtCore.QRect(130,20,80,60)),"BEST",QtGui.QTextOption(QtCore.Qt.AlignHCenter))
		painter.setFont(QtGui.QFont("Arial",18))
		painter.setPen(QtGui.QColor(255,255,255))	
		painter.drawText(QtCore.QRectF(QtCore.QRect(130,15,80,55)),str(self.best),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom))
		painter.setPen(QtCore.Qt.NoPen)
		painter.drawRoundedRect(QtCore.QRect(240,15,80,60),5,5)
		painter.setFont(QtGui.QFont("Arial",16))
		painter.setPen(QtGui.QColor(255,255,255))			
		painter.drawText(QtCore.QRectF(QtCore.QRect(240,15,80,60)),"RESET",QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
		painter.setPen(QtCore.Qt.NoPen)
		self.drawRectangles(painter)

	def drawRectangles(self,painter):
		for i in range(4):
			for j in range(4):
				painter.setFont(QtGui.QFont("Arial",20,10))
				painter.setBrush(self.colors[self.tiles[i][j]])
				painter.drawRoundedRect(QtCore.QRect(20+j*80,90+i*80,60,60),10,10)
				if self.tiles[i][j] != 0:
					if self.tiles[i][j]<15:
						painter.setPen(QtGui.QColor(100,100,100))
					else :
						painter.setPen(QtGui.QColor(255,255,255))
					painter.drawText(QtCore.QRectF(QtCore.QRect(20+j*80,90+i*80,60,60)),str(self.tiles[i][j]),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
					painter.setPen(QtCore.Qt.NoPen)

	def gameOver(self):
		if QtGui.QMessageBox.question(self,'Message',"<center><b>Game Over</b></center> <br> Do You Want To Restart ?",QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.Yes)==QtGui.QMessageBox.Yes:
			self.randomInit()
		else:
			self.close()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	game = PyQtGame()
	app.exec_()


