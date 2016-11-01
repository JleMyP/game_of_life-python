# -*- coding: utf-8 -*-

import sys, os, time
try:
  import android
except:
  android = False

from utils import *
from life import *
from cycle import *
      

class Window(object):
  def __init__(self, w, h, buttons, labels, d=None):
    self.rect = pygame.Rect(((win_w-w)/2, (win_h-h)/2, w, h))
    self.buttons, self.labels = buttons, labels
    self.surf = ramka(None, w, h, 20, (255,255,255), lw=5)
    self.img2 = ramka(None, w-20, h-20, 20, (10,10,10))
    for b in self.buttons:
      b[0] = pygame.Rect(b[0]+b[1].get_size())
    if d:
      self.__dict__.update(d)
  
  def close(self): pass
  
  def draw(self):
    self.surf.blit(self.img2, (10,10))
    for rect, img, f, args in self.buttons:
      self.surf.blit(img, rect)
    for pos, t, color, font, center in self.labels:
      text = font.render(t.format(**globals()), True, color)
      if center:
        rect = text.get_rect()
        rect.center = pos
        self.surf.blit(text, rect)
      else:
        self.surf.blit(text, pos)
    window.blit(self.surf, self.rect)
  
  def event_callback(self, event):
    if event.type == MOUSEBUTTONDOWN:
      px, py = event.pos
      px, py = px-self.rect.x, py-self.rect.y
      for rect, img, f, args in self.buttons:
        if rect.collidepoint((px, py)):
          if not args:
            f()
          elif isinstance(args, tuple):
            f(*args)
          else:
            f(args)
  


def event_callback():
  global run
  for event in pygame.event.get():
    if event.type == QUIT:
      run = False
    elif dialog_window:
      dialog_window.event_callback(event)
    elif event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        run = False
      elif event.key == 13:
        new()
      elif event.key == K_SPACE:
        pause()
      elif event.key == K_LEFT and pause:
        back()
      elif event.key == K_RIGHT and pause:
        next()
      elif event.key == K_c:
        clear()
      elif event.key == K_f:
        show_fast()
      else:
        print event.scancode
    elif event.type == MOUSEBUTTONDOWN:
      x,y = event.pos
      for rect, img, f, cls in buttons:
        if rect.collidepoint(event.pos) and (not cls or isinstance(game, cls)):
          f()
      if pause and not fast_flag and game.rect.collidepoint(event.pos):
        game.event(event.pos)

def draw(clear=False):
  if clear:
    window.fill(0)
    game.draw(clear)
    for rect, img, f, cls in buttons:
      if not cls or isinstance(game, cls):
        window.blit(img, rect)
  pygame.draw.rect(window, 0, (win_w-bar, (btn_space+btn_size)*4, bar, win_h))
  text = font.render('FPS: %0.2f'%clock.get_fps(), True, (255,255,255))
  window.blit(text, (win_w-bar+10, win_h-font_size))
  if fast_flag:
    text = font.render('Fast: %i/%i'%(fast_flag.proc, fast_flag.n), True, (255,255,255))
    window.blit(text, (win_w-bar+10, win_h-font_size*4))
    if fast_flag.complete:
      text = font.render('%i per %i'%(fast_flag.n, fast_flag.complete), True, (255,255,255))
      window.blit(text, (win_w-bar+10, win_h-font_size*3))
  g = globals()
  for pos, t, color, cls in labels:
    if not cls or isinstance(game, cls):
      text = font.render(t.format(**g), True, color)
      window.blit(text, pos)
  pygame.draw.line(window, (255,255,255), (win_w-bar, 0), (win_w-bar, win_h))
  if dialog_window:
    dialog_window.draw()
  if fast_flag and not fast_flag.complete:
    pygame.display.update((win_w-bar, 0, bar, win_h))
  else:
    pygame.display.update()

def ramka(surf, w, h, r, clr1, clr2=0, pos=(0,0), lw=2):
  new = False
  x, y = pos
  if not surf:
    bg = clr1[0]//2, clr1[1]//2, clr1[2]//2
    surf = pygame.Surface((w, h))
    surf.fill(bg)
    new = True
  for cx, cy in ((x+r, y+r), (x+w-r, y+r), (x+w-r, y+h-r), (x+r, y+h-r)):
    pygame.draw.circle(surf, clr1, (int(cx), int(cy)), r)
    pygame.draw.circle(surf, clr2, (int(cx), int(cy)), r, lw)
  pygame.draw.rect(surf, clr1, (x, y+r, w, h-2*r))
  pygame.draw.rect(surf, clr1, (x+r, y, w-2*r, h))
  for p1, p2 in ([(x, y+r), (x, y+h-r)], [(x+r, y), (x+w-r, y)],
                 [(x+w-2, y+r), (x+w-2, y+h-r)], [(x+r, y+h-2), (x+w-r, y+h-2)]):
    pygame.draw.line(surf, clr2, p1, p2, lw)
  if new:
    surf.set_colorkey(bg)
    return surf.convert_alpha()

def text_button(w, h, text, font, r=0, btn_clr=(255,255,255), text_clr=(0,0,0)):
  if r:
    img = ramka(None, w, h, r, btn_clr, btn_clr)
  else:
    img = pygame.surface.Surface((w, h))
    img.fill(btn_clr)
  text = font.render(text, True, text_clr)
  rect = text.get_rect()
  rect.topleft = ((w-rect.width)//2, (h-rect.height)//2)
  img.blit(text, rect)
  return img
  

def init_images(size):
  img_prev = ramka(None, size, size, 5, (255,255,255), (255,255,255))
  pygame.draw.line(img_prev, 0, (size*0.25, size/2), (size*0.75, size*0.25), 4)
  pygame.draw.line(img_prev, 0, (size*0.25, size/2), (size*0.75, size*0.75), 4)
  
  img_pause = ramka(None, size, size, 5, (255,255,255), (255,255,255))
  pygame.draw.line(img_pause, 0, (size*0.25, size/4), (size*0.25, size*0.75), 4)
  pygame.draw.line(img_pause, 0, (size*0.75, size/4), (size*0.75, size*0.75), 4)
  
  img_next = ramka(None, size, size, 5, (255,255,255), (255,255,255))
  pygame.draw.line(img_next, 0, (size*0.75, size/2), (size*0.25, size*0.25), 4)
  pygame.draw.line(img_next, 0, (size*0.75, size/2), (size*0.25, size*0.75), 4)
  
  img_clear = text_button(size, size, ru('C'), btn_font, 5)
  img_size = text_button(size, size, ru('S'), btn_font, 5)
  img_new = text_button(size, size, ru('N'), btn_font, 5)
  img_fast = text_button(size, size, ru('F'), btn_font, 5)
  img_change = text_button(size, size, ru('A'), btn_font, 5)
  img_plus = text_button(size, size, ru('+'), btn_font, 5)
  img_minus = text_button(size, size, ru('-'), btn_font, 5)
  
  img_save = ramka(None, size, size, 5, (255,255,255), (255,255,255))
  pygame.draw.polygon(img_save, 0, [
    (size/4, size/2), (size/2, size/4), (size*0.75, size/2), (size*0.625, size/2),
    (size*0.625, size*0.75), (size*0.375, size*0.75), (size*0.375, size/2)])
  img_load = pygame.transform.flip(img_save, False, True)
  
  img_ok = text_button(size*4, size, ru('принять'), btn_font, 10)
  img_close = text_button(size*4, size, ru('закрыть'), btn_font, 10)
  img_p10 = text_button(size*3, size, ru('+10'), btn_font, 10)
  img_p100 = text_button(size*3, size, ru('+100'), btn_font, 10)
  img_p500 = text_button(size*3, size, ru('+500'), btn_font, 10)
  
  l = locals()
  for x in range(1, 10):
    l['img_%i'%x] = text_button(size, size, str(x), btn_font, 10)
  
  del size
  return locals()


def next():
  if not fast_flag and game.pause:
    game.step()
    game.draw()

def back():
  if not fast_flag and game.pause:
    game.back()
    game.draw(True)

def pause():
  game.pause = not game.pause

def clear():
  if not fast_flag:
    game.new(True)
    draw(True)
    if not game.pause:
      pause()

def new():
  if not fast_flag:
    game.new()
    game.draw(True)

def fast():
  if fast_flag:
    fast_flag.runing = False
  else:
    show_window(win_query_fast)

def settings():
  if isinstance(game, Life):
    show_window(win_settings_life)
  else:
    show_window(win_settings_cycle)

def save():
  game.save()

def load():
  if not fast_flag:
    try:
      game.load()
      game.draw(True)
    except:
      pass

def change_ca():
  global game
  if not fast_flag:
    cls = Cycle if isinstance(game, Life) else Life
    game = cls(game_rect, cell)
    draw(True)

def show_window(win):
  global dialog_window
  dialog_window = win

def close_window():
  global dialog_window
  dialog_window.close()
  dialog_window = None
  draw(True)

def edit_fast(n, set=False):
  win_query_fast.steps += n

def edit_cell(n):
  if 3 < win_query_cell.cell + n < 11:
    win_query_cell.cell += n

def apply_cell():
  if win_query_cell.cell != game.cell:
    game.resize(game_rect, win_query_cell.cell)
  close_window()

def fast_run(n=None):
  global fast_flag
  if not fast_flag:
    if not n:
      n = win_query_fast.steps
      close_window()
    fast_flag = Fast(game, n)
    fast_flag.start()

def fast_draw():
  history, x = fast_flag.lst, 0
  fast_flag.proc = 0
  draw()
  while x < len(history):
    event_callback()
    if not run:
      break
    if not game.pause:
      fast_flag.proc += 1
      if isinstance(game, Life):
        game.history = history[x-2:x]
        game.surf, game.alive, game.stable = history[x]
      else:
        game.surf, game.old = history[x], game.surf
      game.draw()
      game.frame += 1
      x += 1
    draw()
    clock.tick(100)



os.environ['SDL_VIDEO_CENTERED'] = "1"
ru = lambda x: str(x).decode('utf-8')
sys.stderr = sys.stdout = open('err.txt', 'w')

win_w, win_h = 1000, 650
pygame.init()
if android:
  window = pygame.display.set_mode((0, 0), FULLSCREEN)
else:
  window = pygame.display.set_mode((win_w, win_h))
win_w, win_h = window.get_size()
pygame.display.set_caption("Life")
clock = pygame.time.Clock()

run, fast_flag, cell, bar = True, False, 8, 160
btn_size, btn_space = 40, 5
#btn_space = (bar-btn_size*3)//4
btn_size = (bar-4*btn_space)//3
dialog_window = None
font_size, btn_font_size = 20, int(btn_size*0.8)
font = pygame.font.Font('freesansbold.ttf', font_size)
btn_font = pygame.font.Font('freesansbold.ttf', btn_font_size)
cx,cy = (win_w-bar)//cell//2,win_h//cell//2
love = [
  (cx-2,cy-1),(cx-1,cy-1),(cx+1,cy-1),(cx+2,cy-1),
  (cx-2,cy),(cx+2,cy),
  (cx-1,cy+1),(cx,cy+1),(cx+1,cy+1)
  ]

game_rect = (0, 0, win_w-bar, win_h)

#game = Life(game_rect, cell, (3,6,7,8), (3,4,6,7,8), (1,3))
#game = Life(game_rect, cell, (1,), range(9), ver=(1,300))
game = Life(game_rect, cell)
#game = Cycle(game_rect, cell)
#game = Kovrik(game_rect, cell, colors)

globals().update(init_images(btn_size))
buttons = [
    (pygame.Rect((win_w-bar+btn_space, btn_space, btn_size, btn_size)), img_prev, back, Life),
    (pygame.Rect((win_w-bar+btn_space*2+btn_size, btn_space, btn_size, btn_size)), img_pause, pause, None),
    (pygame.Rect((win_w-bar+btn_space*3+btn_size*2, btn_space, btn_size, btn_size)), img_next, next, None),
    
    (pygame.Rect((win_w-bar+btn_space, btn_space*2+btn_size, btn_size, btn_size)), img_clear, clear, Life),
    (pygame.Rect((win_w-bar+btn_space*2+btn_size, btn_space*2+btn_size, btn_size, btn_size)), img_new, new, None),
    (pygame.Rect((win_w-bar+btn_space*3+btn_size*2, btn_space*2+btn_size, btn_size, btn_size)), img_fast, fast, Life),
    
    (pygame.Rect((win_w-bar+btn_space, btn_space*3+btn_size*2, btn_size, btn_size)), img_size, (lambda x=0: show_window(win_query_cell)), None),
    (pygame.Rect((win_w-bar+btn_space*2+btn_size, btn_space*3+btn_size*2, btn_size, btn_size)), img_save, save, Life),
    (pygame.Rect((win_w-bar+btn_space*3+btn_size*2, btn_space*3+btn_size*2, btn_size, btn_size)), img_load, load, Life),
    
    (pygame.Rect((win_w-bar+btn_space, btn_space*4+btn_size*3, btn_size, btn_size)), img_change, change_ca, None)]

labels = [
    ((win_w-bar+10, (btn_space+btn_size)*5+font_size), ru('Кадр: {game.frame}'), (255,255,255), None),
    ((win_w-bar+10, (btn_space+btn_size)*5), '{game.map_w}x{game.map_h}', (255,255,255), None),
    ((win_w-bar+10, (btn_space+btn_size)*5+font_size*2), ru('Цвета: {game.n}'), (255,255,255), Cycle),
    ((win_w-bar+10, (btn_space+btn_size)*5+font_size*2), ru('Живые: {game.alive}'), game.colors[1], Life),
    ((win_w-bar+10, (btn_space+btn_size)*5+font_size*3), ru('Стаб.: {game.stable}'), game.colors[2], Life)]


buttons_fast = [
    [(20, btn_size+15), img_p10, edit_fast, 10],
    [(40+btn_size*3, btn_size+15), img_p100, edit_fast, 100],
    [(60+btn_size*6, btn_size+15), img_p500, edit_fast, 500],
    [(40, 5+(btn_size+10)*2), img_ok, fast_run, None],
    [(80+btn_size*4, (btn_size+15)*2), img_close, close_window, None]]
labels_fast = [
    ((250, 15+btn_font_size/2), ru('Шагов: {win_query_fast.steps}'), (255,255,255), btn_font, True)]
win_query_fast = Window(500, 200, buttons_fast, labels_fast, {'steps':0})
win_query_fast.close = lambda x=0: win_query_fast.__setattr__('steps', 0)

buttons_cell = [
    [(btn_size, 5+(btn_size+10)*2), img_ok, apply_cell, None],
    [(btn_size*6, 5+(btn_size+10)*2), img_close, close_window, None],
    [(btn_size*4, 5+(btn_size+10)), img_minus, edit_cell, -1],
    [(btn_size*6, 5+(btn_size+10)), img_plus, edit_cell, 1]]
labels_cell = [
    ((btn_size*5.5, 15+btn_font_size/2), ru('Ячейка:'), ( 255,255,255 ), btn_font, True),
    ((btn_size*5.5, 5+(btn_size*1.5+10)), ru('{win_query_cell.cell}'), (255,255,255), btn_font, True)]
win_query_cell = Window(btn_size*11, 200, buttons_cell, labels_cell, {'cell': game.cell})
win_query_cell.close = lambda x=0: win_query_cell.__setattr__('cell', game.cell)



draw(True)
while run:
  event_callback()
  if not game.pause and not fast_flag:
    game.step()
    game.draw()
  elif fast_flag and fast_flag.complete:
    fast_draw()
    fast_flag = False
    pause()
  draw()
  clock.tick(60 if not fast_flag else 10)

pygame.quit()
