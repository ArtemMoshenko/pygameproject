import pygame
import game

def start_window():
  pygame.init()
  
  size = h, w = 900, 700
  screen = pygame.display.set_mode(size)

  start_but=(300,600,200,60)
  load_but=(550,600,200,60)
  
  myfont = pygame.font.SysFont('Comic Sans MS', 30)
  #button_sound=pygame.mixer.Sound('music.mpeg')
  
  all_sprites = pygame.sprite.Group()

  wallpaper_img=pygame.image.load("wallpaper.png")
  wallpaper_img=pygame.transform.scale(wallpaper_img, size)
  wall_sprite=pygame.sprite.Sprite()
  wall_sprite.image=wallpaper_img
  wall_sprite.rect=wallpaper_img.get_rect()
  wall_sprite.rect.x=0
  wall_sprite.rect.y=0
  all_sprites.add(wall_sprite)
  all_sprites.draw(screen)
  start=pygame.draw.rect(screen,(83, 90, 0),start_but)
  load=pygame.draw.rect(screen,(83, 90, 0),load_but)
  text1 = myfont.render('Начать игру', False, (255, 255, 0))
  screen.blit(text1, (310,600))
  text2 = myfont.render('Продолжить', False, (255, 255, 0))
  screen.blit(text2, (560,600))
  pygame.display.set_caption('Операция ВОРОН')
  
  pygame.display.flip()


  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
              running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        if start.collidepoint(mouse_pos):
          #button_sound.play()
          game.game(0)
        elif load.collidepoint(mouse_pos):
          game.game(1)
