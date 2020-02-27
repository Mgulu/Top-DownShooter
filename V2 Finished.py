# laser sound from dklon open game market
# background imahe Corykeks deviant art
# background music t4ngr4m open game market
# Expolsion sound by Lamoot
# Ufo by Lazy Lazor




import pygame
import random
import os
import math
import sys

# Constants
import self as self



screen_length = 1080
screen_height = 720
# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (128,128,128)
dimgrey = (105,105,105)
yellow = (255, 255, 0)

# So we dont contsanly write clock(60) and can write clock(fps) instead
clock = pygame.time.Clock()
fps = 60

# initialize pygame and create window
pygame.init()
# for audio
pygame.mixer.init()
screen = pygame.display.set_mode((screen_length, screen_height))
pygame.display.set_caption("Space invaders")

# sounds
player_laser_sound = pygame.mixer.Sound('laser.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
pygame.mixer.music.load('music.ogg')
# change back to 0.4
pygame.mixer.music.set_volume(0.00001)

# powerup time


# Mob spawning
def newufo():
    ufo = Alien()
    all_objects.add(ufo)
    mob.add(ufo)

#Health bar
def draw_user_health(area,x,y,pct):
    if pct < 0:
        pct = 0
    rectangle_length = 100
    rectangle_height = 10
    health_bar = (pct/100)*rectangle_length
    main_bar = pygame.Rect( x,y, rectangle_length, rectangle_height)
    health_bar_rect = pygame.Rect( x,y, health_bar ,rectangle_height)
    pygame.draw.rect(area, red, health_bar_rect)
    pygame.draw.rect(area,white,main_bar,2)


# For the background
bg = pygame.image.load('bg.jpg').convert()

# class for aliens

ufo_images = []
ufo_list = ['ufo.gif','ufoB.gif','ufoG.gif','ufoP.gif','ufoW.gif',]
for img in ufo_list:
    ufo_images.append(pygame.image.load(img))

# score and time function

#Font
font_type = pygame.font.match_font('arial')
def text_draw(area,text,size,x,y):
    font = pygame.font.Font(font_type,size)
    text_bar = font.render(text, True,white)
    text_rect = text_bar.get_rect()
    text_rect.midtop = (x,y)
    area.blit(text_bar,text_rect)

# powerUps
powerup_images = {}
powerup_images['health'] = pygame.image.load('health.jpg').convert()
powerup_images['gun'] = pygame.image.load('star.png').convert()


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(ufo_images)
        # To make the color white transparent
        self.image.set_colorkey(black)
        self.image.set_alpha()
        self.rect = self.image.get_rect()
        self.original_image = self.image
        # circle so that it collides with the circle i give it
        self.radius = 24

        # Spawns the enemy somewhere outside the screen but away from the user
        # This needs to change enemies arent spawning away from the user, sometimes ontop of him

        time = int((pygame.time.get_ticks()) / 1000)

        self.rect.x = random.randrange(0, screen_length - time*2)
        choice = random.randint(1,2)
        if choice == 1:
            self.rect.y = random.randrange(screen_height - 10 - time * 2, screen_height - time * 2)
        elif choice == 2:
            self.rect.y = random.randrange(-60, 0)
        # Vary the speed of the enemies
        self.speedy = random.randrange(2,4)

    def move_towards_user(self, user):
        # find normalized direction vector (dx, dy) between enemy and user
        dx, dy = self.rect.x - user.rect.x, self.rect.y - user.rect.y
        distance = math.hypot(dx, dy)
        dx, dy = dx / distance, dy / distance
        # move along this normalized vector towards the user at current speed
        self.rect.x -= dx * self.speedy
        self.rect.y -= dy * self.speedy

    #Rotates aliens but has a problem with the intial facing direction
    #Isnt the same as the users problem as it dosent require the mouse input which is why the user rotations is off
    def rotate_alien(self, user):
        new_x, new_y = user.rect.x - self.rect.x, user.rect.y - self.rect.y
        angle = math.atan2(new_y, new_x)
        angle = (180 / math.pi) * math.atan2(new_y, new_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.image.set_colorkey(black)
        self.image.set_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)

    # for the update part of the loop
    def update(self):
        self.rotate_alien(user)
        self.move_towards_user(user)


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


class User(pygame.sprite.Sprite):
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
        self.health = 100
        # Delay in shooting
        self.shoot_delay = 150
        #powerups
        # Size of the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (screen_length / 2, screen_height / 2)

        # Circle so that it collides with a circle i give it
        self.radius = 24


        # speed of sprite
        self.speedx = 0
        self.speedy = 0

    def rotate_user(self, mouse):
        new_x, new_y = mouse.rect.x - self.rect.x, mouse.rect.y - self.rect.y
        angle = math.atan2(new_y, new_x)
        angle = (180 / math.pi) * math.atan2(new_y, new_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.image.set_colorkey(black)
        self.image.set_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)

    # Fot the update part of my loop
    def update(self):
        time = int((pygame.time.get_ticks()) / 1000)
        self.rotate_user(mouse)
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
        if self.rect.right > screen_length - time *2 :
            self.rect.right = screen_length - time*2
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height - time*2:
            self.rect.bottom = screen_height - time*2
        self.rect.x += self.speedx
        self.rect.y += self.speedy





    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_objects.add(bullet)
        projectile.add(bullet)
        player_laser_sound.play()




# Bullets require a seperate sprite
class Bullet(pygame.sprite.Sprite):
    # X , y in the function so we can later anchor it to the user
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pygame.image.load('laser.png').convert_alpha()
        self.original_image = self.image
        # To make the color white transparent
        self.image.set_colorkey(white)
        self.image.set_alpha()
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.rect.x = user.rect.x
        self.rect.y = user.rect.y

        # This was originally going to be a function but the stuff i intialised above wouldnt show up in a fucntion so
        # i couldnt use a function
        cursor_pos_x, cursor_pos_y = pygame.mouse.get_pos()
        dx, dy = cursor_pos_x - self.rect.x, cursor_pos_y - self.rect.y
        distance = math.hypot(dx, dy)
        new_x, new_y = dx / distance, dy / distance
        # move along this normalized vector towards the player at current speed
        self.change_x += new_x * 5
        self.change_y += new_y * 5


        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        new_x, new_y = mouse_pos_x - self.rect.x, mouse_pos_y - self.rect.y
        angle = math.atan2(new_y, new_x)
        angle = (180 / math.pi) * math.atan2(new_y, new_x)
        self.image = pygame.transform.rotate(self.original_image, int(angle))
        self.image.set_colorkey(white)
        self.image.set_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)


    def update(self):
        time = int((pygame.time.get_ticks()) / 1000)
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        # delete bullet if it exits away from screen
        if self.rect.right > screen_length - time *2:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom > screen_height - time *2 :
            self.kill()

class Bonus(pygame.sprite.Sprite):
# X , y in the function so we can later anchor it to the user
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.type = random.choice(['health','gun'])
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
        distance = math.hypot(dx, dy)
        new_x, new_y = dx / distance, dy / distance
        # move along this normalized vector towards the player at current speed
        self.change_x += new_x * 2
        self.change_y += new_y * 2

    def update(self):
        time = int((pygame.time.get_ticks()) / 1000)
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        # delete bullet if it exits away from screen
        if self.rect.right > screen_length - time *2:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.bottom > screen_height - time *2 :
            self.kill()


# So the update and draw sections of the loop dont get congested

all_objects = pygame.sprite.Group()
mob = pygame.sprite.Group()
projectile = pygame.sprite.Group()

mouse = Mouse(10, 10)
all_objects.add(mouse)

user = User()
all_objects.add(user)

powerups = pygame.sprite.Group()


# spawing the mob
for i in range(8):
    newufo()

pygame.mixer.music.play(loops=-1)



def game_over():
    game_ovr = True
    while game_ovr:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_x:
                    pygame.quit()
                    game_ovr = False
                    quit()

        screen.blit(bg, (0, 0))
        text_draw(screen, "You Lose \n Gamer over", 64, screen_length / 2, 50)

        text_draw(screen, "Exit [X]", 64, screen_length / 2, 350)
        pygame.display.update()

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.quit()
                    paused = False
                    quit()
                if event.key == pygame.K_r:
                    paused = False
        screen.blit(bg, (0, 0))
        text_draw(screen, "Pause Menu", 64, screen_length / 2, 50)
        text_draw(screen, "Resume [R]", 64, screen_length / 2, 250)
        text_draw(screen, "Exit [X]", 64, screen_length / 2, 450)
        pygame.display.update()


def game_loop():
    gameloop = True
    score = 0
    while gameloop == True:
        # Process input (Events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
            #To fire bullets
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    user.shoot()

        # keep loop running at the right speed
        clock.tick(fps)
        # Update
        all_objects.update()
        global time
        time = int((pygame.time.get_ticks()) / 1000)
        # Check to see if a bullet hit a mob
        bullet_collision = pygame.sprite.groupcollide(mob, projectile, True, True)
        for i in bullet_collision:
            if random.random()>0.9:
                # To get the postion where the collision was
                new_powerup = Bonus(i.rect.center)
                all_objects.add(new_powerup)
                powerups.add(new_powerup)
            score += 50
            newufo()
            explosion_sound.play()

        # check to see if a mob hit the player
        mob_collision = pygame.sprite.spritecollide(user, mob, True, pygame.sprite.collide_circle)
        for i in mob_collision:
            newufo()
            user.health -= 20
            if user.health <= 0:
                user.kill()

        #check to see if user hits a power up
        power_collision = pygame.sprite.spritecollide(user, powerups, True,)
        for i in power_collision:
            if i.type == 'health':
                user.health += random.randrange(5,22)
                if user.health >= 100:
                    user.health = 100


        if not user.alive():
            gameloop = False
            game_over()

        # draw/ render

        screen.fill(black)
        background = pygame.transform.scale(bg, ((1280- time* 4) , (720- time* 2)))
        screen.blit(background, (0, 0))
        all_objects.draw(screen)
        # Score
        text_draw(screen, str(score),18, screen_length/2, 10)
        draw_user_health(screen, 5, 5, user.health)
        text_draw(screen, str(time), 20, 1020, 10)
        text_draw(screen, 'P to Pause', 20, 1020, 50)
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
                    intro = False
                    game_loop()
                if event.key == pygame.K_x:
                    quit()
                elif event.type == pygame.K_q:
                    pause()

        screen.blit(bg, (0, 0))
        pygame.draw.rect(screen, white, (140, 30, 800, 620))
        pygame.draw.rect(screen, black, (160, 50, 750, 580))
        text_draw(screen,"~~Space Shooter~~",64,screen_length/2,50)
        text_draw(screen, "Start Game [P]", 64, screen_length / 2, 200)
        text_draw(screen, "Highscore [H]", 64, screen_length / 2, 350)
        text_draw(screen, "Exit [X]", 64, screen_length / 2, 500)
        pygame.display.update()

game_intro()# Game loop


pygame.quit()