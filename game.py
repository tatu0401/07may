import pygame
import random
pygame.init()

C_W=800
C_H=600

screen=pygame.display.set_mode((C_W,C_H))
pygame.display.set_caption("name display")#название окошка


#загрузка изображений
menu=pygame.image.load("menu.jpeg")
game=pygame.image.load("game.jpeg")
win=pygame.image.load("win.jpeg")
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0,255,255)
player_image=pygame.image.load("player.png").convert_alpha()
bullet_image=pygame.image.load("fire.png").convert_alpha()
enemy_image= ['enemy1.png','enemy2.png','enemy3.png']

#загрузка музыки
'''mus='bg_mus.mp3'
pygame.mixer.music.load(mus)
pygame.mixer.music.play(-1)'''

#текст
font=pygame.font.Font("buse.otf",40)
title=font.render("Космический бой",True,WHITE)
title_rect=title.get_rect(center=(C_W//2,100))
q_title=font.render("Игра окончена",True,WHITE)
q_title_rect=q_title.get_rect(center=(C_W//2,100))
w_title=font.render("ПОБЕДА",True,WHITE)
w_title_rect=w_title.get_rect(center=(C_W//2,100))
s_button=font.render("Старт",True,WHITE)
s_rect=s_button.get_rect(center=(C_W//2,180))
q_button=font.render("Выход",True,WHITE)
q_rect=q_button.get_rect(center=(C_W//2,260))

#класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=player_image
        self.rect=self.image.get_rect(center=(200,400))
        self.speed=5

    def update(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x-=self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x+=self.speed
        if keys[pygame.K_UP]:
            self.rect.y-=self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y+=self.speed

        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>C_W:
            self.rect.right=C_W
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>C_H:
            self.rect.bottom=C_H

    def fire(self):
        bullet=Bullet(self.rect.midtop)
        bullets.add(bullet)
            

#класс враг
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img_idx=random.randint(0,len(enemy_image)-1)
        self.image=pygame.image.load(enemy_image[img_idx]).convert_alpha()
        self.rect=self.image.get_rect(center=(random.randint(50, C_W-50),-50))
        self.speed=random.uniform(1,3)

    def update(self):
        self.rect.y+=self.speed
        if self.rect.top>C_H:
            self.kill()

#класс пуля

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect(center=pos)
        self.speed=-10

    def update(self):
        self.rect.y+=self.speed
        if self.rect.bottom<0:
            self.kill
        
    
players=pygame.sprite.GroupSingle()
enemies=pygame.sprite.Group()
bullets=pygame.sprite.Group()

player=Player()
players.add(player)

SPAWN_ENEMY_EVENT=pygame.USEREVENT+1
pygame.time.set_timer(SPAWN_ENEMY_EVENT,1000)

running=True
clock=pygame.time.Clock()
game_state="main_menu"

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            pygame.quit()

    if game_state=="main_menu":
        screen.fill(BLACK)
        screen.blit(menu,(0,0))
        screen.blit(title,title_rect)
        screen.blit(s_button,s_rect)
        screen.blit(q_button,q_rect)
        if event.type==pygame.MOUSEBUTTONDOWN:
            s_click=s_rect.collidepoint(pygame.mouse.get_pos())
            if s_click==1:
                game_state="game"
                life=3
                score=0
            q_click=q_rect.collidepoint(pygame.mouse.get_pos())
            if q_click==1:
                running=False
                
    elif game_state=="game_over":
        screen.fill(BLACK)
        screen.blit(win,(0,0))
        screen.blit(q_title,title_rect)
        screen.blit(s_button,s_rect)
        screen.blit(q_button,q_rect)
        if event.type==pygame.MOUSEBUTTONDOWN:
            s_click=s_rect.collidepoint(pygame.mouse.get_pos())
            if s_click==1:
                game_state="game"
                life=3
                score=0
            q_click=q_rect.collidepoint(pygame.mouse.get_pos())
            if q_click==1:
                running=False

    elif game_state=="game_win":
        screen.fill(BLACK)
        screen.blit(win,(0,0))
        screen.blit(w_title,title_rect)
        screen.blit(s_button,s_rect)
        screen.blit(q_button,q_rect)
        if event.type==pygame.MOUSEBUTTONDOWN:
            s_click=s_rect.collidepoint(pygame.mouse.get_pos())
            if s_click==1:
                game_state="game"
                life=3
                score=0
            q_click=q_rect.collidepoint(pygame.mouse.get_pos())
            if q_click==1:
                running=False

    elif game_state=="game":
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == SPAWN_ENEMY_EVENT:
                enemies.add(Enemy())
                pygame.sprite.RenderPlain(enemies)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    player.fire()
                elif event.key==pygame.K_q:
                    game_state="main_menu"

        collisions=pygame.sprite.spritecollide(player,enemies,True)
        if collisions:
            life-=1
            if life==0:
                game_state="game_over"
        hits=pygame.sprite.groupcollide(bullets,enemies,True,True)
        score+=5*len(hits)
        if score==50:
            game_state="game_win"
            


        screen.fill(BLACK)
        screen.blit(game,(0,0))
        enemies.draw(screen)
        players.draw(screen)
        bullets.draw(screen)
        enemies.update()
        players.update()
        bullets.update()

        font=pygame.font.Font("buse.otf",30)
        score_txt=font.render(f"Счет: {score}",True,BLUE)
        life_txt=font.render(f"Жизнь: {life}",True,BLUE)
        text=font.render("Для выхода нажмите в главное меню Q",True,BLUE)
        screen.blit(score_txt,(10,10))
        screen.blit(life_txt,(10,50))
        screen.blit(text,(150,550))
                
                




    pygame.display.flip()

pygame.quit()
    
    
            











