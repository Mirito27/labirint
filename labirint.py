from pygame import *
w = 80
h = 100
x = 80
y = 70
size_x = 80
size_y = 70
x_speed = 0
y_speed = 0

window = display.set_mode((1920, 1080))
display.set_caption("Лабирнт!!!!!")
background = transform.scale(image.load('fon.png'), (1920, 1080))


class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
wall_1 = GameSprite('wall2.png',80,180,200,200)
wall_2 = GameSprite('wall2.png',80,180,400,300)
wall_3 = GameSprite('wall2.png',80,180,400,150)
wall_4 = GameSprite('wall2.png',80,180,200,10)
final = GameSprite('dio2.png',80,100,640,250)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)
barriers.add(wall_4)

bullets = sprite.Group()



class Bullet(GameSprite):
    def __init__(self,picture,x,y,w,h, x_speed):
         super().__init__(picture,w,h,x,y)
         self.x_speed = x_speed
    def update(self):
        self.rect.x += self.x_speed
        if self.rect.x > 640:
            self.kill()



class Player(GameSprite):
    def __init__(self,picture,w,h,x,y, x_speed,y_speed):
        super().__init__(picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet)
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:     
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
player = Player('hero.png',w,h,x,y, x_speed,y_speed)



class Enemy(GameSprite):
    def __init__(self,picture,x,y,size_x,size_y,speed):
        super().__init__(picture,x,y,size_x,size_y)
        self.speed = speed
        self.side = 'right'
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= 640:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
enemy = Enemy('dio2.png',70,80,500,420, x_speed)
monsters = sprite.Group()
monsters.add(enemy)






run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYUP:
            if e.key == K_UP:
                player.y_speed = 0
            if e.key == K_RIGHT:
                player.x_speed = 0
            if e.key == K_LEFT:
                player.x_speed = 0
            if e.key == K_DOWN:
                player.y_speed = 0
            if e.key == K_SPACE:
                player.fire()
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                player.y_speed = -5
            if e.key == K_RIGHT:
                player.x_speed = 5
            if e.key == K_LEFT:
                player.x_speed = -5
            if e.key == K_DOWN:
                player.y_speed = 5
    if finish != True:
        window.blit(background, (0, 0))
        barriers.update()
        barriers.draw(window)
        player.reset()
        player.update()
        final.reset()
        enemy.reset()
        enemy.update()
        bullets.update()
        bullets.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, monsters, True, True)
        monsters.update()
        monsters.draw(window)
        if sprite.collide_rect(player, final):
            finish = True

            img = image.load('false.png')
            window.fill((255,255,255))


    display.update()











