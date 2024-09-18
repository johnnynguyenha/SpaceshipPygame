# Johnny Nguyen
# johnnynguyenha on github

import pygame
import Player
import random
from random import uniform
from os.path import join 

#general setup
pygame.init() #initializes pygame and loads it
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 #resolution our game will be in
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite,):
    def __init__(self, groups):
        super().__init__(groups)
        self.original_image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.image = self.original_image # helps pygame import images and runs better
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2 , WINDOW_HEIGHT/2))
        self.velocity = 500
        self.direction = pygame.math.Vector2(0,0)
    
    # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    # mask
        self.mask = pygame.mask.from_surface(self.image)


    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s] - int(keys[pygame.K_w]))
        self.direction = self.direction.normalize() if self.direction else self.direction # no matter what direction, will always be at the same speed
        player.rect.center += self.direction * self.velocity * dt
        
        recent_keys = pygame.key.get_just_pressed()
        if (recent_keys[pygame.K_SPACE] and self.can_shoot):
            Laser((all_sprites, laser_sprites), laser_surf, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image =  surf # helps pygame import images and runs better
        self.rect = self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))
    def update(self, dt):
        pass

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0: #remove the laser when it goes off screen
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.original_image = surf
        self.image = self.original_image
        self.rect = self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)))
    # meteor timer
        self.alive = True
        self.kill_time = 30000
        self.start_time = pygame.time.get_ticks()
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = random.randint(400,500)
        self.rotation_speed = random.randint(40,80)
        self.rotation = 0

    def meteor_timer(self): 
        if pygame.time.get_ticks() - self.start_time > self.kill_time:
            self.kill()
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        self.meteor_timer()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1) # meteors rotate
        self.rect = self.image.get_frect(center= self.rect.center) # meteors dont wobble

class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()

def collisions():
    global running
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
         damage_sound.play()
         running = False
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            Explosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks()
    text_surf = font.render(str(current_time), True, '#98ff98')
    text_rect = text_surf.get_frect(midbottom = ((WINDOW_WIDTH/2), WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface, 'white', text_rect.inflate(30,10).move(0,-5), 5, 10)




# plain surface
surf = pygame.Surface((100,100)) # makes a surface (image)
surf.fill('blue')

# import
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_img = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
laser_sound.set_volume(0.05)
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
explosion_sound.set_volume(0.05)
damage_sound = pygame.mixer.Sound(join('audio', 'damage.ogg'))
damage_sound.set_volume(0.05)
music_sound = pygame.mixer.Sound(join('audio', 'game_music.wav'))
music_sound.set_volume(0.03)
music_sound.play(loops = -1)

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites,star_surf)
player = Player(all_sprites)

#custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000 # determines framerate, dt = delta time in ms
    # event loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((meteor_sprites, all_sprites), meteor_img)
    # update
    all_sprites.update(dt)
    collisions()

    #draw game
    display_surface.fill('mediumpurple4')
    all_sprites.draw(display_surface)
    pygame.display.set_caption('Spaceship Game')
    display_score()

    pygame.display.update()
pygame.quit() #include this to ensure game quits properly
