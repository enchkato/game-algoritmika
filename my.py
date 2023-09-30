from pygame import *
# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, size_x,size_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # Каждый спрайт должен хранить свойство image - изображения
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
 
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # Метод, отрисовывающий героя на окне
    def reset(self):
        windows.blit(self.image, (self.rect.x , self.rect.y))
 
 
 
 
# класс главного игрока
class Player(GameSprite):
    def __init__(self,player_image,player_x,player_y, size_x, size_y,player_x_speed, player_y_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self,player_image,player_x,player_y,size_x,size_y)
 
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if hero.rect.x <= win_width - 80 and hero.x_speed > 0 or hero.rect.x >= 0 and hero.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if hero.rect.y <= win_height - 80 and hero.y_speed > 0 or hero.rect.y >= 0 and hero.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top,p.rect.bottom)
    # Метод выстрел пули
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 30, 30, 15)
        bullets.add(bullet)
 
# Спрайт-врага
class Enemy(GameSprite):
    side = "left"
 
    def __init__(self, player_image: object, player_x: object, player_y: object, size_x: object, size_y: object, player_speed: object) -> object:
        # вызов класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
 
        # Движение врага
    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
 
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()
# Окошка
win_width = 700
win_height = 500
display.set_caption('РОБЛОКС')
windows = display.set_mode((win_width,win_height))
 
background_image = image.load('fon.png')
 
barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
 
platform1 = GameSprite('wall.png', win_width/2 - win_width, win_height/2, 350, 50)
platform2 = GameSprite('wall.png',380,150,50,350)
 
hero = Player('hero.png', 100, 100, 100, 100, 0, 0)
enemy = Enemy('cyborg.png', 450, 200, 80, 80, 2)
win_sprite = GameSprite('pac 1.png',590,400,70,70)
 
monsters.add(enemy)
 
barriers.add(platform1)
barriers.add(platform2)
 
lose_image = image.load('fon.png')
win_image = image.load('123.png')
 
 
clock = time.Clock()
 
run = True
while run:
    windows.blit(background_image,(0,0))
 
    hero.update()
    hero.reset()
 
    platform1.reset()
    platform2.reset()
 
    bullets.update()
    bullets.draw(windows)
 
    monsters.update()
    monsters.draw(windows)
 
    win_sprite.update()
    win_sprite.reset()
 
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                hero.x_speed = -5
            elif e.key == K_RIGHT:
                hero.x_speed = 5
            elif e.key == K_UP:
                hero.y_speed = -5
            elif e.key == K_DOWN:
                hero.y_speed = 5
            elif e.key == K_SPACE:
                hero.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                hero.x_speed = 0
            elif e.key == K_RIGHT:
                hero.x_speed = 0
            elif e.key == K_UP:
                hero.y_speed = 0
            elif e.key == K_DOWN:
                hero.y_speed = 0
 
    hits = sprite.spritecollide(hero,monsters,False)
    for enemy in hits:
        windows.blit(lose_image, (0,0))
        display.update()
        time.delay(5000)
        run = False
 
    if sprite.collide_rect(hero, win_sprite):
        windows.blit(win_image, (0, 0))
        display.update()
        time.delay(5000)
        run = False
 
 
    hits = sprite.groupcollide(monsters, bullets, True,True)
    for enemy, bullet_list in hits.items():
        enemy.kill()
 
    display.update()
    clock.tick(40)