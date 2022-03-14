import pygame
import start
import game

          
def victory(player):

    
    def vic(player):   
        # если победил синий
        if player==1:

            img_vic=pygame.image.load('red_win.jpeg')
            img_vic=pygame.transform.scale(img_vic, size)
            screen.blit(img_vic,(0, 0))
        
        else:
            img_vic=pygame.image.load('blue_win.jpeg')
            img_vic=pygame.transform.scale(img_vic, size)
            screen.blit(img_vic,(0, 0))

    pygame.init()
    pygame.font.init()
    size=(900, 700)
    screen = pygame.display.set_mode(size)
    back_but=(300,600,280,60)
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    
    running = True
    vic(player)
    text1 = myfont.render('Вернуться в меню', False, (255, 255, 0))
    back=pygame.draw.rect(screen,(83, 90, 0),back_but)
    
    screen.blit(text1, (310,600))
    pygame.display.flip()
    while running:
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
              running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back.collidepoint(mouse_pos):                        
                              
                    start.start_window()

           
   
   
 
