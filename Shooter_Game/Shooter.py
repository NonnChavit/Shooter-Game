
from pygame import *

from pygame import *

import random
import time as timer
import math

window_width = 700
window_height = 900
window = display.set_mode( (window_width, window_height) )

class Character(sprite.Sprite):
    def __init__(self, filename, x, y, w, h, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(filename),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def draw (self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class UFO(Character):
    def __init__(self, filename, x, y, w, h, speed, max_hp):
        super().__init__(filename, x, y, w, h, speed)
        self.max_hp = max_hp
        self.hp = max_hp
    def update(self):
        global ufo_pass
        self.rect.y += self.speed
        if self.rect.y > 900:
            self.rect.y = 0
            self.rect.x = random.randint(50,650)
            ufo_pass += 1
    def hit(self):
        global Enemies_Killed
        self.hp -= 1
        if self.hp == 0:
            self.rect.x = random.randint(50,650)
            self.rect.y = 0
            self.hp = self.max_hp
            Enemies_Killed += 1

class Asteroid(Character):
    def __init__(self, filename, x, y, w, h, speed_x, speed_y):
        super().__init__(filename, x, y, w, h, speed)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
class Bullet(Character):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

            

player1 = Character("rocket.png", 200, 800, 50, 100, 7)

bullet_group = sprite.Group()
asteroid_group = sprite.Group()

bg = transform.scale(image.load("galaxy.jpg"), (window_width, window_height))
ufo_group = sprite.Group()
for i in range (3):
    x = random.randint(50,650)
    speed = random.randint(2,8)
    ufo = UFO("ufo.png", x, 0, 50, 50, speed, 3)
    ufo_group.add(ufo)
    




game = True
finish = False
fps = 45
clock = time.Clock()
last_fire_time = timer.time()
hp = 10
ufo_pass = 0
bullets_size = 40
bullets_remain = bullets_size
font.init()
Enemies_Killed = 0
style = font.SysFont(None, 36)
blink_count = 0
game_win = True
generate_boss = True
asteroid_time = timer.time()
while game:
    window.blit(bg,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish ==  False:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and player1.rect.x < 615:
            player1.rect.x += player1.speed
        if keys_pressed[K_a] and player1.rect.x > 0:
            player1.rect.x -= player1.speed
        if keys_pressed[K_SPACE] and timer.time()-last_fire_time > 0.1 and bullets_remain > 0:
            print("FIRE!!!")
            bullet = Bullet("bullet.png", player1.rect.x, 900, 20, 45, 5)
            bullet_group.add(bullet)
            last_fire_time = timer.time()
            bullets_remain -= 1
        if (bullets_remain <= 0):
            if (timer.time()-last_fire_time > 2):
                bullets_remain = bullets_size
            else: 
                if (blink_count < 20):
                    text_reloading = style.render("RELOADING ", 1, (255, 255, 255))
                    blink_count += 1
                elif (blink_count < 40):
                    text_reloading = style.render(" ", 1, (255, 255, 255))
                    blink_count += 1
                else:
                    blink_count = 0
                window.blit(text_reloading, (400, 400))
            
        if (timer.time()-asteroid_time >= 2):
            x = random.randint(50,650)
            speed_x = random.choice((-1,1))
            speed_y = 5
            asteroid = Asteroid("asteroid.png", x, 0, 50, 50, speed_x, speed_y)
            asteroid_group.add(asteroid)
            asteroid_time = timer.time()

        
        collide_list = sprite.groupcollide(asteroid_group, bullet_group, True, True)
        collide_list = sprite.groupcollide(bullet_group, ufo_group, True, False)
        if len((collide_list))> 0:
            for k in collide_list.keys():
              collide_list[k][0].hit()
        collide_list = sprite.spritecollide(player1, ufo_group, True)
        if len((collide_list)) > 0:
            x = random.randint(50,650)
            speed = random.randint (2,12)
            ufo = UFO("ufo.png", x, 0, 50, 50, speed, 3)
            ufo_group.add(ufo)    
            hp -= 1 

        print(hp)
        print(Enemies_Killed)

        collide_list = sprite.spritecollide(player1, asteroid_group, True)
        if len((collide_list)) > 0:
            hp = math.floor(hp/2)
        player1.draw()

        ufo_group.update()
        ufo_group.draw(window)
        player1.draw()
        bullet_group.update()
        bullet_group.draw(window)
        asteroid_group.draw(window)
        asteroid_group.update()
    
        text_hp = style.render("HP = "+str(hp), 1, (255, 255, 255))
        window.blit(text_hp, (20,20))
        text_pass = style.render("Enemies Passed = "+str(ufo_pass), 1, (255, 255, 255))
        window.blit(text_pass, (20,50))
        text_remain = style.render("Bullets Remain = "+str(bullets_remain), 1, (255, 255, 255))
        window.blit(text_remain, (400,20))
        text_killed= style.render("Enemies Killed="+str(Enemies_Killed), 1,  (255, 255, 255))
        window.blit(text_killed, (400, 50))
        text_Lose = style.render("You Lose", 1, (255, 255, 255))
        
         

        if (hp == 0):
            print("You Lose")
            finish = True
            game_win = False
        if (Enemies_Killed == 15):
            finish = True
        if (ufo_pass >= 50):
            print("You Lose",)
            finish = True
            game_win = False
        
        
        if (Enemies_Killed % 5 == 0 and Enemies_Killed != 0):
            if generate_boss == True:
                ufo = UFO("ufo.png", 200,0,200,50,1,10)
                ufo_group.add(ufo)
                generate_boss = False
        else: 
            generate_boss = True

        
            
    else:
        if game_win == True:
            text = style.render("You Win", 1, (255, 255, 255))
        else:
            text = style.render("You Lose", 1, (255, 255, 255))
        window.blit(text, (300, 350))
      
        
    display.update()
    clock.tick(fps)


        