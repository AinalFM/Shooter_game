from pygame import *
from random import randint
from time import time as timer

# Ukuran layar
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Galaxy Game')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

# Musik dan sound effect
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Font dan teks
font.init()
game_font = font.SysFont('Arial', 36)
win_text = game_font.render('YOU WIN!', True, (255, 255, 255))
lose_text = game_font.render('YOU LOSE!', True, (180, 0, 0))

# Clock (untuk FPS)
clock = time.Clock()

# Kelas GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Kelas Player
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

# Kelas Bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
# Kelas Enemy
class Enemy(GameSprite):
    def update(self):
        global lost, finish
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
            if lost >= max_lost:
                finish = True

# Buat objek Player, sprite grup enemy, bullet dan asteroid
player = Player('rocket.png', 5, 400, 65, 65, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()

#creating a group of asteroid sprites ()
asteroids = sprite.Group()
for i in range(1, 4):
   asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 3))
   asteroids.add(asteroid)

# Variabel game
score = 0 # variabel utk menampung skor
goal = 10 # variabel sebagai batas skor maksimal
max_lost = 3 # variabel sebagai batas lost maksimal
finish = False # variabel untuk menentukan kondisi akhir menang/kalah
game = True # variabel untuk menentukan keberlangsungan game
num_fire = 0 # variabel untuk menampung jumlah tembakan yang terjadi
rel_time = False # varibel untuk reload bullet setelah 5 tembakan terjadi
life = 3 # variabel nyawa
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # cek sudah berapa tembakan yang terjadi
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    player.fire()
                    fire_sound.play()
                if num_fire >= 5 and rel_time == False :
                    last_time = timer() #record time when this happened
                    rel_time = True #set the reload flag
    if not finish:
        window.blit(background, (0, 0)) # tempel background ke layar
        # gambar & update pergerakan spritenya
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        # terapkan reload timenya
        if rel_time == True:
            now_time = timer() #read time
            if now_time - last_time < 3: #before 3 seconds are over, display reload message
                reload = game_font.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   #set the bullets counter to zero
                rel_time = False #reset the reload flag
        # Deteksi tabrakan bullet & enemy
        hits = sprite.groupcollide(monsters, bullets, True, True)
        for hit in hits:
            score += 1 # tingkatkan variabel score dengan 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2)) # buat monster baru
            monsters.add(monster) # tambahkan ke group sprite monsters
        # Deteksi tabrakan player & ufo dan player & asteroid
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 3))
            asteroids.add(asteroid)
            life = life - 1
        # Cek menang
        if score >= goal:
            finish = True
            window.blit(win_text, (250, 220)) # tempelkan teks menang
        # Cek kalah
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose_text, (250, 220)) # tempelkan teks kalah
        # Tampilkan tulisan score, missed, dan life
        text_score = game_font.render("Score: " + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 20))
        text_lost = game_font.render("Missed: " + str(lost), True, (255, 255, 255))
        window.blit(text_lost, (10, 50))
        text_life = game_font.render("Life: " + str(life), True, (0,255,0))
        window.blit(text_life, (600, 20))
        display.update()
    clock.tick(60)