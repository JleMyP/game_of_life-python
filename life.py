import pygame
from pygame.locals import *
from utils import *


class Life:
  def __init__(self, rect, cell, born=(3,), save=(2,3), ver=(2,5), colors=None, lst=None, sum_func=None):
    self.born, self.save, self.ver = born, save, ver
    self.colors = colors if colors else (0, (0,255,0), (150,150,150))
    self.spawn = (0,)*(ver[1]-ver[0])+(1,)*ver[0]
    self.alive = self.stable = 0
    self.pause = True
    self.find_stable = self.find_stop = False
    self.sum_func = sum_func or get_sum_mur
    self.resize(rect, cell)
    self.nsurf = generate_empty(self.map_w, self.map_h)
    self.window = pygame.display.get_surface()
    if lst is not None:
      self.new(True)
      for x, y in lst:
        self.surf[x][y] = 1
  
  def resize(self, rect, cell):
    self.cell = cell
    self.map_w, self.map_h = rect[2]//cell, rect[3]//cell
    self.rect = pygame.Rect(tuple(rect[:2])+(self.map_w*cell, self.map_h*cell))
    self.new()
    #self.draw(True)
  
  def copy(self):
    l = Life(self.rect, self.cell, self.born, self.save, self.ver, self.colors, sum_func=self.sum_func)
    l.surf, l.history, l.frame = self.surf, self.history, self.frame
    return l
  
  def new(self, clear=False):
    self.history, self.frame = [], 0
    self.nsurf = generate_empty(self.map_w, self.map_h)
    if clear:
      self.surf = generate_empty(self.map_w, self.map_h)
    else:
      self.surf = generate(self.map_w, self.map_h, self.spawn)

  def step(self):
    self.history.append((self.surf, self.alive, self.stable))
    if len(self.history) == 101:
      del self.history[0]
    ln_his = len(self.history)
    nsurf = generate_empty(self.map_w, self.map_h)
    self.alive = self.stable = 0
    for x in xrange(self.map_w):
      for y in xrange(self.map_h):
        sum = self.sum_func(x, y, self.surf, self.map_w, self.map_h)
        if sum in self.born:
          self.nsurf[x][y] = self.surf[x][y] or 1
        elif sum in self.save:
          self.nsurf[x][y] = self.surf[x][y]
        else:
          self.nsurf[x][y] = 0
        if self.find_stable and self.nsurf[x][y] == 1 and ln_his >= 10:
          for h, a, s in self.history[-10:]:
            if h[x][y] != self.nsurf[x][y]:
              break
          else:
            self.nsurf[x][y] = 2
        self.alive += 1 if self.nsurf[x][y] == 1 else 0
        if self.find_stable:
          self.stable += 1 if self.nsurf[x][y] == 2 else 0
    self.surf, self.nsurf = self.nsurf, self.surf
    if self.alive:
      self.frame += 1
      if self.find_stop:
        for h, a, s in self.history[-10::2]:
          if h != self.surf:
            break
        else:
          self.frame -= 1

  def step_f(self):
    self.nsurf = generate_empty(self.map_w, self.map_h)
    for x in xrange(self.map_w):
      for y in xrange(self.map_h):
        sum = self.sum_func(x, y, self.surf, self.map_w, self.map_h)
        if (sum in self.born or sum in self.save and self.surf[x][y]):
          self.nsurf[x][y] = 1
        else:
          self.nsurf[x][y] = 0
    self.surf, self.nsurf = self.nsurf, self.surf
    return self.surf, 0, 0
    
  def back(self):
    if len(self.history) >= 1:
      self.surf, self.alive, self.stable = self.history[-1]
      self.frame -= 1
      del self.history[-1]
      self.draw(True)

  def event(self, pos):
    cx, cy = (pos[0]-self.rect.x)//self.cell, (pos[1]-self.rect.y)//self.cell
    if self.surf[cx][cy]:
      self.surf[cx][cy] = 0
    else:
      self.surf[cx][cy] = 1
    self.draw(one=(cx, cy))

  def draw(self, all=False, one=None):
    if one:
      x, y = one
      pygame.draw.rect(self.window, self.colors[self.surf[x][y]], (
        x*self.cell+1+self.rect.x, y*self.cell+1+self.rect.y, self.cell-1, self.cell-1))
      #  x*self.cell+self.px+self.cell//2, y*self.cell+self.py+self.cell//2), self.cell//2)
      return
    for x in xrange(self.map_w):
      for y in xrange(self.map_h):
        if not self.history or self.surf[x][y] != self.history[-1][0][x][y] or all:
          pygame.draw.rect(self.window, self.colors[self.surf[x][y]] ,(
            x*self.cell+1+self.rect.x, y*self.cell+1+self.rect.y, self.cell-1, self.cell-1))
          #  x*self.cell+self.px+self.cell//2, y*self.cell+self.py+self.cell//2), self.cell//2)

  def save_map(self, name="map"):
    with open("%s.txt"%name, 'w') as f:
      for y in xrange(self.map_h):
        lst = [str(self.surf[x][y]) for x in xrange(self.map_w)]
        f.write(''.join(lst)+'\n')

  def load_map(self, name="map"):
    with open('%s.txt'%name) as f:
      lines = f.readlines()
      self.surf = [[int(lines[y][x]) for y in xrange(self.map_h)] for x in xrange(self.map_w)]
