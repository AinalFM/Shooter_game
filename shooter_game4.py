#hubungkan module pygame
from pygame import *
from random import randint


# buat objek window, captionnya, background
window = display.set_mode((700,500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))


# hubungkan backsound
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

# buat objek time utk atur besaran FPS
clock = time.Clock()
FPS = 60


# buat objek font
font.init()
font = font.Font(None, 36)


# buat kelas Gamesprite dan Player
# buat kelas Gamesprite
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# buat kelas player
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self): # fungsi utk melontarkan peluru
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

from random import randint
lost = 0 # variabel lost -> utk menghitung jumlah UFO yang udh jatuh ke bawah/terlewat
# buat kelas enemy
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y = self.rect.y + self.speed # update pergerakan UFOnya
        if self.rect.y > 500: # tambahin kondisi utk ngecek apakah UFO udah lebih dri batas bawah
            self.rect.x = randint(80, 620) # koordinat x nya diacak
            self.rect.y = 0 # koordinat y nya direset kembali ke 0
            lost = lost + 1

# buat sprite grup utk objek dari kelas Enemy
monsters = sprite.Group()
for i in range(1, 6): # loopingnya berulang 5 kali karena pengen bikin 5 ufo
   monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

# Kelas Bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y = self.rect.y - self.speed
        if self.rect.y < 0:
            self.kill()

# buat sprite grup utk objek dari kelas Bullet
bullets = sprite.Group()

# buat objek player
player = Player('rocket.png', 5, 400, 80, 100, 10)

# buat game loopnya
finish = False
run = True
score = 0
max_lost = 3
goal = 10
while run:
    for e in event.get(): # analisis event
        if e.type == QUIT: 
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire.play()
    if not finish:
        window.blit(background,(0, 0)) # tempelkan bg ke window
        player.reset() # tempelkan rocket ke windownya
        player.update() # tambahkan pergerakan rocket
        monsters.draw(window) # tempelkan grup ufo ke windownya
        monsters.update() # tambahkan pergerakan ufonya
        bullets.draw(window)
        bullets.update()
        text_missed = font.render("Missed: " + str(lost), 1, (255, 255, 255)) #  buat tulisan 'Missed' menggunakan objek font
        window.blit(text_missed, (10, 50)) # gambar tulisan ke layar
        text_score = font.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        
        # cek tabrakan yg terjadi    
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # tiap bertabrakan, jumlah score jadi nambah 1
            # dan objek monster dibuat kembali (lahir kembali)
            score = score + 1
            monster = Enemy('ufo.png ', randint(80,  620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # kondisi kalah
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True #lose, set the background and no longer control the sprites.
            lose = font.render('YOU LOSE!', True, (180, 0, 0))
            window.blit(lose, (200, 200))

        # kondisi menang
        if score >= goal:
            finish = True
            win = font.render('YOU WIN!', True, (255, 255, 255)) 
            window.blit(win, (200, 200))


        display.update() # tampilannya diupdate
        clock.tick(FPS) # FPSnya dipasang