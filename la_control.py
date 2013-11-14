#!/usr/bin/env python2
import time
import sys
from mpd import MPDClient
from xbmcjson import XBMC,PLAYER_VIDEO
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
l.ledHigh()

tick = 0

XBMCHosts = ["minibox.local"]
XBMCHost = []

MPDHosts = ["localhost"]
MPDHost = []

state = "MPD"
l.topButtonOn(0,'g')
l.topButtonOn(1,'a')

def connectMPD(Host):
    MPDHost.append(MPDClient())
    try:
      MPDHost[Host].timeout = 12000
      MPDHost[Host].connect(MPDHosts[Host],6600)
      l.rightButtonOn(int(Host*2),'g')
    except:
      print "No Connection"
      MPDHost.pop()
      l.rightButtonOn(int(Host*2),'r')

def connectXBMC(Host):
    try:
      XBMCHost.append(XBMC("http://" + XBMCHosts[Host] + ":8080/jsonrpc"))
      l.rightButtonOn(int(Host*2),'g')
    except:
      print "No Connection"
      l.rightButtonOn(int(Host*2),'r')


for position,item in enumerate(MPDHosts):
  print position
  connectMPD(position)


numberOfHosts = len(MPDHost)


def tryXBMC(func):
    def catchXBMC(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print "XBMC not Connected"
    return catchXBMC

def tryMPD(func):
    def catchMPD(*args, **kwargs):
        Host = args[1]/2
        try:
            return func(*args, **kwargs)
        except:
            l.rightButtonOn(int(Host*2),'r')
            print "MPD not connected"
    return catchMPD

@tryMPD
def decrementVol(x,y):
  Host = y/2
  status = MPDHost[Host].status()
  currentVolume = int(status['volume'])
  if not currentVolume - 5 < 0:
    MPDHost[Host].setvol(currentVolume - 5)
  status = MPDHost[Host].status()
  displayMPDVolumeBar(status,Host*2+1)

@tryMPD
def incrementVol(x,y):
  Host = y/2
  status = MPDHost[Host].status()
  currentVolume = int(status['volume'])
  if not currentVolume + 5 > 100:
    MPDHost[Host].setvol(currentVolume + 5)
  status = MPDHost[Host].status()
  displayMPDVolumeBar(status,Host*2+1)

@tryMPD
def setVol(x,y):
  Host = y/2
  volume = int(x*12.5+12.5)
  MPDHost[Host].setvol(volume)
  status = MPDHost[Host].status()
  displayMPDVolumeBar(status,Host*2+1)

def displayMPDVolumeBar(status,offset):
  volbutton = int(int(status['volume'])/12.5)
  for i in range(0,8):
    if i >= volbutton:
      l.gridButtonOn(i,offset,'e')
    else:
      l.gridButtonOn(i,offset,'f')

def displayMPDStatus(status,offset):
  if status['state'] == 'play':
    l.gridButtonOn(1,offset,'f')
  if status['state'] == 'pause':
    l.gridButtonOn(1,offset,'s')

def displayMPDPeriodic():
  Hostnumber = 0
  for i in MPDHost:
    status = MPDHost[Hostnumber].status()
    displayMPDStatus(status,2*Hostnumber)
    displayMPDVolumeBar(status,2*Hostnumber+1)
    Hostnumber = Hostnumber + 1

@tryMPD
def MPDtoggle(x,y):
  Host = y/2
  status = MPDHost[Host].status()
  if status['state'] == 'play':
    MPDHost[Host].pause()
    l.gridButtonOn(1,Host*2,'s')
  else:
    MPDHost[Host].play()
    l.gridButtonOn(1,Host*2,'f')

@tryMPD
def MPDnext(x,y):
  Host = y/2
  MPDHost[Host].next()

@tryMPD
def MPDprevious(x,y):
  Host = y/2
  MPDHost[Host].previous()

def exitProg(x,y):
  l.clear()
  quit()

@tryXBMC
def displayXBMCPeriodic():
  displayXBMCStatus()
  Hostnumber = 0
  for i in MPDHost:
    status = MPDHost[Hostnumber].status()
    Hostnumber = Hostnumber + 1

@tryXBMC
def displayXBMCStatus():
  l.gridButtonOn(0,0,'f')
  l.gridButtonOn(1,0,'e')
  l.gridButtonOn(2,0,'f')
  l.gridButtonOn(0,1,'e')
  l.gridButtonOn(1,1,'f')
  l.gridButtonOn(2,1,'e')
  l.gridButtonOn(0,2,'f')
  l.gridButtonOn(1,2,'e')
  l.gridButtonOn(2,2,'f')
  l.gridButtonOn(0,3,'s')
  l.gridButtonOn(1,3,'s')
  l.gridButtonOn(2,3,'s')
  l.gridButtonOn(3,3,'s')
  

@tryXBMC
def XBMCDown(x,y):
  XBMCHost[0].Input.Down()

@tryXBMC
def XBMCUp(x,y):
  XBMCHost[0].Input.Up()

@tryXBMC
def XBMCRight(x,y):
  XBMCHost[0].Input.Right()

@tryXBMC
def XBMCLeft(x,y):
  XBMCHost[0].Input.Left()

@tryXBMC
def XBMCSelect(x,y):
  XBMCHost[0].Input.Select()

@tryXBMC
def XBMCBack(x,y):
  XBMCHost[0].Input.Back()

@tryXBMC
def XBMCTitle(x,y):
  XBMCHost[0].Input.ExecuteAction(action='title')

@tryXBMC
def XBMCMenu(x,y):
  XBMCHost[0].Input.ExecuteAction(action="osd")

@tryXBMC
def XBMCInfo(x,y):
  XBMCHost[0].Input.Info()

@tryXBMC
def XBMCPrevious(x,y):
  XBMCHost[0].Input.ExecuteAction(action='previous')

@tryXBMC
def XBMCToggle(x,y):
  XBMCHost[0].Input.ExecuteAction(action='playpause')

@tryXBMC
def XBMCNext(x,y):
  XBMCHost[0].Input.ExecuteAction(action='next')

@tryXBMC
def XBMCStop(x,y):
  XBMCHost[0].Input.ExecuteAction(action='stop')

def generateMPDKeyBindings():
  dictKeyBindings = {}
  for i in range(0,numberOfHosts*2):
    xbinding = 0
    Host = int(i / 2)
    if i % 2 == 0:
      dictKeyBindings[(xbinding,i,True)] = MPDprevious
      xbinding += 1
      dictKeyBindings[(xbinding,i,True)] = MPDtoggle
      xbinding += 1
      dictKeyBindings[(xbinding,i,True)] = MPDnext
      xbinding += 1
      dictKeyBindings[(xbinding,i,True)] = decrementVol
      xbinding += 1
      dictKeyBindings[(xbinding,i,True)] = incrementVol
      xbinding += 1
    else:
      for xbinding in range(0,8):
        dictKeyBindings[(xbinding,i,True)] = setVol
  dictKeyBindings[(8,7,False)] = exitProg
  dictKeyBindings[(0,False)] = stateMPD
  dictKeyBindings[(1,False)] = stateXBMC
  return dictKeyBindings

def generateXBMCKeyBindings():
  dictKeyBindings = {}
  dictKeyBindings[(0,0,False)] = XBMCTitle
  dictKeyBindings[(1,0,False)] = XBMCUp
  dictKeyBindings[(2,0,False)] = XBMCInfo
  dictKeyBindings[(0,1,False)] = XBMCLeft
  dictKeyBindings[(1,1,False)] = XBMCSelect
  dictKeyBindings[(2,1,False)] = XBMCRight
  dictKeyBindings[(0,2,False)] = XBMCMenu
  dictKeyBindings[(1,2,False)] = XBMCDown
  dictKeyBindings[(2,2,False)] = XBMCBack
  dictKeyBindings[(0,3,False)] = XBMCPrevious
  dictKeyBindings[(1,3,False)] = XBMCToggle
  dictKeyBindings[(2,3,False)] = XBMCNext
  dictKeyBindings[(3,3,False)] = XBMCStop
  dictKeyBindings[(0,False)] = stateMPD
  dictKeyBindings[(1,False)] = stateXBMC
  dictKeyBindings[(8,7,False)] = exitProg
  return dictKeyBindings

def stateMPD(x,y):
  global state
  state = "MPD"
  l.clear()
  l.topButtonOn(0,'g')
  l.topButtonOn(1,'a')
  displayMPDPeriodic()
  print state

def stateXBMC(x,y):
  global state
  state = "XBMC"
  l.clear()
  l.topButtonOn(1,'g')
  l.topButtonOn(0,'a')
  displayXBMCPeriodic()
  print state

dictMPDKeyBindings = {}
dictMPDKeyBindings = generateMPDKeyBindings()

dictXBMCKeyBindings = {}
dictXBMCKeyBindings = generateXBMCKeyBindings()

while True:
  if tick == 25:
    if state == "MPD":
      displayMPDPeriodic()
    if state == "XBMC":
      displayXBMCPeriodic()
    tick = 0
  button = l._IO__ButtonRecv()
  while button is not None:
    if state == "MPD":
      if button in dictMPDKeyBindings:
        dictMPDKeyBindings[button](button[0],button[1])
    if state == "XBMC":
      if button in dictXBMCKeyBindings:
        dictXBMCKeyBindings[button](button[0],button[1])
    button = l._IO__ButtonRecv()

  time.sleep(0.04)
  tick = tick + 1
