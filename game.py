import pygame
from random import randint
import json
import victory
import start

def game(mode):

  class Board:
      def __init__(self, width, height, screen, left=10, top=10):
          self.transp = pygame.Surface(size, pygame.SRCALPHA)
          self.screen = screen
          self.constant(width, height, screen, left=10, top=10)
  
          self.turn = 0
          self.board = [[0] * height for _ in range(width)]
          self.pole = [[0] * height for _ in range(width)]
          if mode==0:
            self.create_pole()
          else:
            self.load()
          self.draw_pole()
          self.change_turn()
  
          self.show_m = 0
          self.show_f = 0
          self.place_m = 0
          self.unit_move = 0
          self.unit_fire = 0
          
  
          # self.units = []
           
          self.buttons()
          self.draw_income()
          self.load_sound()
          self.create_fire_sprite()
  
      def constant(self, width, height, screen, left=10, top=10):
          self.width = width
          self.height = height
          self.cell_size = 50
          self.left = left + 5
          self.right = 20
          self.top = 20
          self.right_kray = width * self.cell_size
          self.button_tank = (self.right_kray + 50, 250, 75, 50)
          self.button_sold = (self.right_kray + 50, 330, 110, 50)
          self.button_turn = (self.right_kray + 50, 180, 180, 40)
          self.button_supertank = (self.right_kray + 50, 410, 120, 50)
          self.button_turn_text=(self.right_kray + 50, 180)
          self.button_save = (self.right_kray + 50, 490, 240, 50)
          self.button_menu = (self.right_kray + 50, 550, 240, 50)
          self.text_xy = (self.right_kray + 50, 30)
          self.income_xy = (self.right_kray + 50, 110)
          self.money_xy = (self.right_kray + 50, 70)
          self.money1 = 1000
          self.money2 = 1000
          self.income1 = 0
          self.income2 = 0
          self.base1 = (5, 0)
          self.base2 = (width - 6, height - 1)
  
          self.sold_price = 200
          self.tank_price = 500
          self.supertank_price = 100
  
          self.fire_start=10**10
          self.end=0

      def load(self):
        f=open("save.txt","r")
        data=json.load(f)
        self.pole=data['pole']
        self.turn=data['turn']
        
        self.money1=data['money1']
        self.money2=data['money2']
        for x in range(len(self.board)):
          for y in range(len(self.board)):
            if data['board'][x][y]!=0:
              unit=data['board'][x][y]
              
              if unit[0]==1:
                self.add_unit(Tank(x, y, unit[1],can_move=unit[3],has_hp=unit[2]))
              elif unit[0]==2:
                self.add_unit(Soldier(x, y, unit[1],can_move=unit[3],has_hp=unit[2]))
              elif unit[0]==3:
                self.add_unit(Trak(x, y, unit[1],can_move=unit[3],has_hp=unit[2]))
                       

        f.close()


      def save(self):
        f=open("save.txt","w")
        data={}
        data['turn']=self.turn
        data['pole']=self.pole
        data['money1'] = self.money1
        data['money2'] = self.money2
        save_board=[[0] * self.height for _ in range(self.width)]
        for x in range(len(self.board)):
          for y in range(len(self.board)):
            if self.board[x][y]!=0:
              unit= self.board[x][y]
            
              save_board[x][y]=[unit.type,unit.player,unit.hp,unit.can_move]
            
        data['board']=save_board
        file_data=json.dumps(data)
        f.write(file_data)

        f.close()
  
      def create_fire_sprite(self):
        self.fire_image = pygame.image.load("fire.png")
        self.fire_image = pygame.transform.scale(self.fire_image, (40, 40))
        self.fire_sprite = pygame.sprite.Sprite()
        self.fire_sprite.image = self.fire_image
        self.fire_sprite.rect = self.fire_sprite.image.get_rect()
        
      def draw_income(self):
        self.screen.fill((43, 0, 61), (*self.income_xy, 250, 40))
  
        if self.turn == 0:
              text = myfont.render('Доход: '+str(self.income1), False, (255, 0, 0))
        else:
              text = myfont.render('Доход: '+str(self.income2), False, (0, 0, 255))
        screen.blit(text, (self.income_xy))
  
      def load_sound(self):
          self.sound_shot = pygame.mixer.Sound('shot.mpeg')
          self.sound_music=pygame.mixer.Sound('music.mpeg')
          self.sound_music.set_volume(0.01)
          #self.sound_music.play(loops=-1)
          
          # загрузим все остальные звуки
  
      def create_base(self):
          x1, y1 = self.base1
          x2, y2 = self.base2
          pygame.draw.rect(screen, (0, 0, 255),
                           (self.left + x1 * self.cell_size, self.top +
                            y1 * self.cell_size, self.cell_size, self.cell_size),
                           2)
          pygame.draw.rect(screen, (255, 0, 0),
                           (self.left + x2 * self.cell_size, self.top +
                            y2 * self.cell_size, self.cell_size, self.cell_size),
                           2)
  
      def check_victory(self):
          x1, y1 = self.base1
          x2, y2 = self.base2
          if self.board[x1][y1]:
              if self.board[x1][y1].player == 0:
                  
                  
                  victory.victory(1)
          elif self.board[x2][y2]:
              if self.board[x2][y2].player == 1:
                 
                  victory.victory(2)
  
      
  
      def create_pole(self):
          for x in range(len(self.pole)):
              for y in range(len(self.pole[x]) // 2):
                  self.pole[x][y] = randint(1, 20)
          for x in range(len(self.pole)):
              for y in range(len(self.pole[x]) // 2):
                  self.pole[x][y + len(self.pole[x]) //
                               2] = self.pole[x][len(self.pole[x]) // 2 - y - 1]
          #print(self.pole)
  
      def draw_pole(self):
          for x in range(len(self.board)):
              for y in range(len(self.board[x])):
                  color = (int(130 * (self.pole[x][y] / 20)),
                           int(130 * (self.pole[x][y] / 20)), 0, 64)
                  #print(color)
                  self.fill_cell(x, y, color)
          #screen.blit(self.transp,(0,0))
  
      def erase_transp(self):
          for x in range(len(self.board)):
              for y in range(len(self.board[x])):
                  self.fill_cell(x, y, (0, 0, 0))
  
      def count_income(self):
          income = 0
          for x in range(len(self.board)):
              for y in range(len(self.board[x])):
                  if self.board[x][y] != 0:
                      if self.board[x][y].player == self.turn:
                          rad = self.board[x][y].income
                          for x1 in range(x - rad, x + rad + 1):
                              for y1 in range(y - rad, y + rad + 1):
                                  if x1 < self.width and y1 < self.height:
                                      income += self.pole[x1][y1]
          if self.turn == 0:
              self.income1 = income
          else:
              self.income2 = income
  
      def buttons(self):
          self.screen.fill("yellow", self.button_turn)
          self.screen.fill("green", self.button_sold)
          self.screen.fill("green", self.button_tank)
          self.screen.fill("green", self.button_supertank)
          self.screen.fill("red", self.button_save)
          self.screen.fill("red", self.button_menu)
          
          text = myfont.render('Конец хода', False, (0, 0, 0))
          screen.blit(text, (self.button_turn_text))

          text1 = myfont.render('Танк', False, (0, 0, 0))
          screen.blit(text1, (self.button_tank))

          text2 = myfont.render('Солдат', False, (0, 0, 0))
          screen.blit(text2, (self.button_sold))

          text3 = myfont.render('Трактор', False, (0, 0, 0))
          screen.blit(text3, (self.button_supertank))

          text4 = myfont.render('Сохранить игру', False, (0, 0, 0))
          screen.blit(text4, (self.button_save))

          text5 = myfont.render('Выйти в меню', False, (0, 0, 0))
          screen.blit(text5, (self.button_menu))

      # размер
      def set_size(self, left, top, cell_size):
          self.left = left
          self.top = top
          self.cell_size = cell_size
  
      # поле
      def render(self, screen):
          #self.draw_pole()
          for y in range(self.height):
              for x in range(self.width):
                  pygame.draw.rect(
                      screen, (255, 255, 255),
                      (self.left + x * self.cell_size, self.top +
                       y * self.cell_size, self.cell_size, self.cell_size), 1)
          '''
          for unit in self.units:
  
              screen.fill(unit.color,(self.left+unit.x * self.cell_size+unit.size//2,self.top+unit.y * self.cell_size+unit.size//2,unit.size,unit.size))
  
          '''
          #self.erase_transp()
          #self.draw_pole()
          self.create_base()
          
          all_sprites.draw(screen)
          self.draw_money()
          self.draw_dots()
          self.draw_hp()
          self.count_income()
          self.draw_income()
          
         
          #screen.blit(self.transp,(0,0))
  
      # проверяет находится ли x и y внутри поля с клетками и если да, возвращает номер клетки
      def find_cell(self, x, y):
          if x > self.left + self.width * self.cell_size or x < self.left or y > self.top + self.cell_size * self.height:
              return False
          p_x = (x - self.left) // self.cell_size
          p_y = (y - self.top) // self.cell_size
          return (p_x, p_y)
  
      # добавляем юнит
      def add_unit(self, unit):
          if not self.board[unit.x][unit.y]:
              #unit.x = x
              #unit.y = y
              # self.units.append(unit)
              self.board[unit.x][unit.y] = unit
              self.create_sprite(unit, unit.x, unit.y)
  
              # print(self.board)
  
      # создаем спрайт
      def create_sprite(self, unit, x, y):
  
          unit.sprite = pygame.sprite.Sprite()
  
          unit.sprite.image = unit.image
          unit.sprite.rect = unit.sprite.image.get_rect()
          unit.sprite.rect.x = x * self.cell_size + self.cell_size // 2.5
          unit.sprite.rect.y = y * self.cell_size + self.cell_size // 2.5
          # print(unit.sprite.rect.x,unit.sprite.rect.y,x,y)
          self.draw_sprites()
  
      # рисуем спрайты
      def draw_sprites(self):
          all_sprites.empty()
          # print(all_sprites.sprites())
          for x in range(self.width):
              for y in range(self.height):
                  if self.board[x][y] != 0:
                      unit = self.board[x][y]
                      all_sprites.add(unit.sprite)
                      # print(x,y)
          # print(all_sprites.sprites())
          all_sprites.draw(screen)
          #self.effects_sprites.draw(screen)
  
      # режимы
      def show_moves(self, x, y):
          # print(self.board)
          if self.board[x][y] == 0:
              pass
          elif self.board[x][y].player != self.turn:
              pass
          elif self.board[x][y].can_move == 0:
              pass
          else:
              self.show_m = 1
              self.unit_move = (x, y, self.board[x][y].move)
              x, y = self.board[x][y].x, self.board[x][y].y
              move = self.board[x][y].move
  
              for i in range(x - move, x + move + 1):
                  for j in range(y - move, y + move + 1):
                      if 0 <= i < self.width and 0 <= j < self.height:
                          self.fill_cell(i, j, "yellow")
  
      def show_fire(self, x, y):
          # print(self.board)
          if self.board[x][y] == 0:
              pass
          elif self.board[x][y].player != self.turn:
              pass
          elif self.board[x][y].can_move == 0:
              pass
          else:
              self.show_f = 1
              self.unit_fire = (x, y, self.board[x][y].fire)
              x, y = self.board[x][y].x, self.board[x][y].y
              fire = self.board[x][y].fire
  
              for i in range(x - fire, x + fire + 1):
                  for j in range(y - fire, y + fire + 1):
                      if 0 <= i < self.width and 0 <= j < self.height:
                          self.fill_cell(i, j, "red")
  
      def fill_cell(self, x, y, color):
          screen.fill(color,
                      (self.left + x * self.cell_size, self.top +
                       y * self.cell_size, self.cell_size, self.cell_size))
  
      def fill_cell_transp(self, x, y, color):
          self.transp.fill(color,
                           (self.left + x * self.cell_size, self.top +
                            y * self.cell_size, self.cell_size, self.cell_size))
  
      def move_unit(self, x, y):
          x1, y1, move = self.unit_move
          unit = self.board[x1][y1]
          if unit.can_move:
              if self.board[x][y] == 0:
                  if abs(x - x1) <= move and abs(y - y1) <= move:
                      # print("aaaa")
                      # print(self.board)
                      unit.sprite.rect.x = x * self.cell_size + self.cell_size // 2.5
                      unit.sprite.rect.y = y * self.cell_size + self.cell_size // 2.5
                      unit.x = x
                      unit.y = y
                      self.board[x][y] = unit
                      self.board[x1][y1] = 0
                      # print(self.board)
                      self.hide_moves()
                      self.draw_sprites()
                      self.board[x][y].can_move = 0
                      self.draw_dots()
                      self.check_victory()
                      
                      
  
                  else:
                      self.hide_moves()
  
              else:
                  self.hide_moves()
  
      def fire_unit(self, x, y):
          x1, y1, fire = self.unit_fire
          unit = self.board[x1][y1]
  
          if unit.can_move:
              if self.board[x][y] != 0:
                  if abs(x - x1) <= fire and abs(y - y1) <= fire:
                      self.board[x][y].hp -= unit.attack
                      if self.board[x][y].hp <= 0:
                          self.board[x][y] = 0
                          self.draw_sprites()
  
                      # print("aaaa")
                      # print(self.board)
  
                      # print(self.board)
                      self.sound_shot.play(maxtime=300)
                      self.hide_moves()
                      self.draw_fire(x,y)
                   
                      
                      #self.draw_sprites()
                      self.board[x1][y1].can_move = 0
                      self.draw_dots()
                      
  
                  else:
                      self.hide_moves()
  
              else:
                  self.hide_moves()
      def draw_fire(self,x,y):
        self.fire_sprite.rect.x =x * self.cell_size + self.cell_size // 2.5
        self.fire_sprite.rect.y =y * self.cell_size + self.cell_size // 2.5 
          
        all_sprites.add(self.fire_sprite)
       
        all_sprites.draw(screen)
       
        self.fire_start=pygame.time.get_ticks()
      
  
        
        
        
        
       
     
  
      def hide_fire(self):
          if pygame.time.get_ticks()-self.fire_start>150:
              all_sprites.remove(self.fire_sprite)
              self.draw_pole()
              self.render(screen)
              self.fire_start=10**10
              
         
  
          
          
      
  
      def hide_moves(self):
          self.show_m = 0
          self.place_m = 0
          self.show_f = 0
          self.unit_move = 0
          for i in range(self.width):
              for j in range(self.height):
                  self.fill_cell(i, j, "black")
          self.draw_pole()
  
      def check_button(self, x, y, rect):
          if rect[0] + rect[2] > x > rect[0] and rect[1] + rect[3] > y > rect[1]:
              return True
          else:
              return False
  
      def buy(self, unit):
  
          if self.turn == 0:
              money = self.money1
          else:
              money = self.money2
          if unit == 1:
              price = self.tank_price
  
          elif unit == 2:
              price = self.sold_price
          elif unit == 3:
              price = self.supertank_price
          elif unit == 4:
              #цена нового юнита
  
              pass
  
          if money >= price:
              if self.turn == 0:
                  self.money1 -= price
              else:
                  self.money2 -= price
              self.place_m = unit
              for x in range(self.width):
                  if self.turn == 0:
                      for y in range(self.height - 2, self.height):
                          self.fill_cell(x, y, "green")
                  else:
                      for y in range(0, 2):
                          self.fill_cell(x, y, "green")
  
          else:
              pass
              # когда нет денег
  
      def change_turn(self):
          for x in range(len(self.board)):
              for y in range(len(self.board[x])):
                  if self.board[x][y] != 0:
                      if self.board[x][y].player != self.turn:
                          self.board[x][y].can_move = 1
          
   
  
          if self.turn == 0:
              self.money1 += self.income1
              self.turn = 1
          else:
              self.money2 += self.income2
              self.turn = 0
  
          self.draw_dots()
  
          self.screen.fill((43, 0, 61), (*self.text_xy, 250, 40))
          if self.turn == 1:
              text = myfont.render('Ход испанцев', False, (0, 0, 255))
          else:
              text = myfont.render('Ход англичан', False, (255, 0, 0))
          screen.blit(text, (self.text_xy))
          '''
          for x in range(len(self.board)):
              for y in range(len(self.board[x])):
                  if self.board[x][y] != 0:
                    unit=self.board[x][y]
                    print("x",unit.x,"y",unit.y,"type",unit.type,"can",unit.can_move,"player",unit.player,"turn",self.turn)
          '''
  
      def check_place(self, x, y):
          # print(x,y,self.turn)
          if self.turn == 1:
              if y < 2:
                  return True
          else:
              if y >= self.height - 2:
                  return True
          return False
  
      def draw_money(self):
          self.screen.fill((43, 0, 61), (*self.money_xy, 200, 40))
  
          if self.turn == 1:
              money = self.money2
              color = "blue"
          else:
              money = self.money1
              color = "red"
          text = myfont.render('Денег: ' + str(money), False, color)
  
          screen.blit(text, (self.money_xy))
  
      def draw_dots(self):
          for x in range(len(self.board)):
              for y in range(len(self.board[x])):
                  if self.board[x][y] != 0:
                      if self.board[x][y].can_move:
                          color = "green"
                      else:
                          color = "red"
                      if self.board[x][y].player == self.turn:
                          # print("aaaa")
  
                          self.screen.fill(
                              color, (self.left + x * self.cell_size +
                                      self.cell_size // 3, self.top +
                                      y * self.cell_size + self.cell_size // 3,
                                      self.cell_size // 5, self.cell_size // 5))
  
      def draw_hp(self):
          for x in range(len(self.board)):
              for y in range(len(self.board[x])):
                  unit = self.board[x][y]
  
                  if unit != 0:
                      hp = unit.hp / unit.maxhp
                      if hp >= 0.7:
                          color = "green"
                      elif 0.3 < hp < 0.7:
                          color = "yellow"
                      else:
                          color = "red"
                      # color=(int(255-hp*255),int(255*hp),0)
                      self.screen.fill(
                          color,
                          (self.left + x * self.cell_size + self.cell_size // 10,
                           self.top + y * self.cell_size,
                           int((self.cell_size // 1.2) * hp),
                           self.cell_size // 5))
  
  
  class Unit:
      def __init__(self, x, y, turn,can_move=1,has_hp=0):
          self.x = x
          self.y = y
  
          self.sprite = 0
          self.player = turn
          #print(board.turn,turn)
          self.can_move = can_move
          self.has_hp=has_hp
          
            
          
  
  
  class Tank(Unit):
      def __init__(self, x, y, turn,can_move=1,has_hp=0):
          super().__init__(x, y, turn,can_move=1,has_hp=0)
          self.x = x
          self.y = y
          self.type = 1
          if self.player == 1:
              self.image = pygame.image.load("blue_shot_0.png")
              self.image = pygame.transform.scale(self.image, (40, 40))
          else:
              self.image = pygame.image.load("red_shot_0.png")
              self.image = pygame.transform.scale(self.image, (40, 40))
  
          self.move = 1
          self.fire = 2
          self.income = 0
          self.maxhp = 400
          if has_hp:
            self.hp=has_hp
            #print("hp1",self.hp)
          else:
            self.hp = 400
            #print("hp2",self.hp)
          self.attack = 200
          self.price = 500
  
  
  class Soldier(Unit):
      def __init__(self, x, y, turn,can_move=1,has_hp=0):
          super().__init__(x, y, turn,can_move=1,has_hp=0)
          self.x = x
          self.y = y
          self.type = 2
          if self.player == 1:
              self.image = pygame.image.load("soldier_blue_0.png")
              self.image = pygame.transform.scale(self.image, (20, 40))
          else:
              self.image = pygame.image.load("soldier_red_0.png")
              self.image = pygame.transform.scale(self.image, (20, 40))
  
          self.move = 3
          self.fire = 1
          self.income = 0
          self.maxhp = 100
          if not self.has_hp:
            self.hp = 100
          self.attack = 100
          self.price = 200
  
  
  class Trak(Unit):
      def __init__(self, x, y, turn,can_move=1,has_hp=0):
          super().__init__(x, y, turn,can_move=1,has_hp=0)
          self.x = x
          self.y = y
          self.type = 3
          if self.player == 1:
              self.image = pygame.image.load("tractor_blue_0.png")
              self.image = pygame.transform.scale(self.image, (40, 40))
          else:
              self.image = pygame.image.load("tractor_red_0.png")
              self.image = pygame.transform.scale(self.image, (40, 40))
  
          self.move = 1
          self.fire = 0
          self.income = 1
          self.maxhp = 200
          if not self.has_hp:
            self.hp = 200
          self.attack = 0
          self.price = 100
  
  
  
  #if __name__ == '__main__':

  pygame.init()
  pygame.font.init()
  myfont = pygame.font.SysFont('Comic Sans MS', 30)

  fps = 30
  size = h, w = 900, 700
  screen = pygame.display.set_mode(size)
  screen.fill((43, 0, 61))

  pygame.display.set_caption('Операция ВОРОН')
  # pygame.display.set_mode((300, 300), pygame.FULLSCREEN)
  all_sprites = pygame.sprite.Group()
  board = Board(11, 12, screen)
  # board.add_unit(Soldier(4,3,(255,0,0),15))
  # board.add_unit(Tank(2,1,"blue",15))
  # board.add_unit(Soldier(1,1,"yellow",15))

  all_sprites.draw(screen)

  board.render(screen)

  clock = pygame.time.Clock()

  running = True
  while running:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False
          if event.type == pygame.MOUSEBUTTONDOWN:
              xp, yp = event.pos[0], event.pos[1]
              if board.find_cell(xp, yp):
                  x, y = board.find_cell(xp, yp)

                  if event.button == 3:
                      if board.show_m:
                          board.hide_moves()
                      elif board.show_f:
                          board.hide_moves()

                      elif board.show_f == 0:
                          board.show_fire(x, y)
                  elif event.button == 1:
                      if board.show_m:
                          board.move_unit(x, y)
                      elif board.show_f:
                          board.fire_unit(x, y)
                      elif board.place_m:
                          if board.check_place(x, y):
                              if board.place_m == 1:

                                  board.add_unit(Tank(x, y, board.turn))
                              elif board.place_m == 2:
                                  board.add_unit(Soldier(x, y, board.turn))
                              elif board.place_m == 3:
                                  board.add_unit(Trak(x, y, board.turn))
                                  # другие юниты
                              board.hide_moves()

                      else:

                          board.show_moves(x, y)
              else:

                  if board.check_button(xp, yp, board.button_tank):
                      board.buy(1)
                  elif board.check_button(xp, yp, board.button_turn):
                      board.change_turn()
                  elif board.check_button(xp, yp, board.button_sold):
                      board.buy(2)
                  elif board.check_button(xp, yp, board.button_supertank):
                      board.buy(3)
                  elif board.check_button(xp, yp, board.button_save):
                      board.save()
                  elif board.check_button(xp, yp, board.button_menu):
                      start.start_window()

                  # проверка нажатия кнопок и покупки юнитов

              board.render(screen)
      board.hide_fire()
          #     print(board.find_cell(event.pos[0], event.pos[1]))

      clock.tick(fps)
      pygame.display.flip()
  pygame.quit()

#game(1)
