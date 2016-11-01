import pygame
from pygame.locals import *
from utils import *


class Cycle:
  def __init__(self, rect, cell, colors=0, obl=None):
    if isinstance(colors, int):
      self.n = colors if colors else rnd(7, 15)
      colors = [(rnd(255), rnd(255), rnd(255)) for i in xrange(self.n)]
    self.resize(rect, cell)
    self.colors = colors
    self.n, self.pause = len(colors), True
    self.obl_f = get_sum_neuman_value if not obl else obl
    self.window = pygame.display.get_surface()

  def resize(self, rect, cell):
    self.cell = cell
    self.map_w, self.map_h = rect[2]//cell, rect[3]//cell
    self.rect = pygame.Rect(tuple(rect[:2])+(self.map_w*cell, self.map_h*cell))
    self.new(0,0)
  
  def new(self, clear=False, change=True):
    if change:
      self.n = rnd(7, 15)
      self.colors = [(rnd(255), rnd(255), rnd(255)) for i in xrange(self.n)]
    if not clear:
      self.surf = generate(self.map_w, self.map_h, range(self.n))
    else:
      self.surf = generate_empty(self.map_w, self.map_h, -1)
    self.old = generate_empty(self.map_w, self.map_h, -1)
    self.frame = 0

  def copy(self):
    c = Cycle(self.rect, self.cell, self.colors, self.obl_f)
    c.surf, c.old, c.frame = self.surf, self.old, self.frame
    return c

  def step(self, fast=False):
    self.old = self.surf
    nsurf = generate_empty(self.map_w, self.map_h, -1)
    for x in xrange(self.map_w):
      for y in xrange(self.map_h):
        next = 0 if self.surf[x][y] == self.n-1 else self.surf[x][y]+1
        sum = self.obl_f(x, y, self.surf, self.map_w, self.map_h, next)
        nsurf[x][y] = next if sum else self.surf[x][y]
    self.surf = nsurf
    if fast:
      return nsurf
    self.frame += 1
  
  def step_f(self):
    return self.step(1)

  def event(self, pos):
    cx, cy = (pos[0]-self.rect.x)//self.cell, (pos[1]-self.rect.y)//self.cell

  def draw(self, flag=False):
    for x in xrange(self.map_w):
      for y in xrange(self.map_h):
        if self.surf[x][y] != self.old[x][y]:
          pygame.draw.rect(self.window, self.colors[self.surf[x][y]], (
            x*self.cell+1+self.rect.x, y*self.cell+1+self.rect.y, self.cell-1, self.cell-1))