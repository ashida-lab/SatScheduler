import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import qdarkstyle

from test import Ui_Dialog

import pickle

import cv2
import numpy as np
from scipy.linalg import expm3,norm
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore,QtGui

import math

from numba import double
from numba.decorators import jit

class ImageDialog(QDialog):
  def __init__(self):
    super(ImageDialog,self).__init__()
    
    self.ui=Ui_Dialog()
    self.ui.setupUi(self)
    
    self.map()
    
    self.ui.hourSpinBox.valueChanged.connect(self.timeSpinChange)
    self.ui.minuteSpinBox.valueChanged.connect(self.timeSpinChange)
    self.ui.secondSpinBox.valueChanged.connect(self.timeSpinChange)
    
    self.ui.latSpinBox.valueChanged.connect(self.latSpinChange)
    self.ui.lonSpinBox.valueChanged.connect(self.lonSpinChange)
    
    self.ui.timeSlider.valueChanged.connect(self.timeSliderChange)
    
    self.ui.calendarWidget.selectionChanged.connect(self.dateChange)
    
    self.ui.sat1cb.stateChanged.connect(self.satSelect)
    self.ui.sat2cb.stateChanged.connect(self.satSelect)
    self.ui.sat3cb.stateChanged.connect(self.satSelect)
    self.ui.sat4cb.stateChanged.connect(self.satSelect)
    
    self.re_period=8 #day
    
    self.loadOrbit()
    
    self.sp1=[]
    self.sp2=[]
    self.sp3=[]
    self.sp4=[]
    self.plotOrbit()
    
    self.sp5=[]
    self.sp6=[]
    self.sp7=[]
    self.sp8=[]
    self.items=[]
    self.plotSat()
    
    self.plotTask()
    
  def map(self):
    cvImg=cv2.imread('C:\\Users\\ashiy\\Pictures\\land_ocean_ice_8192.png')
    cvImg=cv2.cvtColor(cvImg,cv2.COLOR_BGR2RGB)
    
    cvImg=cv2.flip(cv2.transpose(cvImg),1)
    
    img=pg.ImageItem(cvImg)
    self.ui.mapView.addItem(img)
    img.setZValue(-100)
    img.setRect(QRectF(-180,-90,360,180))
    
    self.inf1 = pg.InfiniteLine(movable=True, angle=90,pen=(200, 0, 0), bounds = [-180, 180], hoverPen=(0,200,0),label='lon={value:0.1f}deg', 
                       labelOpts={'position':0.1, 'color': (200,200,100), 'fill': (200,200,200,50), 'movable': True})
    self.inf1.sigPositionChangeFinished.connect(self.lonChange)
    
    self.inf2 = pg.InfiniteLine(movable=True, angle=0, pen=(0, 0, 200), bounds = [-90, 90], hoverPen=(0,200,0), label='lat={value:0.1f}deg', 
                       labelOpts={'position':0.1, 'color': (200,200,100), 'fill': (200,200,200,50), 'movable': True})
    self.inf2.sigPositionChangeFinished.connect(self.latChange)
    
    self.ui.mapView.addItem(self.inf1)
    self.ui.mapView.addItem(self.inf2)
    
  def lonChange(self):
    self.ui.lonSpinBox.setValue(self.inf1.value())
    
  def latChange(self):
    self.ui.latSpinBox.setValue(self.inf2.value())
    
  def latSpinChange(self):
    self.inf2.setValue(self.ui.latSpinBox.value())
    
  def lonSpinChange(self):
    self.inf1.setValue(self.ui.lonSpinBox.value())
    
  def timeSpinChange(self):
    if self.ui.secondSpinBox.value()==60:
      self.ui.secondSpinBox.setValue(0)
      self.ui.minuteSpinBox.setValue(self.ui.minuteSpinBox.value()+1)
    
    if self.ui.minuteSpinBox.value()==60:
      self.ui.minuteSpinBox.setValue(0)
      self.ui.hourSpinBox.setValue(self.ui.hourSpinBox.value()+1)
    
    if self.ui.hourSpinBox.value()==24:
      self.ui.hourSpinBox.setValue(0)
      
    if self.ui.secondSpinBox.value()==-1:
      self.ui.secondSpinBox.setValue(59)
      self.ui.minuteSpinBox.setValue(self.ui.minuteSpinBox.value()-1)
      
    if self.ui.minuteSpinBox.value()==-1:
      self.ui.minuteSpinBox.setValue(59)
      self.ui.hourSpinBox.setValue(self.ui.hourSpinBox.value()-1)
      
    if self.ui.hourSpinBox.value()==-1:
      self.ui.hourSpinBox.setValue(23)
      
      
    self.total_second=self.ui.hourSpinBox.value()*3600+self.ui.minuteSpinBox.value()*60+self.ui.secondSpinBox.value()
    self.ui.timeSlider.setValue(self.total_second)
    
  def timeSliderChange(self):
    self.total_second=self.ui.timeSlider.value()
    hh=self.total_second//3600
    mm=(self.total_second-hh*3600)//60
    ss=self.total_second-hh*3600-mm*60
    
    self.ui.hourSpinBox.setValue(hh)
    self.ui.minuteSpinBox.setValue(mm)
    self.ui.secondSpinBox.setValue(ss)
    
    self.inf3.setValue(self.total_second/3600)
    
    self.plotSat()
    
  def dateChange(self):
    date=self.ui.calendarWidget.selectedDate()
    print(date.toJulianDay())
    
    self.plotSat()
    self.plotOrbit()
    
  def _create_time(self,timetxt):
    hour,minute,second=timetxt.split(':')
    time=int(hour)*3600+int(minute)*60+int(second)
    
    return time/3600.0
    
  def plotTask(self):
    ylabels0=['sat1','sat2','sat3','sat4']
    ylabels=[]
    modes=[]
    times=[]
    
    fname=r'task.csv'
    textlist=open(fname).readlines()
    
    for tx in textlist:
      if not tx.startswith('#'):
        ylabel,mode,starttime,endtime=tx.split(',')
        ylabels.append(ylabel.replace('\n',''))
        modes.append(int(mode.replace('\n','')))
        times.append([self._create_time(starttime.replace('\n','')),self._create_time(endtime.replace('\n',''))])
        
    tasks={}
    for i,task in enumerate(ylabels0):
      tasks[task]=i
    
    ydict=dict(enumerate(ylabels0))
    ax1=pg.AxisItem(orientation='left')
    ax1.setTicks([ydict.items()])
    ax1.setGrid(255)
    
    ax2=pg.AxisItem(orientation='bottom')
    ax2.setGrid(255)
    
    plot=self.ui.taskView.addPlot(axisItems={'bottom':ax2,'left':ax1})
    
    for i in range(len(ylabels)):
      start_time,end_time=times[i]
      x=(start_time+end_time)/2.0
      y=tasks[ylabels[i]]
      width=end_time-start_time
      color='rgbcmy'[modes[i]]
      
      bg=BarGraph(x=[x],y=[y],width=[width],height=0.8,brush=color)
      plot.addItem(bg)
    
    self.inf3 = pg.InfiniteLine(movable=True, angle=90,pen=(200, 0, 200), bounds = [0, 24], hoverPen=(0,200,0),label='time={value:0.2f}', 
                       labelOpts={'position':0.1, 'color': (200,200,100), 'fill': (200,200,200,50), 'movable': True})
    self.inf3.sigPositionChangeFinished.connect(self.timeChange)
    plot.addItem(self.inf3)
    
  def timeChange(self):
    self.ui.timeSlider.setValue(self.inf3.value()*3600)
  
  def loadOrbit(self):
    self.orbitlist=[]
    with open ('sat1.dat', 'rb') as fp:
      tmp = pickle.load(fp)
      self.orbitlist.append(tmp)

    with open ('sat2.dat', 'rb') as fp:
      tmp = pickle.load(fp)
      self.orbitlist.append(tmp)
      
  def satSelect(self):
    self.plotOrbit()
    self.plotSat()

  def plotOrbit(self):
    self.ui.mapView.removeItem(self.sp1)
    
    self.sp1 = pg.ScatterPlotItem(pxMode=False)   ## Set pxMode=False to allow spots to transform with the view

    self.ui.mapView.removeItem(self.sp2)
    
    self.sp2 = pg.ScatterPlotItem(pxMode=False)   ## Set pxMode=False to allow spots to transform with the view
    
    self.ui.mapView.removeItem(self.sp3)
    
    self.sp3 = pg.ScatterPlotItem(pxMode=False)   ## Set pxMode=False to allow spots to transform with the view

    self.ui.mapView.removeItem(self.sp4)
    
    self.sp4 = pg.ScatterPlotItem(pxMode=False)   ## Set pxMode=False to allow spots to transform with the view

    date=self.ui.calendarWidget.selectedDate()
    date_time=((date.toJulianDay()-2451545)%self.re_period)*24*3600.0
    
    print(date_time)
    
    if self.ui.sat1cb.checkState() == QtCore.Qt.Checked:
      spots = []
      for cnt in range(24*36*4):
        t=int(date_time+cnt*25)

        spots.append({'pos': self.orbitlist[0][t]['pos'], 'size': 0.5, 'pen': {'color': 'c', 'width': 1}})
      
      self.sp1.addPoints(spots)
      self.ui.mapView.addItem(self.sp1)
    
    if self.ui.sat2cb.checkState() == QtCore.Qt.Checked:
      spots = []
      for cnt in range(24*36*4):
        t2=int(date_time+cnt*25+24*3600*4)%(24*3600*8)

        spots.append({'pos': self.orbitlist[0][t2]['pos'], 'size': 0.5, 'pen': {'color': 'c', 'width': 1}})
      
      self.sp2.addPoints(spots)
      self.ui.mapView.addItem(self.sp2)
    
    if self.ui.sat3cb.checkState() == QtCore.Qt.Checked:
      spots = []
      for cnt in range(24*36*4):
        t=int(date_time+cnt*25)

        spots.append({'pos': self.orbitlist[1][t]['pos'], 'size': 0.5, 'pen': {'color': 'y', 'width': 1}})
      
      self.sp3.addPoints(spots)
      self.ui.mapView.addItem(self.sp3)
    
    if self.ui.sat4cb.checkState() == QtCore.Qt.Checked:
      spots = []
      for cnt in range(24*36*4):
        t2=int(date_time+cnt*25+24*3600*4)%(24*3600*8)

        spots.append({'pos': self.orbitlist[1][t2]['pos'], 'size': 0.5, 'pen': {'color': 'y', 'width': 1}})
      
      self.sp4.addPoints(spots)
      self.ui.mapView.addItem(self.sp4)

  def plotSat(self):
    self.ui.mapView.removeItem(self.sp5)
    
    self.sp5 = pg.ScatterPlotItem(pxMode=False,brush=pg.mkBrush(200, 0, 200, 50))   ## Set pxMode=False to allow spots to transform with the view

    self.ui.mapView.removeItem(self.sp6)
    
    self.sp6 = pg.ScatterPlotItem(pxMode=False,brush=pg.mkBrush(200, 0, 200, 50))   ## Set pxMode=False to allow spots to transform with the view
    
    self.ui.mapView.removeItem(self.sp7)
    
    self.sp7 = pg.ScatterPlotItem(pxMode=False,brush=pg.mkBrush(200, 0, 200, 50))   ## Set pxMode=False to allow spots to transform with the view

    self.ui.mapView.removeItem(self.sp8)
    
    self.sp8 = pg.ScatterPlotItem(pxMode=False,brush=pg.mkBrush(200, 0, 200, 50))   ## Set pxMode=False to allow spots to transform with the view

    for item in self.items:
      self.ui.mapView.removeItem(item)

    date=self.ui.calendarWidget.selectedDate()
    t=int(((date.toJulianDay()-2451545)%self.re_period)*24*3600.0+self.ui.timeSlider.value())
    t2=int(((date.toJulianDay()-2451545)%self.re_period)*24*3600.0+self.ui.timeSlider.value()+24*60*60*4)%(24*3600*8)
    
    if self.ui.sat1cb.checkState() == QtCore.Qt.Checked:
      spots = []
      spots.append({'pos': self.orbitlist[0][t]['pos'], 'size': 3.0, 'pen': {'color': 'm', 'width': 2}})
      
      self.sp5.addPoints(spots)
      self.ui.mapView.addItem(self.sp5)
      
      self.obsArea(self.orbitlist[0][t]['pos'][1]*math.pi/180,self.orbitlist[0][t]['pos'][0]*math.pi/180)
    
    if self.ui.sat2cb.checkState() == QtCore.Qt.Checked:
      spots = []
      spots.append({'pos': self.orbitlist[0][t2]['pos'], 'size': 3.0, 'pen': {'color': 'm', 'width': 2}})
      
      self.sp6.addPoints(spots)
      self.ui.mapView.addItem(self.sp6)
      
      self.obsArea(self.orbitlist[0][t2]['pos'][1]*math.pi/180,self.orbitlist[0][t2]['pos'][0]*math.pi/180)
    
    if self.ui.sat3cb.checkState() == QtCore.Qt.Checked:
      spots = []
      spots.append({'pos': self.orbitlist[1][t]['pos'], 'size': 3.0, 'pen': {'color': 'm', 'width': 2}})
      
      self.sp7.addPoints(spots)
      self.ui.mapView.addItem(self.sp7)
      
      self.obsArea(self.orbitlist[1][t]['pos'][1]*math.pi/180,self.orbitlist[1][t]['pos'][0]*math.pi/180)
      
    if self.ui.sat4cb.checkState() == QtCore.Qt.Checked:
      spots = []
      spots.append({'pos': self.orbitlist[1][t2]['pos'], 'size': 3.0, 'pen': {'color': 'm', 'width': 2}})
      
      self.sp8.addPoints(spots)
      self.ui.mapView.addItem(self.sp8)
      
      self.obsArea(self.orbitlist[1][t2]['pos'][1]*math.pi/180,self.orbitlist[1][t2]['pos'][0]*math.pi/180)
      
  def obsArea(self,lat,lon):
    angle=60.*math.pi/180.
    R=6000000.0
    h=500000.0
    a=1./np.tan(angle)
    b=R+h
    
    r=(-2*a*b+np.sqrt(4*a*a*b*b-4*(1+a*a)*(b*b-R*R)))/(2*(1+a*a))
    z=a*r+b
    
    data=[]
    x_prev=0
    y_prev=0
    
    for cnt in range(180):
      pos1=[r*np.cos(2*math.pi/180.*cnt),r*np.sin(2*math.pi/180.*cnt),z]
      
      axis1=np.array([1,0,0])
      M1=self.rot3d(axis1,lat-math.pi/2)
      axis2=np.array([0,0,1])
      M2=self.rot3d(axis2,-lon)
      
      pos2=np.dot(M1,pos1)
      pos3=np.dot(M2,pos2)
      
      lla=self.xyz2lla(pos3)
      
      x=180.0/math.pi*lla[1]
      y=180.0/math.pi*lla[0]
      
      if x*x_prev<0 or y*y_prev<0:
        item=customPolyItem(data)
        self.ui.mapView.addItem(item)
        self.items.append(item)
        
        data=[]
        
      data.append((x,y))
      x_prev=x
      y_prev=y
      
    item=customPolyItem(data)
    self.ui.mapView.addItem(item)
    self.items.append(item)
    
  def rot3d(self,axis,theta):
    return expm3(np.cross(np.eye(3),axis/norm(axis)*theta))
    
  def xyz2lla(self,xyz):
    lla=np.array([np.arcsin(xyz[2]/norm(xyz)),np.arctan2(xyz[0],xyz[1]),norm(xyz)])
    
    return lla
  
  def lla2xyz(self,lla):
    xyz=np.array([lla[2]*np.cos(lla[0])*np.cos(lla[1]),lla[2]*np.cos(lla[0])*np.sin(lla[1]),lla[2]*np.sin(lla[1])])
    
    return xyz
    
class BarGraph(pg.BarGraphItem):
  def mouseDragEvent(self,ev):
    if ev.button()!=QtCore.Qt.LeftButton:
      ev.ignore()
      return
      
    self.opts['x']=ev.pos().x()
    self.opts.update(self.opts)
    self.drawPicture()
    
    ev.accept()
    
class customPolyItem(pg.GraphicsObject):
  def __init__(self,data):
    pg.GraphicsObject.__init__(self)
    self.data=data
    self.points=[]
    self.generatePicture()
    
  def generatePicture(self):
    self.picture=QtGui.QPicture()
    p=QtGui.QPainter(self.picture)
    p.setPen(pg.mkPen('m',width=2))
    for item in self.data:
      point=QtCore.QPointF(item[0],item[1])
      self.points.append(point)
    p.drawPolyline(*self.points)
    p.end()
    
  def paint(self,p,*args):
    p.drawPicture(0,0,self.picture)
    
  def boundingRect(self):
    return QtCore.QRectF(self.picture.boundingRect())
  
if __name__=='__main__':
  app=QApplication(sys.argv)
  app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
  
  dialog=ImageDialog()
  
  dialog.show()
  sys.exit(app.exec_())
    