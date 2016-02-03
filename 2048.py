#coding=utf-8
import sys
from PyQt4 import QtGui,QtCore
from random import randint

class Example(QtGui.QWidget):
    def __init__(self):
        super(Example,self).__init__()
        self.tiles = [[0]*4 for i in range(4)]
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
        for m in range(randint(2,3)):
            i = randint(0,3)
            j = randint(0,3)
            self.tiles[i][j] = 2
        self.color = [255,80,160]        
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,350,350)
        self.setWindowTitle("Draw Reac")
        self.show()

    def paintEvent(self,e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()
    
    def keyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_Up:
            self.Up()
        elif e.key() == QtCore.Qt.Key_Down:
            self.Down()
        elif e.key() == QtCore.Qt.Key_Left:
            self.Left()
        elif e.key() == QtCore.Qt.Key_Right:
            self.Right()

    def Left(self):
        print self.tiles
        # self.colToTop('j')
        isChanged = 1
        for i in range(4):
            firstNumLocation = -1
            firstZeroLocation = -1
            for j in range(4):
                if self.tiles[i][j]!=0:
                    if firstNumLocation==-1 and firstZeroLocation==-1:
                        firstNumLocation = j
                        firstNumValue = self.tiles[i][j]
                    elif firstNumLocation==-1 and firstZeroLocation!=-1:
                        firstNumLocation = firstZeroLocation
                        firstNumValue = self.tiles[i][j]
                        self.tiles[i][firstZeroLocation] = firstNumValue
                        self.tiles[i][j] =0
                        firstZeroLocation +=1                 
                    elif firstNumLocation!=-1 and firstZeroLocation!=-1:
                        if self.tiles[i][j] == firstNumValue:
                            firstNumValue*=2
                            isChanged = 1
                            self.tiles[i][firstNumLocation] = firstNumValue
                            self.tiles[i][j]=0
                            firstNumLocation = -1
                        else:
                            firstNumLocation+=1
                            firstNumValue = self.tiles[i][j]
                            self.tiles[i][firstNumLocation]=firstNumValue
                            self.tiles[i][j]=0                        
                            firstZeroLocation+=1
                    else:
                        if self.tiles[i][j] == firstNumValue:
                            firstNumValue*=2
                            isChanged = 1
                            self.tiles[i][firstNumLocation] = firstNumValue
                            self.tiles[i][j]=0
                            firstZeroLocation=firstNumLocation+1
                            firstNumLocation = -1
                        else:
                            firstNumLocation+=1
                            firstNumValue = self.tiles[i][j]  
                else:
                    if firstZeroLocation == -1:
                        firstZeroLocation = j      
        # self.color = [180,70,100]
        if isChanged:
            while 1:
                i = randint(0,3)
                j = randint(0,3)
                if self.tiles[i][j]==0:
                    print i,j
                    self.tiles[i][j]=2
                    break
                else:
                    pass
        self.update()
        print self.tiles

    def Up(self):
        print self.tiles
        # self.rowToTop('j')
        isChanged = 1
        for i in range(4):
            firstNumLocation = -1
            firstZeroLocation = -1
            for j in range(4):
                # exec 'bigEnd='+temp
                if self.tiles[j][i]!=0:
                    if firstNumLocation==-1 and firstZeroLocation==-1:
                        firstNumLocation = j
                        firstNumValue = self.tiles[j][i]
                    elif firstNumLocation==-1 and firstZeroLocation!=-1:
                        firstNumLocation = firstZeroLocation
                        firstNumValue = self.tiles[j][i]
                        self.tiles[firstZeroLocation][i] = firstNumValue
                        self.tiles[j][i] =0
                        # self.inOrDe(temp,firstZeroLocation)         
                        firstZeroLocation+=1
                    elif firstNumLocation!=-1 and firstZeroLocation!=-1:
                        if self.tiles[j][i] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            isChanged = 1
                            self.tiles[firstNumLocation][i] = firstNumValue
                            self.tiles[j][i]=0
                            firstNumLocation = -1
                        else:
                            # self.inOrDe(temp,firstNumLocation)
                            firstNumLocation+=1
                            firstNumValue = self.tiles[j][i]
                            self.tiles[firstNumLocation][i]=firstNumValue
                            self.tiles[j][i]=0                        
                            # self.inOrDe(temp,firstZeroLocation)
                            firstZeroLocation+=1
                    else:
                        if self.tiles[j][i] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            isChanged = 1
                            self.tiles[firstNumLocation][i] = firstNumValue
                            self.tiles[j][i]=0
                            firstNumLocation = -1
                            if self.isj(temp):
                                firstZeroLocation=firstNumLocation-1
                            else:
                                firstZeroLocation=firstNumLocation+1
                        else:
                            self.inOrDe(temp,firstNumLocation)
                            firstNumValue = self.tiles[j][i] 
                else:
                    if firstZeroLocation == -1:
                        firstZeroLocation = j                       
        # self.color = [0,34,189]
        if isChanged:
            while 1:
                i = randint(0,3)
                j = randint(0,3)
                if self.tiles[i][j]==0:
                    print i,j
                    self.tiles[i][j]=2
                    break
                else:
                    pass    
        self.update()
        print self.tiles

    def Down(self):
        print self.tiles
        # self.rowToTop('3-j')
        temp = '3-j'
        isChanged = 1
        for i in range(4):
            firstNumLocation = -1
            firstZeroLocation = -1
            for j in range(4):
                # exec 'bigEnd='+temp
                if self.tiles[3-j][i]!=0:
                    if firstNumLocation==-1 and firstZeroLocation==-1:
                        firstNumLocation = 3-j
                        firstNumValue = self.tiles[3-j][i]
                    elif firstNumLocation==-1 and firstZeroLocation!=-1:
                        firstNumLocation = firstZeroLocation
                        firstNumValue = self.tiles[3-j][i]
                        self.tiles[firstZeroLocation][i] = firstNumValue
                        self.tiles[3-j][i] =0
                        self.inOrDe(temp,firstZeroLocation)         
                    elif firstNumLocation!=-1 and firstZeroLocation!=-1:
                        if self.tiles[3-j][i] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            isChanged = 1
                            self.tiles[firstNumLocation][i] = firstNumValue
                            self.tiles[3-j][i]=0
                            firstNumLocation = -1
                        else:
                            # self.inOrDe(temp,firstNumLocation)
                            firstNumLocation-=1
                            firstNumValue = self.tiles[3-j][i]
                            self.tiles[firstNumLocation][i]=firstNumValue
                            self.tiles[3-j][i]=0                        
                            # self.inOrDe(temp,firstZeroLocation)
                            firstZeroLocation-=1
                    else:
                        if self.tiles[3-j][i] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            isChanged = 1
                            print firstNumValue
                            self.tiles[firstNumLocation][i] = firstNumValue
                            self.tiles[3-j][i]=0
                            if self.isBigEnd(temp):
                                firstZeroLocation=firstNumLocation-1
                            else:
                                firstZeroLocation=firstNumLocation+1
                            firstNumLocation = -1  
                        else:
                            # self.inOrDe(temp,firstNumLocation)
                            firstNumLocation = firstNumLocation-1
                            firstNumValue = self.tiles[3-j][i] 
                else:
                    if firstZeroLocation == -1:
                        firstZeroLocation = 3-j               
        # self.color = [100,200,150]
        if isChanged:
            while 1:
                i = randint(0,3)
                j = randint(0,3)
                if self.tiles[i][j]==0:
                    print i,j
                    self.tiles[i][j]=2
                    break
                else:
                    pass   
        self.update()
        print self.tiles

    def isBigEnd(self,temp):
            return 1 if temp=='3-j' else 0

    def inOrDe(self,temp,item):
        if self.isBigEnd(temp):
            item -=1                 
        else:   
            item +=1      

    def isChanged(self,temp):
        pass

    def rowToTop(self,temp):
        for i in range(4):
            firstNumLocation = -1
            firstZeroLocation = -1
            for j in range(4):
                exec 'bigEnd='+temp
                if self.tiles[bigEnd][i]!=0:
                    if firstNumLocation==-1 and firstZeroLocation==-1:
                        firstNumLocation = bigEnd
                        firstNumValue = self.tiles[bigEnd][i]
                    elif firstNumLocation==-1 and firstZeroLocation!=-1:
                        firstNumLocation = firstZeroLocation
                        firstNumValue = self.tiles[bigEnd][i]
                        self.tiles[firstZeroLocation][i] = firstNumValue
                        self.tiles[bigEnd][i] =0
                        self.inOrDe(temp,firstZeroLocation)         
                    elif firstNumLocation!=-1 and firstZeroLocation!=-1:
                        if self.tiles[bigEnd][i] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            self.tiles[firstNumLocation][i] = firstNumValue
                            self.tiles[bigEnd][i]=0
                        else:
                            self.inOrDe(temp,firstNumLocation)
                            firstNumValue = self.tiles[bigEnd][i]
                            self.tiles[firstNumLocation][i]=firstNumValue
                            self.tiles[bigEnd][i]=0                        
                            self.inOrDe(temp,firstZeroLocation)
                    else:
                        if self.tiles[bigEnd][i] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            self.tiles[firstNumLocation][i] = firstNumValue
                            self.tiles[bigEnd][i]=0
                            if self.isBigEnd(temp):
                                firstZeroLocation=firstNumLocation-1
                            else:
                                firstZeroLocation=firstNumLocation+1
                        else:
                            self.inOrDe(temp,firstNumLocation)
                            firstNumValue = self.tiles[bigEnd][i] 
                else:
                    if firstZeroLocation == -1:
                        firstZeroLocation = bigEnd       

    def colToTop(self,temp):
        for i in range(4):
            firstNumLocation = -1
            firstZeroLocation = -1
            for j in range(4):
                exec 'bigEnd='+temp
                if self.tiles[i][bigEnd]!=0:
                    if firstNumLocation==-1 and firstZeroLocation==-1:
                        firstNumLocation = bigEnd
                        firstNumValue = self.tiles[i][bigEnd]
                    elif firstNumLocation==-1 and firstZeroLocation!=-1:
                        firstNumLocation = firstZeroLocation
                        firstNumValue = self.tiles[i][bigEnd]
                        self.tiles[i][firstZeroLocation] = firstNumValue
                        self.tiles[i][bigEnd] =0
                        self.inOrDe(temp,firstZeroLocation)         
                    elif firstNumLocation!=-1 and firstZeroLocation!=-1:
                        if self.tiles[i][bigEnd] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            self.tiles[i][firstNumLocation] = firstNumValue
                            self.tiles[i][bigEnd]=0
                        else:
                            self.inOrDe(temp,firstNumLocation)
                            firstNumValue = self.tiles[i][bigEnd]
                            self.tiles[i][firstNumLocation]=firstNumValue
                            self.tiles[i][bigEnd]=0                        
                            self.inOrDe(temp,firstZeroLocation)
                    else:
                        if self.tiles[i][bigEnd] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            self.tiles[i][firstNumLocation] = firstNumValue
                            self.tiles[i][bigEnd]=0
                            if self.isBigEnd(temp):
                                firstZeroLocation=firstNumLocation-1
                            else:
                                firstZeroLocation=firstNumLocation+1
                        else:
                            self.inOrDe(temp,firstNumLocation)
                            firstNumValue = self.tiles[i][bigEnd] 
                else:
                    if firstZeroLocation == -1:
                        firstZeroLocation = bigEnd       

    def Right(self):
        print self.tiles
        # self.colToTop('3-j')
        isChanged = 1
        for i in range(4):
            firstNumLocation = -1
            firstZeroLocation = -1
            for j in range(4):
                if self.tiles[i][3-j]!=0:
                    if firstNumLocation==-1 and firstZeroLocation==-1:
                        firstNumLocation = 3-j
                        firstNumValue = self.tiles[i][3-j]
                    elif firstNumLocation==-1 and firstZeroLocation!=-1:
                        firstNumLocation = firstZeroLocation
                        firstNumValue = self.tiles[i][3-j]
                        self.tiles[i][firstZeroLocation] = firstNumValue
                        self.tiles[i][3-j] =0
                        firstZeroLocation -=1                 
                    elif firstNumLocation!=-1 and firstZeroLocation!=-1:
                        if self.tiles[i][3-j] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            isChanged = 1
                            self.tiles[i][firstNumLocation] = firstNumValue
                            self.tiles[i][3-j]=0
                            firstNumLocation = -1
                        else:
                            firstNumLocation-=1
                            firstNumValue = self.tiles[i][3-j]
                            self.tiles[i][firstNumLocation]=firstNumValue
                            self.tiles[i][3-j]=0                        
                            firstZeroLocation-=1
                    else:
                        if self.tiles[i][3-j] == firstNumValue:
                            firstNumValue=firstNumValue*2
                            isChanged = 1
                            self.tiles[i][firstNumLocation] = firstNumValue
                            self.tiles[i][3-j]=0
                            firstZeroLocation=firstNumLocation-1
                            firstNumLocation = -1
                        else:
                            firstNumLocation-=1
                            firstNumValue = self.tiles[i][3-j]
                else:
                    if firstZeroLocation == -1:
                        firstZeroLocation = 3-j
        # self.color = [249,189,120]
        if isChanged:
            while 1:
                i = randint(0,3)
                j = randint(0,3)
                if self.tiles[i][j]==0:
                    print i,j
                    self.tiles[i][j]=2
                    break
                else:
                    pass       
        self.update()
        print self.tiles

    def PaintRect(self,e):
        qp = QtGui.QPainter()
        qp.begin(self)
        color = QtGui.QColor(10,40,60,100)
        qp.setPen(color)
        qp.setBrush(QtGui.QColor(14,145,218,160))
        qp.drawRect(20,20,100,100)
        qp.end()


    def drawRectangles(self,qp):
        color = QtGui.QColor(10,40,70)
        color.setNamedColor("#d4d4d4")
        qp.setPen(color)

        for i in range(4):
            for j in range(4):
                # qp.setPen(QtGui.QPen(QtGui.QColor(0x776e65)))
                qp.setFont(QtGui.QFont('Arial',20))
                if self.tiles[i][j] != 0:
                    qp.setBrush(self.colors[self.tiles[i][j]])
                    qp.drawRoundedRect(QtCore.QRect(20+j*80,20+i*80,60,60),10,10)
                    color = QtGui.QColor(255,255,255)
                    qp.setPen(color)
                    qp.drawText(QtCore.QRectF(QtCore.QRect(20+j*80,20+i*80,60,60)),str(self.tiles[i][j]),QtGui.QTextOption(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter))
                else:
                    qp.setBrush(self.colors[self.tiles[i][j]])
                    qp.drawRoundedRect(QtCore.QRect(20+j*80,20+i*80,60,60),10,10)
        qp.setBrush(QtGui.QColor(25,0,90,20))
        qp.drawRect(10,10,330,330)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
