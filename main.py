import pygame
import random
from os.path import join #helps us 

#general setup
pygame.init() #initializes pygame and loads it
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 #resolution our game will be in
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
direction = pygame.math.Vector2(2, -1)
velocity = direction * 100
clock = pygame.time.Clock()

# plain surface
surf = pygame.Surface((100,100)) # makes a surface (image)
surf.fill('blue')

# import image
# join prevents os errors because of either / or \
player_img = pygame.image.load(join('images', 'player.png')).convert_alpha() # helps pygame import images and runs better
player_rect = player_img.get_frect(center=(WINDOW_WIDTH/2 , WINDOW_HEIGHT/2))
stars_img = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for i in range(20)]
meteor_img = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_img.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
laser_img = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_img.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))

while running:
    dt = clock.tick() / 1000 # determines framerate, dt = delta time in ms
    # event loop. 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #draw game
    display_surface.fill('darkgray')
    for pos in star_positions:
        display_surface.blit(stars_img, pos)
    display_surface.blit(meteor_img, meteor_rect)
    display_surface.blit(laser_img, laser_rect)
    display_surface.blit(player_img, player_rect)
    if (player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0):
        velocity.x *= -1
    if (player_rect.top <= 0 or player_rect.bottom >= WINDOW_HEIGHT):
        velocity.y *= -1
    player_rect.center += velocity * dt # multiply dt to keep movement the same regardless of fps
    pygame.display.set_caption('Spaceship Game')
    pygame.display.update()
pygame.quit() #include this to ensure game quits properly
