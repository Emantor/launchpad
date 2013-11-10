#!/usr/bin/env python2
import time
import sys
from mpd import MPDClient
import launchpad

#client_biblio = MPDClient()
#print dir(client_biblio)
#client_biblio.timeput = 1200
#client_biblio.connect("bibliothekar", 6600)
#
#client_local = MPDClient()
#print dir(client_local)
#client_local.timeput = 1200
#client_local.connect("localhost", 6600)

l = launchpad.IO()
l.clear()

tick = 0

Hosts = ["localhost", "bibliothekar", "keks", "cookie"]
MPDHost = []

j = 0
for i in Hosts:
  MPDHost.append(MPDClient())
  try:
    MPDHost[j].connect(i,6600)
    l.rightButtonOn(int(j*2),'g')
  except:
    print "No Connection"
    MPDHost.pop()
    l.rightButtonOn(int(j*2),'r')
  j = j + 1
del j

numberOfHosts = len(MPDHost)

dictVolume = {}
for i in range(0,8):
  dictVolume[(i,5,True)] = int((i+1)*12.5)

def decrementVol(Host):
  status = MPDHost[Host].status()
  currentVolume = int(status['volume'])
  if not currentVolume - 5 < 0:
    MPDHost[Host].setvol(currentVolume - 5)
  status = MPDHost[Host].status()
  displayVolumeBar(status,Host*2+1)

def incrementVol(Host):
  status = MPDHost[Host].status()
  currentVolume = int(status['volume'])
  if not currentVolume + 5 > 100:
    MPDHost[Host].setvol(currentVolume + 5)
  status = MPDHost[Host].status()
  displayVolumeBar(status,Host*2+1)

def setVol(port):
  pass  

def displayVolumeBar(status,offset):
  volbutton = int(int(status['volume'])/12.5)
  for i in range(0,8):
    if i >= volbutton:
      l.gridButtonOn(i,offset,'e')
    else:
      l.gridButtonOn(i,offset,'g')

def displayStatus(status,offset):
  if status['state'] == 'play':
    l.gridButtonOn(1,offset,'g')
  if status['state'] == 'pause':
    l.gridButtonOn(1,offset,'a')

def displayPeriodic():
  Hostnumber = 0
  for i in MPDHost:
    status = MPDHost[Hostnumber].status()
    displayStatus(status,2*Hostnumber)
    displayVolumeBar(status,2*Hostnumber+1)
    Hostnumber = Hostnumber + 1

def toggle(Host):
  status = MPDHost[Host].status()
  if status['state'] == 'play':
    MPDHost[Host].pause()
    l.gridButtonOn(1,Host*2,'a')
  else:
    MPDHost[Host].play()
    l.gridButtonOn(1,Host*2,'g')

def next(Host):
  MPDHost[Host].next()

def previous(Host):
  MPDHost[Host].previous()

def exitProg(Host):
  l.clear()
  quit()

dictKeyBindings = {}
for i in range(0,numberOfHosts*2):
  xbinding = 0
  Host = int(i / 2)
  print Host
  if i % 2 == 0:
    dictKeyBindings[(xbinding,i,True)] = previous
    xbinding += 1
    dictKeyBindings[(xbinding,i,True)] = toggle
    xbinding += 1
    dictKeyBindings[(xbinding,i,True)] = next
    xbinding += 1
    dictKeyBindings[(xbinding,i,True)] = decrementVol
    xbinding += 1
    dictKeyBindings[(xbinding,i,True)] = incrementVol
    xbinding += 1
  else:
    for xbinding in range(0,8):
      dictKeyBindings[(xbinding,i,True)] = setVol
dictKeyBindings[(8,7,False)] = exitProg

while True:
  if tick == 25:
    displayPeriodic()
    tick = 0
  button = l._IO__ButtonRecv()
  while button is not None:
    if button in dictKeyBindings:
      dictKeyBindings[button](button[1]/2)
    button = l._IO__ButtonRecv()

  time.sleep(0.04)
  tick = tick + 1
