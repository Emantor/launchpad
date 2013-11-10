#!/usr/bin/env python2
import random
import midi
import midi.sequencer as sequencer

class IO:
  
  COLOR = {"a" : 63, "g" : 60, "y" : 62, "f" : 28, "e" : 13, "o" : 47, "r" : 15, "o" : 12}
  invCOLOR = {v:k for k, v in COLOR.items()}

  persistentButtonState = [[12]*9,
                           [12]*9,
                           [12]*9,
                           [12]*9,
                           [12]*9,
                           [12]*9,
                           [12]*9,
                           [12]*9
                          ]
  

  P = ['1110',
       '1001',
       '1110',
       '1000',
       '1000',
      ]

  H = ['1001',
       '1001',
       '1111',
       '1001',
       '1001',
      ]

  O = ['0110',
       '1001',
       '1001',
       '1001',
       '0110',
      ]

  E = ['1110',
       '1000',
       '1110',
       '1000',
       '1110',
      ]

  N = ['1001',
       '1101',
       '1011',
       '1001',
       '1001',
      ]

  I = ['1110',
       '0100',
       '0100',
       '0100',
       '1110',
      ]

  X = ['1001',
       '0110',
       '0110',
       '0110',
       '1001',
      ]

  LETTERS = {"A": 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7}

  def __init__(self): 
    self.s = sequencer.SequencerHardware()
    print self.s
    client = self.s["Launchpad Mini"].client
    port = self.s["Launchpad Mini"]["Launchpad Mini MIDI 1"].port
    
    self.seq = sequencer.SequencerDuplex(sequencer_resolution=120)
    self.seq.subscribe_read_port(client, port)
    self.seq.subscribe_write_port(client, port)
    self.seq.start_sequencer()
    self.flashOn()

  def __del__(self):
    del self.s
    del self.seq

  def __ButtonCmd(self,x,y,state=True,color=63,persist=False,flash=False):
    button = midi.NoteOnEvent()
    if x > 8:
      return "error"
    if y > 7:
      return "error"
    button.pitch = y*16 + x
    if state:
      if persist:
        self.persistentButtonState[y][x] = color
      if flash:
        button.velocity = color - 4
      else:
        button.velocity = color
    else:
      button.velocity = self.persistentButtonState[y][x]
    self.seq.event_write(button,True)

  def __ButtonRecv(self,lightup=True,lightcolor="a"):
    event = self.seq.event_read()
    if event is not None:
      if hasattr(event, 'pitch'):
        x = event.pitch % 16
        y = event.pitch / 16
        if lightup and event.velocity == 127:
          self.__ButtonCmd(x,y,True,self.COLOR[lightcolor])
          pressed = True
        elif lightup and event.velocity == 0:
          self.__ButtonCmd(x,y,False)
          pressed = False
        return x,y,pressed
      elif hasattr(event, 'control'):
        button = event.control - 104
        if lightup and event.value == 127:
          self.__TopButtonCmd(button,True,self.COLOR[lightcolor])
        elif lightup and event.value == 0:
          self.__TopButtonCmd(button,False)
        return button
      else:
        return 'unknown'


  def __TopButtonCmd(self,x,state=True,color=63):
    if x > 7:
      return 'error'
    command = midi.ControlChangeEvent()
    command.control = 104 + x
    if state:
      command.value = color
    else:
      command.value = 12
    self.seq.event_write(command,True)

  def topButtonOn(self,x,color="a"):
    self.__TopButtonCmd(x,True,self.COLOR[color],True)

  def topButtonOff(self,x,color="a"):
    self.__TopButtonCmd(x,False)

  def gridButtonOn(self,x,y,color="a",flash=False):
    if x > 7:
      return "error"
    self.__ButtonCmd(x,y,True,self.COLOR[color],True,flash)

  def gridButtonOff(self,x,y):
    if x > 7:
      return "error"
    if y > 7:
      return "error"
    self.__ButtonCmd(x,y,True,12)

  def gridButtonOnColor(self,x,y,color):
    if x > 7:
      return "error"
    self.__ButtonCmd(x,y,True,color)

  def letterButtonOn(self,Letter,color="a"):
    if Letter in self.LETTERS:
      self.__ButtonCmd(8,self.LETTERS[Letter],True,self.COLOR[color])
    else:
      return "error"
    
  def letterButtonOff(self,Letter):
    if Letter in self.LETTERS:
      self.__ButtonCmd(8,self.LETTERS[Letter],True,12)
    else:
      return "error"

  def rightButtonOn(self,number,color="a",flash=False):
    if number > 7:
      return "error"
    self.__ButtonCmd(8,number,True,self.COLOR[color],True,flash)

  def rightButtonOff(self,number):
    if number > 7:
      return "error"
    self.__ButtonCmd(8,number,True,12)

  def writeLetter(self,Letter,xoffset=0,yoffset=0,color="a"):
    if yoffset > 5:
      return "error"
    if xoffset > 4:
      return "error"
    for i in range(0,5):
      for j in range(0,4):
        print j
        row = list(Letter[i])
        if row[j] == '1':
          self.gridButtonOn(j + xoffset,i + yoffset,COLOR[color])
        else:
          self.gridButtonOff(j + xoffset,i + yoffset)

  def clear(self):
    command = midi.ControlChangeEvent()
    command.control = 0
    command.value = 0
    self.seq.event_write(command,True)

  def flashOn(self):
    command = midi.ControlChangeEvent()
    command.control = 0
    command.value = 40
    self.seq.event_write(command,True)

  def randScreen(self):
    for i in range(0,8):
      for j in range(0,9):
        colorrand = random.randint(13,63)
        self.__ButtonCmd(j,i,True,colorrand)

