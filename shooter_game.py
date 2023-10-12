#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost +=1

class Bullet(GameSprite):
    #движение врагов
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#Персонажи игры:
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

game = True
finish = False
clock = time.Clock()
FPS = 60

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

score = 0 #сбитые корабли
lost = 0 #пропущенные корабли

#группа спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1,3))
    monsters.add(monster)

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)

#группа спрайтов-пуль
bullets = sprite.Group()

#группа спрайтов-астероиды
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(80, win_width-80), -40, 80, 50, randint(1,3))
    asteroids.add(asteroid)

num_fire = 0
rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #сколько выстрелов сделано
                if num_fire < 5 and rel_time == False:
                    num_fire+=1
                    fire_sound.play()
                    ship.fire()
                #если сделали 5 выстрелов
                if num_fire >= 5 and rel_time == False:
                    time_n1 = timer()#засекаем время
                    rel_time = True #флаг перезарядки
            
    
    if finish != True:
        window.blit(background,(0, 0))

        text_lose = font1.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text_lose, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)

        for c in sprites_list:
            score+=1
            monster = Enemy('ufo.png', randint(80, win_width-80), -40, 80, 50, randint(1,3))
            monsters.add(monster)

        #проигрыш
        if sprite.spritecollide(ship, monsters, False) or lost >=3:
            finish = True
            text_pro = font1.render('OX', True, (255, 255, 255))
            window.blit(text_pro, (200, 200))
        
        #выигрыш
        if score >= 11:
            finish = True
            text_win = font1.render('Ураа!', True, (255, 255, 255))
            window.blit(text_win, (200, 200))

        #перезарядка
        if rel_time == True:
            time_n2 = timer()
            if time_n2 - time_n1 < 2:
                text_pere = font1.render('Wait, reload...', True, (255, 255, 255))
                window.blit(text_pere, (200, 200))
            else:
                num_fire = 0
                rel_time = False

        ship.update() 
        monsters.update()
        bullets.update()
        asteroids.update()
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        
    display.update()
    clock.tick(FPS)

'''
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
       if keys[K_UP] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_DOWN] and self.rect.y < win_height - 80:
           self.rect.y += self.speed

#класс-наследник для спрайта-врага (перемещается сам)
class Enemy(GameSprite):
   direction = "left"
   def update(self):
       if self.rect.x <= 470:
           self.direction = "right"
       if self.rect.x >= win_width - 85:
           self.direction = "left"

       if self.direction == "left":
           self.rect.x -= self.speed
       else:
           self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1 
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        #картинка стены
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        #хранение свой-ва rect - прямоугольник
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Надпись
font.init()
font = font.Font(None, 70)
win = font.render('ПОБЕДА!', True, (153, 18, 6))
lose = font.render('ЭХ...!', True, (153, 70, 6))

'''