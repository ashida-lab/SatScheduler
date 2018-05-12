import numpy as np
from scipy.linalg import expm3,norm
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import pickle

import math

def rot3d(axis,theta):
  return expm3(np.cross(np.eye(3),axis/norm(axis)*theta))
    
def xyz2lla(xyz):
  lla=np.array([np.arcsin(xyz[2]/norm(xyz)),np.arctan2(xyz[0],xyz[1]),norm(xyz)])
    
  return lla
  
def lla2xyz(lla):
  xyz=np.array([lla[2]*np.cos(lla[0])*np.cos(lla[1]),lla[2]*np.cos(lla[0])*np.sin(lla[1]),lla[2]*np.sin(lla[1])])
    
  return xyz

def makeOrbit(Re,H,re_period,path_num,I):

  omega=2*math.pi*path_num/(re_period*24*3600.0)
  
  Omega=2*math.pi/(24*3600.0)
  x=[]
  y=[]
 
  spots = []
  
  axis0=np.array([0,1,0])
  M0=rot3d(axis0,np.array([I*math.pi/180.0]))
  
  for cnt in range(re_period*24*3600):
    t=np.array([cnt])

    pos=np.array([(Re+H)*np.cos(omega*t),(Re+H)*np.sin(omega*t),0])

    pos2=np.dot(M0,pos)
  
    axis1=np.array([0,0,1])
    phases = np.angle(np.exp(1j*(Omega*t+math.pi)))

    M1=rot3d(axis1,phases)

    pos3=np.dot(M1,pos2)
    
    lla=xyz2lla(pos3)
    
    x=180.0/math.pi*lla[1]
    y=180.0/math.pi*lla[0]
    spots.append({'time': t, 'pos': (x,y)})
  
  with open('sat2.dat', 'wb') as fp:
    pickle.dump(spots, fp)


Re=6000 #km
H=500 #km
re_period=8 #day
path_num=111
I=105 #degree

makeOrbit(Re,H,re_period,path_num,I)

with open ('sat2.dat', 'rb') as fp:
  itemlist = pickle.load(fp)
  
cnt=[1,10,100]  
  
print(itemlist[10]['pos'])