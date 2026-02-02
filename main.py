import os
from this import s

import pygame
import random
import time
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

s = 'sound'

WIDTH = 480
HEIGHT = 525
FPS = 60

global lazer

lazer = pygame.mixer.Sound(os.path.join(s, 'lazer7.mp3'))
lazer.set_volume(1.0)   # max volume

global death
death = pygame.mixer.Sound(os.path.join(s, 'mi_explosion_03_hpx.mp3'))
death.set_volume(0.7)

global background_
pygame.mixer.music.load(os.path.join(s, 'bensound-summer_mp3_music.mp3'))
pygame.mixer.music.set_volume(0.25)

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ignore = (255, 255, 0)

# initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space!")
clock = pygame.time.Clock()

# draw text
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Space wars!", 32, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Use, W, A, S, and D, or arrow keys to move, Space to fire,", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press any key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# images
background = pygame.image.load("starfield2.png").convert()
background_rect = background.get_rect()

player_img = pygame.image.load("PixelArt (1).png").convert()
laser_img = pygame.image.load("New Piskel (8).gif").convert()
meteor_img = pygame.image.load("New Piskel (7).gif").convert()
medic = pygame.image.load("New Piskel (9).gif").convert()

meteor_images = []
meteor_list = ["New Piskel (7).gif", "New Piskel (6).gif", "New Piskel.gif"]

for img in meteor_list:
    meteor_img = pygame.image.load(img).convert()
    meteor_images.append(meteor_img)

# resize
meteor_img = pygame.transform.scale(meteor_img, (40, 40))
player_img = pygame.transform.scale(player_img, (50, 50))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 75

    #Initialize movement

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -8

        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 8

        self.rect.x += self.speedx


        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0



    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(ignore)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser_img

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Medic(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield'])
        self.image = medic
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of the screen
        if self.rect.top > HEIGHT:
            self.kill()


# Game loop
game_over = True
running = True
while running:

    if game_over:
        show_go_screen()
        game_over = False
        pygame.mixer.music.play(-1)
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                pygame.mixer.Sound.play(lazer)

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        pygame.mixer.Sound.play(death)
        if random.random() > 0.9:
            med = Medic(hit.rect.center)
            all_sprites.add(med)
            powerups.add(med)
        newmob()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True)
    for hit in hits:
        player.shield -= hit.radius * 2
        newmob()
        if player.shield <= 0:
            running = False

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            player.shield += random.randrange(5, 20)
            if player.shield >= 100:
                player.shield = 100

    if player.shield == 0:
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    # *after* drawing everything, flip the display
    pygame.display.flip()


pygame.quit()