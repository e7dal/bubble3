import os
import sys
import json

from bubble3 import Bubble

class BubbleClient(Bubble):
 def __init__(self,cfg={}):
  self.CFG=cfg
  print(self.CFG)
 def pull(self, amount=4242, index=0):
  self.say('BC: %d,%d'%(amount,index))
  for i in range(amount):
   #jl=json.loads(l)
   yield {'in':'Hello %d'%(i)}
 def push(self, d={}):
  print(json.dumps(d))     #stdout

