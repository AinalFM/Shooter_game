#hubungkan module pygame
from pygame import *
from random import randint
from time import time as timer # import fungsi untuk menghitung waktu

# buat objek window, captionnya, background
window = display.set_mode((700,500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))


# hubungkan backsound
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

# hubungkan sound effect
fire = mixer.Sound('fire.ogg')


# buat objek time utk atur besaran FPS
clock = time.Clock()
FPS = 60

# buat objek font
font.init()
font = font.SysFont('Arial', 36)

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

# buat sprite grup utk objek monster dari kelas Enemy
monsters = sprite.Group()
for i in range(1, 6): # loopingnya berulang 5 kali karena pengen bikin 5 ufo
   monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

# buat sprite grup untuk objek Asteroid dari kelas Enemy
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

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
goal = 10 # nilai maksimum scorenya
lost = 0
max_lost = 3 # nilai maksimum utk lostnya
num_fire = 0 # variabel yg menghitung jumlah tembakan
rel_time = False # variabel yg menentukan udh masuk fase reload atau belum
while run:
    for e in event.get(): # analisis event
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
            # cek sudah berapa tembakan yang terjadi
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    player.fire()
                    fire.play()
                if num_fire >= 5 and rel_time == False :
                    last_time = timer() # hitung waktu sekarang utk reloadnya nanti
                    rel_time = True # set True karena udh masuk fase reload

    if not finish: # jka gamenya belum selesai
        window.blit(background,(0, 0)) # tempelkan bg ke window
        player.reset() # tempelkan rocket ke windownya
        player.update() # tambahkan pergerakan rocket
        monsters.draw(window) # tempelkan grup ufo ke windownya
        monsters.update() # tambahkan pergerakan ufonya
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        text_missed = font.render("Missed: " + str(lost), 1, (255, 255, 255)) #  buat tulisan 'Missed' menggunakan objek font
        window.blit(text_missed, (10, 50)) # gambar tulisan ke layar
        text_score = font.render("Score: " + str(score), 1, (255, 255, 255)) #  buat tulisan 'Missed' menggunakan objek font
        window.blit(text_score, (10, 20))

        # buat kondisi utk reload timenya
        if rel_time == True:
            now_time = timer() # hitung waktu terakhir kali
            if now_time - last_time < 3: #before 3 seconds are over, display reload message
                reload = font.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   #set the bullets counter to zero
                rel_time = False #reset the reload flag

        # cek tabrakan yg terjadi antara monsters dan bullets
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # buat kondisi kalah
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            lose = font.render('YOU LOSE', True, (220, 20, 60))
            window.blit(lose, (200, 200))

        # buat kondisi menang
        if score >= goal:
            finish = True
            win = font.render('YOU WIN', True, (0, 255, 60))
            window.blit(win, (200, 200))

        display.update() # tampilannya diupdate
        clock.tick(FPS) # FPSnya dipasang

