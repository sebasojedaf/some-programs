# -*- coding: utf-8 -*-
"""parcial1astro.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qFWcytOuMmJnWaOM6-KC5Q6fSzbEKxDB
"""

import astropy
import astropy.units as u
from astropy.time import Time
import math
import numpy as np
import matplotlib.pyplot as plt

#    COMETA HIPERBOLICO, abajo esta la solucion del elíptico, el hiperbolico tiene un problema.


G =  (14.88 * 10**-35)#*u.AU**3/(u.kg*u.d**2)
M = 1.99*10**30   #*u.kg
rt=6372
time=100
iteraciones=1000 # num.eq.
def raiz(e,l):
  x0=l
  iter1=x0-(x0-e*math.sin(x0)-l)/(1-e*math.cos(x0))
  xn=iter1
  for k in range(iteraciones):
    xn=xn-(xn-e*math.sin(xn)-l)/(1-e*math.cos(xn))
  return xn
def raizhiperbolica(e,l):
  x0=l
  iter1=x0-(e*np.sinh(x0)-l-x0)/(e*np.cosh(x0)-1)
  xn=iter1
  for k in range(iteraciones):
    xn=xn-(e*np.sinh(xn.value)-l-xn)/(e*np.cosh(xn.value)-1)
  return xn

def distancia(x,y,z,x2,y2,z2):
  d=np.sqrt((x-x2)**2 + (y-y2)**2 + (z-z2)**2)
  return d
def colision(x,y,z,x2,y2,z2):
  if distancia(x,y,z,x2,y2,z2)<=rt:
    return "hay colision"
  else:
    return "no hay colsion"

xc = [-136.5637561083746, -136.52944516728272, -136.49508281581126] #ua
yc = [-58.86174117642695, -58.8582744676107, -58.85478559561711]#ua
zc = [0.006477038631585696, 0.006476657161271048, 0.006476273252160792]#ua

t0 = Time('2023-07-09T00:00:00', format='isot', scale='utc')
tf = Time('2064-03-15T00:00:00', format='isot', scale='utc')
timevec=np.linspace(t0,tf,time)

t1=Time('2023-07-09T10:00:00', format='isot', scale='utc')
t2=Time('2023-07-09T12:00:00', format='isot', scale='utc')
t3=Time('2023-07-09T14:00:00', format='isot', scale='utc')
tc=[t1,t2,t3]
r1 = [xc[0], yc[0], zc[0]]
r2 = [xc[1], yc[1], zc[1]]
r3 = [xc[2], yc[2], zc[2]]

r1=np.array(r1)
r2=np.array(r2)       # AU
r3=np.array(r3)

v1 = (r2 - r1)/(tc[1]-tc[0])       # AU/DIA
v2 = (r3 - r2)/(tc[2]-tc[1])
l1 = (np.cross(r1,v1))
l2 = (np.cross(r2,v2))        # AU2/DIA
e1 = (np.cross(v1,l1) / (G*M))*u.day*u.day  - (r1 / np.linalg.norm(r1))
e2 = (np.cross(v2,l2) / (G*M))*u.day*u.day  - (r2 / np.linalg.norm(r2))

eprom=(e1+e2)/2.0
ecometa=(np.sqrt((e1[2]**2)+(e1[1]**2)+e1[0]**2) + np.linalg.norm(e2) )/2.0
lprom=(l1+l2)/2.0
p=((np.linalg.norm(lprom))**2)/(G*M)     #semilatus rectum
iota = np.arccos(lprom[2] / np.linalg.norm(lprom))#rad
acometa=p/(1-ecometa**2)#ua

Ωc=  np.arcsin((lprom[0] /(np.sin(iota)*np.linalg.norm(lprom))))#rad
ωc=np.arcsin((e1[2])/(ecometa*np.sin(iota))) #rad
aux=acometa*u.day**2
nc=np.sqrt(G*M)/(-aux)**(3/2)
phic1=np.arcsin((zc[0])/(np.linalg.norm(r1)*np.sin(iota)))
Ec1=np.arccosh((1-(np.linalg.norm(r1)/aux))/ecometa)
lc0=ecometa*np.sinh(Ec1)-Ec1.value

fig=plt.figure(figsize=(7,7))
axc = fig.add_subplot(111, projection='3d')
t0c=t1
print(ecometa,nc,acometa,Ωc,ωc,iota,lc0,t0c,ecometa)
for t in timevec:
  lc=lc0+nc*(t-t0c).value
  bc=raiz(ecometa,lc.value)
  Ec=bc*u.rad
  fc=2*np.arctan(np.sqrt((1+ecometa)/(ecometa-1))*np.tanh(Ec/2))
  phic=fc+ωc
  rc=acometa*(1-ecometa*np.cosh(Ec))
  xc=rc*(np.cos(Ωc)*np.cos(phic)-np.cos(iota)*np.sin(Ωc)*np.sin(phic))
  yc=rc*(np.sin(Ωc)*np.cos(phic)+np.cos(iota)*np.cos(Ωc)*np.sin(phic))
  zc=rc*np.sin(iota)*np.sin(phic)
  axc.scatter(xc,yc,zc)
axc.scatter(0,0,0)

a = (1.495582533630905/149597870) * 10**8 #km AU
e = 1.694863932474438 * 10**-2
Ω =(math.pi/180.0)* 1.498625963929686 * 10**2
ω = (math.pi/180.0)*3.146587763491455 * 10**2
ι = (math.pi/180.0)*4.164075603038432 * 10**-3
n = (math.pi/180.0)*86400*1.141204629731537 * 10**-5     #rad/dia
l0 =(math.pi/180.0)*1.817846947871890 * 10**2

fig=plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')

for t in timevec:
  l=l0+n*(t-t0)
  b=raiz(e,l.value)
  E=b
  f=2*np.arctan(math.sqrt((1+e)/(1-e))*np.tan(E/2))
  phi=f+ω
  r=a*(1-e*math.cos(E))
  x=r*(math.cos(Ω)*math.cos(phi)-math.cos(ι)*math.sin(Ω)*math.sin(phi))
  y=r*(math.sin(Ω)*math.cos(phi)+math.cos(ι)*math.cos(Ω)*math.sin(phi))
  z=r*math.sin(ι)*math.sin(phi)
  ax.scatter(x,y,z,c="blue")

ax.scatter(0,0,0)

import astropy.units as u
from astropy.time import Time
t0 = Time('2023-08-09T09:00:00', format='isot', scale='utc')
t1=  Time('2023-07-09T11:00:00', format='isot', scale='utc')
#t=t0+1*u.day
print(t1-t0)

#COMETA ELIPTICO
rtua=4.25942e-5# radio de la tierra en ua

xc1 = [0.7059032210909959, 0.7064970232872655, 0.7070906151926998] #ua
yc1 = [-1.769547135717722, -1.7682131326526134, -1.7668786032741868]#ua
zc1 = [0.0001947177390506007, 0.00019457094778662054, 0.0001944240986080829]#ua

t1=Time('2023-07-09T10:00:00', format='isot', scale='utc')
t2=Time('2023-07-09T12:00:00', format='isot', scale='utc')
t3=Time('2023-07-09T14:00:00', format='isot', scale='utc')
tf=Time('2033-07-09T10:00:00', format='isot', scale='utc')
time=100000
timevecc=np.linspace(t1,tf,time)
tc=[t1,t2,t3]
r1 = [xc1[0], yc1[0], zc1[0]]
r2 = [xc1[1], yc1[1], zc1[1]]
r3 = [xc1[2], yc1[2], zc1[2]]

r1=np.array(r1)
r2=np.array(r2)       # AU
r3=np.array(r3)

v1 = (r2 - r1)/(tc[1]-tc[0])       # AU/DIA
v2 = (r3 - r2)/(tc[2]-tc[1])
l1 = (np.cross(r1,v1))
l2 = (np.cross(r2,v2))        # AU2/DIA
e1 = (np.cross(v1,l1) / (G*M))*u.day*u.day  - (r1 / np.linalg.norm(r1))
e2 = (np.cross(v2,l2) / (G*M))*u.day*u.day  - (r2 / np.linalg.norm(r2))
ec=(np.sqrt((e1[2]**2)+(e1[1]**2)+e1[0]**2) + np.linalg.norm(e2) )/2.0

lprom=(l1+l2)/2.0
p=((np.linalg.norm(lprom))**2)/(G*M)     #semilatus rectum AU
iota = -np.arccos(lprom[2] / np.linalg.norm(lprom))#rad
acometa=p/(1-ec**2)#ua
Ωc=  np.arcsin((lprom[0] /(np.sin(iota)*np.linalg.norm(lprom))))
ωc=np.arcsin((e1[2])/(ec*np.sin(iota))) #rad
aux=acometa*u.day**2
nc=np.sqrt(G*M)/(aux)**(3/2)
phicom1=np.arcsin((zc1[0])/(np.linalg.norm(r1)*np.sin(iota)))
Ec1=-np.arccos((1-(np.linalg.norm(r1)/aux))/ec)
lc0=Ec1/u.rad -ec*np.sin(Ec1)

fig=plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')
t0c=t1
T=2*math.pi/nc
print(ec,nc,Ωc,ωc,iota,lc0,acometa,p)


for t in timevecc:
  lc=lc0+nc*(t-t1).value
  bc=raiz(ec,lc.value)
  Ec=bc*u.rad
  fc=2*np.arctan(math.sqrt((1+ec)/(1-ec))*np.tan(Ec/2))
  phic=fc+ωc
  rc=acometa*(1-ec*np.cos(Ec))
  xc=rc*(np.cos(Ωc)*np.cos(phic)-np.cos(iota)*np.sin(Ωc)*np.sin(phic))
  yc=rc*(np.sin(Ωc)*np.cos(phic)+np.cos(iota)*np.cos(Ωc)*np.sin(phic))
  zc=rc*np.sin(iota)*np.sin(phic)
  ax.scatter(xc,yc,zc,c="red")
  l=l0+n*(t-t0)
  b=raiz(e,l.value)
  E=b
  f=2*np.arctan(math.sqrt((1+e)/(1-e))*np.tan(E/2))
  phi=f+ω
  r=a*(1-e*math.cos(E))
  x=r*(math.cos(Ω)*math.cos(phi)-math.cos(ι)*math.sin(Ω)*math.sin(phi))
  y=r*(math.sin(Ω)*math.cos(phi)+math.cos(ι)*math.cos(Ω)*math.sin(phi))
  z=r*math.sin(ι)*math.sin(phi)
  ax.scatter(x,y,z,c="green")
  if t==t1:
    min=distancia(x,y,z,xc.value,yc.value,zc.value)
    tmin=t
  if distancia(x,y,z,xc.value,yc.value,zc.value)<min:
    min=distancia(x,y,z,xc.value,yc.value,zc.value)
    print(tmin, min)
    tmin=t
  if min < rtua:
    minmin=min
    print("hay colision")
print(tmin,min)


ax.scatter(0,0,0)