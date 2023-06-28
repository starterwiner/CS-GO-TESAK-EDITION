from typing import Any
from pygame import *


window = display.set_mode((400, 500))
display.set_caption("CS:GO TESAK EDITION")

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self,pl_image, pl_x, pl_y, size_x, size_y, pl_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image),(size_x, size_y))
        self.speed = pl_speed
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(GameSprite):
    def update (self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 680:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 5 :
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 14, 20, -15)
        bullets.add(bullet)


from random import*
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x  = randint(0,4)
            self.rect.y = 0 
            lost += 1
             
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



background = transform.scale(image.load("galaxy.jpg"),(400, 500))
ship = Player("rocket.png", 100, 300, 80, 100, 10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("asteroid.png", randint(0,450),-40, 50, 50, randint(1,5))
    monsters.add(monster)

#monsters = sprite.Group()
#for i in range(1,6):
#    monster = Enemy("ufo.png", randint(0,450),-40, 50, 50, randint(1,5))
#    monsters.add(monster)    

bullets = sprite.Group()


finish = False
import sys



font.init()
mainfont = font.Font(None, 20)

lose = mainfont.render("U LUSE!", True, (255,255,255))
win = mainfont.render("U WIN!", True, (0,255,0))

score = 0 
lost = 0 
max_lost = 3



while True:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()


    if not finish:
        window.blit(background,(0,0))
        text_rakh = mainfont.render("Рахунок:"+str(lost), True,(255,255,255))
        text_skip = mainfont.render("Пропущені:"+str(lost), True,(255,255,255))
        window.blit(text_rakh,(10,10))
        window.blit(text_skip,(10,30))

        ship.update()      
        monsters.update()
        bullets.update()

        ship.draw()
        bullets.draw(window)
        monsters.draw(window)

        collides = sprite.groupcollide(monsters,bullets, True,True)
        for c in collides:
            score +=1 
            monster = Enemy("asteroid.png", randint(0,450),-40, 50, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost > max_lost:
            finish = True
            window.blit(lose, (200,250))
        if score >= 10:
            finish = True
            window.blit(win, (200,250))


    display.update()
    time.delay(50)








