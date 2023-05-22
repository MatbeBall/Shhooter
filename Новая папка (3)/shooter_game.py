#Создай собственный Шутер!
from random import randint
from pygame import *
from time import time as timer

mixer.init()
font.init()
lost = 0
score = 0
bulletcounter = 0
 
finish = False
win = display.set_mode((700, 500))
class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y,speed): 
        sprite.Sprite.__init__(self) 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
        self.speed=speed
    def reset(self): 
        win.blit(self.image, (self.rect.x, self.rect.y)) 

class player(GameSprite):
    def reset1(self): 
        win.blit(self.image, (self.rect.x, self.rect.y)) 
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed
    def fire(self):
        bul1 = bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bulletgroup.add(bul1)
    
class enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(0, 650)
            self.speed = randint(1, 5)
            global lost
            lost += 1
class bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        
class asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(0, 650)
            self.speed = randint(1, 5)



font1 = font.SysFont("Arial",50)
ril_time = False

group = sprite.Group()
bulletgroup = sprite.Group()
asgroup = sprite.Group()

for i in range(5):
    enemy2 = enemy('ufo.png', randint(0, 500), 0, 100, 50, randint(1, 5))
    group.add(enemy2)


spufo = player('rocket.png', 50, 450, 50, 50, 10)
as1 = asteroid('asteroid.png',randint(0, 450), 0, 50, 50, 10)
asgroup.add(as1)


clock = time.Clock()

bg = transform.scale(image.load('galaxy.jpg'),(700,500))
mixer.music.load('space.ogg')
game = True
mixer.music.play()
b4 = font1.render('Вы Выйграли!', 20, (255,255,255))
b3 = font1.render('Проигрыш!', 20, (255,255,255))


while game:

    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if bulletcounter <= 4:
                    spufo.fire()
                    bulletcounter += 1
                elif bulletcounter >= 4:
                    ril_time = True
                    w = timer()

                
   
    
    if not finish: 
        

        b = font1.render('Счёт: '+str(score), 10, (255,255,255))
        b2 = font1.render('Попущено: '+str(lost), 10, (255,255,255))
        b5 = font1.render(str(bulletcounter), 10, (255,255,255))
        win.blit(bg, (0, 0))
        win.blit(b, (0, 0))
        win.blit(b2, (0,35))
        win.blit(b5, (650,0))
        
        sprites_list1 = sprite.spritecollide(spufo, group, True)
        sprites_list3 = sprite.spritecollide(spufo, asgroup, True)
        sprites_list2 = sprite.groupcollide(group, bulletgroup, True, True)
        
        for i in sprites_list3:
            win.blit(b3, (250,230))
            finish = True
        
        for i in sprites_list1:
            win.blit(b3, (250,230))
            finish = True

        for i in sprites_list2:
            score += 1
            enemy2 = enemy('ufo.png', randint(0, 500), 0, 100, 50, randint(1, 10))
            group.add(enemy2)

        if score == 10:
            win.blit(b4, (250,230))
            finish = True

        if lost == 10:
            win.blit(b3, (250,230))
            finish = True
        
        as1.reset()
        as1.update()   
        spufo.reset1()
        spufo.update()
        group.draw(win)
        group.update()
        bulletgroup.update()
        bulletgroup.draw(win)
        if ril_time == True:
            t = timer()
            if t-w <= 3:
                b6 = font1.render('Перезарядка!', 20, (255,255,255))
                win.blit(b6, (250,230))
            else:
                bulletcounter = 0
                ril_time = False
    
        
        display.update()
        clock.tick(60)