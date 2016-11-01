from threading import Thread
from random import randrange as rnd, choice
import time


class Fast(Thread):
  def __init__(self, game, n):
    Thread.__init__(self)
    self.game, self.n, self.complete = game.copy(), n, False
    self.lst, self.runing, self.proc = [], False, 0
  
  def run(self):
    self.runing = True
    t1 = time.time()
    for self.proc in xrange(1, self.n+1):
      if not self.runing:
        break
      self.lst.append(self.game.step_f())
    self.n = self.proc
    t = time.time() - t1
    self.complete = t



def generate(w, h, lst):
  return [[choice(lst) for y in xrange(h)] for x in xrange(w)]

def generate_empty(w, h, v=0):
  return [[v for y in xrange(h)] for x in xrange(w)]

def get_values_mur(x, y, map, w, h):
  sum = 0
  for px, py in ((x-1, y-1), (x, y-1), (x+1, y-1),
                 (x-1, y),             (x+1, y),
                 (x-1, y+1), (x, y+1), (x+1, y+1)
                ):
    sum += map[px%w][py%h]
  return sum

def get_sum_mur(x, y, map, w, h):
  sum = 0
  for px, py in ((x-1, y-1), (x, y-1), (x+1, y-1),
                 (x-1, y),             (x+1, y),
                 (x-1, y+1), (x, y+1), (x+1, y+1)
               ):
    if px == w: px = 0
    if py == h: py = 0
    sum += 1 if map[px][py] else 0
  return sum

def get_sum_neuman(x, y, map, w, h):
  sum = 0
  for px, py in ((x, y-1), (x, y+1), (x-1, y), (x+1, y)):
    sum += 1 if map[px%w][py%h] else 0
  return sum

def get_sum_mur_value(x, y, map, w, h, value):
  sum = 0
  for px, py in ((x-1, y-1), (x, y-1), (x+1, y-1),
                (x-1, y),             (x+1, y),
                (x-1, y+1), (x, y+1), (x+1, y+1)
               ):
    sum += 1 if map[px%w][py%h] == value else 0
  return sum

def get_sum_dia_value(x, y, map, w, h, value):
  sum = 0
  for px, py in ((x-1, y-1), (x-1, y+1), (x+1, y+1), (x+1, y-1)):
    sum += 1 if map[px%w][py%h] == value else 0
  return sum

def get_sum_neuman_value(x, y, map, w, h, value):
  sum = 0
  for px, py in ((x, y-1), (x, y+1), (x-1, y), (x+1, y)):
    sum += 1 if map[px%w][py%h] == value else 0
  return sum