import pygame
from sys import exit
from random import randint, choice

PEWPEW = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics\Player\player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics\Player\player_walk_2.png').convert_alpha()
        self.walk = [player_walk_1, player_walk_2]
        self.index = 0
        self.jump = pygame.image.load('graphics\Player\jump.png').convert_alpha()
        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio\jump.mp3')
    
    def check_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.index += 0.1
            if self.index >= len(self.walk): self.index = 0
            self.image = self.walk[int(self.index)]

    def update(self):
        self.check_input()
        self.apply_gravity()
        self.animate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        self.type = type
        if self.type == 'snail':
            snail_1 = pygame.image.load('graphics\Snail\snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics\Snail\snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        elif self.type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 200
        
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(bottomright=(randint(900,1100), y_pos))
    
    def movement(self):
        self.rect.x -= 6
        if self.rect.right < 0: self.kill()

    def animate(self, type):
        if self.type == type:
            if self.index == 0: self.index = 1
            else: self.index = 0
            self.image = self.frames[self.index]
    
    if PEWPEW:
        def spawn_pewpew(self):
            if self.type == 'snail':
                pewpew_sound.play()
                pewpew_group.add(PewPew(self.rect.left))

    def update(self):
        self.movement()

class ObstacleGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
    
    def animate(self, type):
        for sprite in super().sprites():
            sprite.animate(type)
    
    if PEWPEW:
        def spawn_pewpew(self):
            for sprite in super().sprites():
                sprite.spawn_pewpew()

if PEWPEW:
    class PewPew(pygame.sprite.Sprite):
        def __init__(self, x_pos):
            super().__init__()
            self.image = pygame.image.load('graphics\laser.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.25)
            self.rect = self.image.get_rect(midright=(x_pos+20,287))
        
        def movement(self):
            self.rect.y = player.sprite.rect.y + 40
            self.rect.x -= 10
            if self.rect.right <= 0: self.kill()
        
        def update(self):
            self.movement()

def displayScore():
    current_score = int((pygame.time.get_ticks() - start_time)/1000)
    score_surf = pixel_type.render(f"Score: {current_score}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf, score_rect)
    return current_score

def check_collision():
    global game_active
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        if PEWPEW: pewpew_group.empty()
        game_active = False

pygame.init()
clock = pygame.time.Clock()
start_time = 0
game_active = False
score = 0

#music
bg_music = pygame.mixer.Sound('audio\music.wav')
bg_music.play(loops = -1)

if PEWPEW: pewpew_sound = pygame.mixer.Sound('audio\pew pew.mp3')

#creating game window
icon = pygame.image.load('graphics\Snail\snail1.png')
pygame.display.set_caption("snel game!")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 400))

#creating fonts
pixel_type = pygame.font.Font('font\Pixeltype.ttf', 50)

#creating background surfaces
sky_surface = pygame.image.load("graphics\sky.png").convert()
ground_surface = pygame.image.load("graphics\ground.png").convert()

#sprite groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = ObstacleGroup()

if PEWPEW: pewpew_group = pygame.sprite.Group()

#game over/intro screen
player_stand = pygame.image.load('graphics\Player\player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = pixel_type.render("snel game!", False, (111,196,169))
game_name_rect = game_name.get_rect(midtop = (400,50))

#timers
obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event, 1100)

snail_animation_event = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_event, 500)
fly_animation_event = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_event, 200)

if PEWPEW:
    pewpew_event = pygame.USEREVENT + 4
    pygame.time.set_timer(pewpew_event, 2000)

tick_rate = 60
while True:

    #event loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            
            #obstacle spawn
            if event.type == obstacle_event: obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))
            
            #obstacle animation
            if event.type == snail_animation_event: obstacle_group.animate('snail')
            if event.type == fly_animation_event: obstacle_group.animate('fly')

            #pewpew spawn
            if PEWPEW:
                if event.type == pewpew_event: obstacle_group.spawn_pewpew()
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start_time = pygame.time.get_ticks()
                game_active = True
    
    if game_active:
        #background
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        #score text
        score = displayScore()        

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        if PEWPEW:
            pewpew_group.draw(screen)
            pewpew_group.update()

        check_collision()
    
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        if score==0: game_message = pixel_type.render("Press SPACE to start", False, (111,196,169))
        else: game_message = pixel_type.render(f"Score: {score}", False, (111,196,169))
        game_message_rect = game_message.get_rect(midbottom = (400,350))
        screen.blit(game_message, game_message_rect)

    pygame.display.update()
    clock.tick(int(tick_rate))
    tick_rate = 60 + 5*(score//10)