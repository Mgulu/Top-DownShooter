# laser sound from dklon
import pygame
import random
import os
import math
import sys

# Constants
import self as self

screen_width = 1080
screen_height = 720
fps = 60
# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (128,128,128)
dimgrey = (105,105,105)
yellow = (255, 255, 0)

# initialize pygame and create window
pygame.init()
# for audio
pygame.mixer.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space invaders")
clock = pygame.time.Clock()

# sounds
shoot_sound = pygame.mixer.Sound('laser.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
pygame.mixer.music.load('music.ogg')
pygame.mixer.music.set_volume(0.4)

# powerup time
powerup_time = 15000

# Mobs spawning
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#SHield bar
def draw_shield_bar(surf,x,y,pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct/100)*bar_length
    outline_rect = pygame.Rect( x,y, bar_length, bar_height)
    fill_rect = pygame.Rect( x,y, fill ,bar_height)
    pygame.draw.rect(surf, red, fill_rect)
    pygame.draw.rect(surf,white,outline_rect,2)


# For the background
bg = pygame.image.load('bg.jpg').convert()

# class for aliens

mob_images = []
mob_list = ['ufo.gif','ufoB.gif','ufoG.gif','ufoP.gif','ufoW.gif',]
for img in mob_list:
    mob_images.append(pygame.image.load(img))

# score and time function

font_name = pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text, True,white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

# powerUps
powerup_images = {}
powerup_images['shield'] = pygame.image.load('shield.png').convert()
powerup_images['gun'] = pygame.image.load('star.png').convert()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(mob_images)
        # To make the color white transparent
        self.image.set_colorkey(black)
        self.image.set_alpha()
        self.rect = self.image.get_rect()
        self.original_image = self.image
        # circle so that it collides with the circle i give it
        self.radius = 24

        # Spawns the enemy somewhere outside the screen but away from the user
        # This needs to change enemies arent spawning away from the user, sometimes ontop of him

        self.rect.x = player.rect.x + random.randrange(-screen_width, screen_width)
        self.rect.y = player.rect.y + random.randrange(-screen_height, screen_height)
        # Vary the speed of the enemies
        self.speedy = random.randrange(2,4)

    def move_towards_player(self, player):
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = self.rect.x - player.rect.x, self.rect.y - player.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        # move along this normalized vector towards the player at current speed
        self.rect.x -= dx * self.speedy
        self.rect.y -= dy * self.speedy

    #Rotates aliens but has a problem with the intial facing direction
    #Isnt the same as the users problem as it dosent require the mouse input which is why the user rotations is off
    def rotate_alien(self, player):
        rel_x, rel_y = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        angle = math.atan2(rel_y, rel_x)
        angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.image.set_colorkey(black)
        self.image.set_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)

    # for the update part of the loop
    def update(self):
        self.rotate_alien(player)
        self.move_towards_player(player)


class Mouse(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(red)
        self.rect = self.image.get_rect()

    # Position of mouse is where the mouse is
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos




        # Class for player sprite


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Loading up the image
        self.image = pygame.image.load('ship.jpg').convert_alpha()
        self.original_image = self.image

        # To make the color white transparent
        self.image.set_colorkey(black)
        self.image.set_alpha()
        self.change_x = 0
        self.change_y = 0
        self.shield = 100
        # Delay in shooting
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()
        #powerups
        self.power = 1
        self.power_time = pygame.time.get_ticks()

        # Size of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)

        # Circle so that it collides with a circle i give it
        self.radius = 24


        # speed of sprite
        self.speedx = 0
        self.speedy = 0

    def rotate_player(self, mouse):
        rel_x, rel_y = mouse.rect.x - self.rect.x, mouse.rect.y - self.rect.y
        angle = math.atan2(rel_y, rel_x)
        angle = (180 / math.pi) * math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.image.set_colorkey(black)
        self.image.set_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)

    # Fot the update part of my loop
    def update(self):

        self.rotate_player(mouse)
        # So the sprite isnt continously moving
        self.speedx = 0
        self.speedy = 0
        # Gets all the keys currently being pressed
        keystate = pygame.key.get_pressed()
        # if the key is a
        if keystate[pygame.K_a]:
            self.speedx = -7
        if keystate[pygame.K_d]:
            self.speedx = 7
        if keystate[pygame.K_s]:
            self.speedy = 7
        if keystate[pygame.K_w]:
            self.speedy = -7
        # To make a boundary
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Timeout for powerupnn
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()




# Bullets require a seperate sprite
class Bullet(pygame.sprite.Sprite):
    # X , y in the function so we can later anchor it to the user
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y

        # This was originally going to be a function but the stuff i intialised above wouldnt show up in a fucntion so
        # i couldnt use a function
        cursor_pos_x, cursor_pos_y = pygame.mouse.get_pos()
        dx, dy = cursor_pos_x - self.rect.x, cursor_pos_y - self.rect.y
        dist = math.hypot(dx, dy)
        re_x, re_y = dx / dist, dy / dist
        # move along this normalized vector towards the player at current speed
        self.change_x += re_x * 5
        self.change_y += re_y * 5

    def update(self):

        self.rect.x += self.change_x
        self.rect.y += self.change_y
        # delete bullet if it exits away from screen
        if self.rect.right > screen_width:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom > screen_height:
            self.kill()

class Pow(pygame.sprite.Sprite):
# X , y in the function so we can later anchor it to the user
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.type = random.choice(['shield','gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.change_x = 0
        self.change_y = 0


        # This was originally going to be a function but the stuff i intialised above wouldnt show up in a fucntion so
        # i couldnt use a function
        cursor_pos_x, cursor_pos_y = pygame.mouse.get_pos()
        dx, dy = cursor_pos_x - self.rect.x, cursor_pos_y - self.rect.y
        dist = math.hypot(dx, dy)
        re_x, re_y = dx / dist, dy / dist
        # move along this normalized vector towards the player at current speed
        self.change_x += re_x * 2
        self.change_y += re_y * 2

    def update(self):

        self.rect.x += self.change_x
        self.rect.y += self.change_y
        # delete bullet if it exits away from screen
        if self.rect.right > screen_width:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom > screen_height:
            self.kill()


# So the update and draw sections of the loop dont get congested
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

mouse = Mouse(10, 10)
all_sprites.add(mouse)

player = Player()
all_sprites.add(player)

powerups = pygame.sprite.Group()


# spawing the mobs
for i in range(8):
    newmob()





pygame.mixer.music.play(loops=-1)

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_x:
                    pygame.quit()
                    paused = False
                    quit()
        draw_text(screen, "Pause Menu", 64, screen_width / 2, 50)
        draw_text(screen, "Continue [C]", 64, screen_width / 2, 200)
        draw_text(screen, "Exit [X]", 64, screen_width / 2, 350)
        pygame.display.update()

def game_over():
    screen.blit(bg, (0, 0))
    draw_text(screen, "Gamer over", 64, screen_width / 2, 50)
    pygame.delay = 200


def game_loop():
    running = True
    score = 0
    while running == True:
        # keep loop running at the right speed
        clock.tick(fps)
        # Process input (Events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.K_ESCAPE:
                pause()
            # To fire bullets
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot()

        # Update
        all_sprites.update()
        time = int((pygame.time.get_ticks()) / 1000)
        # Check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            if random.random()>0.9:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            score += 50
            newmob()
            explosion_sound.play()

        # check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            newmob()
            player.shield -= 20
            if player.shield <= 0:
                player.kill()
        #check to see if user hits a power up
        hits = pygame.sprite.spritecollide(player, powerups, True,)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(5,22)
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'gun':
                player.powerup()

        if not player.alive():
            running = False
            game_over()

        # draw/ render


        screen.fill(black)
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        # Score
        draw_text(screen, str(score),18, screen_width/2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_text(screen, str(time), 20, 1020, 10)
        # After drawing everything update the screen
        pygame.display.update()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_loop()
                    intro == False
                if event.key == pygame.K_x:
                    quit()

        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, white, (140, 30, 800, 620))
        pygame.draw.rect(screen, black, (160, 50, 750, 580))
        draw_text(screen,"~~Space Shooter~~",64,screen_width/2,50)
        draw_text(screen, "Start Game [P]", 64, screen_width / 2, 200)
        draw_text(screen, "Highscore [H]", 64, screen_width / 2, 350)
        draw_text(screen, "Exit [X]", 64, screen_width / 2, 500)
        pygame.display.update()




game_intro()# Game loop


pygame.quit()