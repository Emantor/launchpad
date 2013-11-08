#!/usr/bin/env python2
import midi
import midi.sequencer as sequencer

class IO:
  
  COLOR = {"amber" : 63, "green" : 60, "yellow" : 62, "dgreen" : 28, "dred" : 13, "orange" : 47, "red" : 15}
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

  def lightButton(self,x,y,color="amber"):
    button = midi.NoteOnEvent()
    if x > 7:
      return "error"
    if y > 7:
      return "error"
    button.pitch = x*16 + y
    button.velocity = self.COLOR[color]
    button.msdelay = 0
    self.seq.event_write(button)

