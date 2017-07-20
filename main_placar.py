import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
from time import sleep
Home=''
Guest=''
teamHome={}
teamGuest={}
scoreHome=0
scoreGuest=0
gols=[]
last=''
time='00:00:00'

tickAUX = 0
untime = 10 # 10 ms = 1 cs

class endGame(QDialog):
	def __init__ (self,parent=None):
		super(endGame,self).__init__(parent)
		uic.loadUi('tela5.ui',self)
		self.endgame.clicked.connect(self.close)
		self.restartgame.clicked.connect(self.newgame)
		self.teamhome.setText(Home + ' ' + str(scoreHome))
		self.teamguest.setText(Guest + ' ' + str(scoreGuest))

		for x in gols:
			a = x.split('-')
			if a[0]==Home:
				self.golshome.addItem('%s -> %s'%(a[1],a[3]))
			else:
				self.golsguest.addItem('%s -> %s'%(a[1],a[3]))
	
	def close(self):
		sys.exit()


	def newgame(self):
		global Home, Guest, teamHome, teamGuest,scoreHome,scoreGuest,gols,last,time,tickAUX
		Home=''
		Guest=''
		teamHome={}
		teamGuest={}
		scoreHome=0
		scoreGuest=0
		gols=[]
		last=''
		time='00:00:00'
		tickAUX = 0
		self.hide()
		n=Cadastro()
		n.activateWindow()
		n.exec_()

class Gol(QDialog):
	def __init__(self,parent=None):
		super(Gol,self).__init__(parent)
		uic.loadUi('tela4.ui',self)
		self.namehome.setText(Home)
		self.nameguest.setText(Guest)
		self.namehome.clicked.connect(self.addgolHome)
		self.nameguest.clicked.connect(self.addgolGuest)

	def addgolHome(self):
		global scoreHome, last, gols		
		
		if self.numero.text() in teamHome:
			last=self.namehome.text()
			scoreHome+=1
			gols.append(self.namehome.text()+'-'+teamHome[self.numero.text()]+'-'+str(scoreHome)+'-'+time)
			Cadastro.display(self)
		else:
			self.message.setText('Jogador não cadastrado')

	def addgolGuest(self):
		global scoreGuest, last, gols

		if self.numero.text() in teamGuest:
			last=self.nameguest.text()
			scoreGuest+=1
			gols.append(self.nameguest.text()+'-'+teamGuest[self.numero.text()]+'-'+str(scoreGuest)+'-'+time)
			Cadastro.display(self)
		else:
			self.message.setText('Jogador não cadastrado')



class Display (QDialog):
	def __init__(self,parent=None):
		super(Display,self).__init__(parent)
		uic.loadUi('tela3.ui',self)
		self.tick = tickAUX
		self.timer = QTimer()
		self.labeltime.setText(time)
		self.scorehome.setText(str(scoreHome))
		self.scoreguest.setText(str(scoreGuest))
		self.home.setText(Home)
		self.guest.setText(Guest)
		self.timer.timeout.connect(self.setTime)
		self.btnstart.clicked.connect(self.start)
		self.btnrestart.clicked.connect(self.reset)
		self.btngol.clicked.connect(self.showGol)
		self.btnerro.clicked.connect(self.dellast)
		self.endgame.clicked.connect(self.end)
		if last!='':
			a=gols[-1].split('-')
			self.message.setText('Gol do(a) ' +a[0]+' -> '+a[1])
			sleep (5)
			self.message.setText('')

	def end(self):
		e=endGame()
		e.activateWindow()
		self.hide()
		e.exec_()

	def dellast(self):
		global scoreHome, scoreGuest, gols

		if last==Home:
			scoreHome-=1
			self.scorehome.setText(str(scoreHome))
		else:
			scoreGuest-=1
			self.scoreguest.setText(str(scoreGuest))
		gols.pop()
	
	def start(self):
		if not self.isTimerActive():
			self.timer.start(untime)
			self.btnstart.setText("Stop")
		else:
			self.timer.stop()
			self.btnstart.setText("Start")

	def reset(self):
		self.timer.stop()
		self.tick = 0
		time = "00:00:00"
		self.labeltime.setText(time)

	def isTimerActive(self):
		return self.timer.isActive()

	def setTime(self):
		self.tick += 1
		minutes = self.tick / 3600
		seconds = (self.tick % 3600) / 100 % 60
		decimals = (self.tick) % 100
		self.labeltime.setText("%02d:%02d:%02d" % (minutes, seconds,decimals))

	def showGol(self):
		global time, tickAUX
		if self.isTimerActive():
			self.timer.stop()
			tickAUX = self.tick
			time=self.labeltime.text()
			b=Gol(self)
			b.activateWindow()
			self.hide()
			b.exec_()

class Cadastro(QDialog):
	def __init__(self,parent=None):
		super(Cadastro, self).__init__(parent)
		uic.loadUi('tela2.ui',self)
		self.btnaddteam.clicked.connect(self.addTeam)
	
	def addTeam(self):
		global Home, teamHome, Guest, teamGuest
		
		if Home=='':
			self.btnaddteam.setText('Cadastrar Time 1')
			Home = self.ateamname.text()
			teamHome={}
			teamHome[self.number1.text()]=self.name1.text()
			teamHome[self.number2.text()]=self.name2.text()
			teamHome[self.number3.text()]=self.name3.text()
			teamHome[self.number4.text()]=self.name4.text()
			teamHome[self.number5.text()]=self.name5.text()
			teamHome[self.number6.text()]=self.name6.text()
			teamHome[self.number7.text()]=self.name7.text()
			teamHome[self.number8.text()]=self.name8.text()
			teamHome[self.number9.text()]=self.name9.text()
			teamHome[self.number10.text()]=self.name10.text()
			del teamHome['']
			Main.addTeam(self)
		else:
			self.btnaddteam.setText('Cadastrar Time 2')
			Guest = self.ateamname.text()
			teamGuest={}
			teamGuest[self.number1.text()]=self.name1.text()
			teamGuest[self.number2.text()]=self.name2.text()
			teamGuest[self.number3.text()]=self.name3.text()
			teamGuest[self.number4.text()]=self.name4.text()
			teamGuest[self.number5.text()]=self.name5.text()
			teamGuest[self.number6.text()]=self.name6.text()
			teamGuest[self.number7.text()]=self.name7.text()
			teamGuest[self.number8.text()]=self.name8.text()
			teamGuest[self.number9.text()]=self.name9.text()
			teamGuest[self.number10.text()]=self.name10.text()
			del teamGuest['']
			self.display()

	def display(self):
		a=Display()
		a.activateWindow()
		self.hide()
		a.exec_()

		
		
class Main(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		uic.loadUi('tela1.ui',self)
		self.addteam.clicked.connect(self.addTeam)

	def addTeam(self):
		t=Cadastro(self)
		t.activateWindow()
		self.hide()
		t.exec_()

if __name__ == '__main__':
    root = QApplication(sys.argv)
    app = Main()
    app.show()
    root.exec_() 