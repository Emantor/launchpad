#!/usr/bin/env python2
import midi
import midi.sequencer as sequencer

class IO:
  
  COLOR = {"amber" : 63, "green" : 60, "yellow" : 62, "dgreen" : 28, "dred" : 13, "orange" : 47, "red" : 15}
  

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
    client = self.s["Launchpad Mini"].client
    port = self.s["Launchpad Mini"]["Launchpad Mini MIDI 1"].port
    
    self.seq = sequencer.SequencerDuplex(sequencer_resolution=120)
    self.seq.subscribe_read_port(client, port)
    self.seq.subscribe_write_port(client, port)
    self.seq.start_sequencer()

  def __del__(self):
    del self.s
    del self.seq

  def __ButtonCmd(self,x,y,state=True,color="amber"):
    button = midi.NoteOnEvent()
    if x > 8:
      return "error"
    if y > 7:
      return "error"
    button.pitch = y*16 + x
    if state:
      button.velocity = self.COLOR[color]
    else:
      button.velocity = 12
    self.seq.event_write(button,True)

  def gridButtonOn(self,x,y,color="amber"):
    if x > 7:
      return "error"
    if y > 7:
      return "error"
    self.__ButtonCmd(x,y,True,color)

  def letterButtonOn(self,Letter,color="amber"):
    if Letter in self.LETTERS:
      self.__ButtonCmd(8,self.LETTERS[Letter],True,color)
    else:
      return "error"
    
  def letterButtonOff(self,Letter):
    if Letter in self.LETTERS:
      self.__ButtonCmd(8,self.LETTERS[Letter],False)
    else:
      return "error"

  def gridButtonOff(self,x,y):
    if x > 7:
      return "error"
    if y > 7:
      return "error"
    self.__ButtonCmd(x,y,False)

  def writeLetter(self,Letter,xoffset=0,yoffset=0,color="amber"):
    if yoffset > 5:
      return "error"
    if xoffset > 4:
      return "error"
    for i in range(0,5):
      for j in range(0,4):
        print j
        row = list(Letter[i])
        if row[j] == '1':
          self.__onButton(i + yoffset,j + xoffset,color)
        else:
          self.offButton(i + yoffset,j + xoffset)

  def clear(self):
    command = midi.ControlChangeEvent()
    command.control = 0
    command.value = 0
    self.seq.event_write(command,True)
