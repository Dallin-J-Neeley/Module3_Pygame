#https://youtu.be/LGqR-zuut5s
import pygame
import random
from pygame.constants import USEREVENT

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#defining the player
class Player(pygame.sprite.Sprite):
    direction = None
    size = None

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill ((255,255,255))
        self.rect = self.surf.get_rect( center =(400,300))  
        self.direction = ""
        

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.direction = "up"
        if pressed_keys[K_DOWN]:
            self.direction = "down"
        if pressed_keys[K_LEFT]:
            self.direction = "left"
        if pressed_keys[K_RIGHT]:
            self.direction = "right"

        if self.direction == "up":
            self.rect.move_ip(0, -5)
        if self.direction == "down":
            self.rect.move_ip(0, 5)
        if self.direction == "left":
            self.rect.move_ip(-5, 0)
        if self.direction == "right":
            self.rect.move_ip(5, 0)

        #wrap around 
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.bottom = SCREEN_HEIGHT - 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.top = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(200,600),
                random.randint(100,500),
            )
        )

#initialize the game
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)


# set the size of screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#create event for adding enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

#create the player!
player = Player() 

#create a group to hold the players and enemies
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

score = int(0)

running = True
while running:
    #look at all events that occur
    for event in pygame.event.get():
        #check if the event was a keypress
        if event.type == KEYDOWN:
            #check if the kepress was escape.
            if event.key == K_ESCAPE:
                running = False
        #Check if they pressed the X        
        elif event.type == QUIT:
            running = False
        #check if the add enemy event was called
        elif event.type == ADDENEMY:
            #only add if there are less than 5 enemies 
            if len(enemies.sprites()) < 5:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    # Fill the screen with black    
    screen.fill((0, 0, 0))

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    #update the player's location based on pressed keys
    player.update(pressed_keys)
    enemies.update()
    
    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    
    text = "score: "
    text += str(score) 
    textsurface = myfont.render(text, False, (255, 255, 255))
    screen.blit(textsurface, (0,0))

    #Check collisions
    collision = pygame.sprite.spritecollideany(player, enemies)
    if collision != None:
        score += 1
        collision.kill()

    pygame.display.flip()
    clock.tick(60)



    