import pygame
from pygame.locals import *
import random

pygame.init()

game_width = 800
game_height = 500
screen_size = (game_width,game_height)
game_window=pygame.display.set_mode(screen_size)
pygame.display.set_caption("Helicopter_Game")
padding_y = 10

black = (0,0,0)
red=(255,0,0)
yellow=(255,255,0)

bullet_cooldown = 500

last_bullet_time = pygame.time.get_ticks()

next_bird = pygame.time.get_ticks()

def scale_image(image,new_width):
    image_scale=new_width / image.get_rect().width
    new_hight =image.get_rect().height * image_scale
    scaled_size = (new_width,new_hight)
    return pygame.transform.scale(image,scaled_size)

bg = pygame.image.load("bg.png").convert_alpha()
bg = scale_image(bg,game_width)
bg_scroll = 0


airplane_images = []
for i in range(2):
    airplane_image = pygame.image.load(f"player/fly{i}.png").convert_alpha()
    airplane_image = scale_image(airplane_image,70)
    airplane_images.append(airplane_image)

heart_images = []
heart_image_index = 0
for i in range(8):
    heart_image = pygame.image.load(f"hearts/heart{i}.png").convert_alpha()
    heart_image = scale_image(heart_image,30)
    heart_images.append(heart_image)

bird_colors = ["blue","red","grey","yellow"]

bird_images = {}
for bird_color in bird_colors:

    bird_images[bird_color] = []

    for i in range(4):

        bird_image = pygame.image.load(f'birds/{bird_color}{i}.png').convert_alpha()
        bird_image = scale_image(bird_image,50)

        bird_image = pygame.transform.flip(bird_image,True,False)

        bird_images[bird_color].append(bird_image)



class Player(pygame.sprite.Sprite):

    def __init__(self,x,y):

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

        self.lives = 3
        self.score = 0

        self.image_index = 0

        self.image_angle = 0

    def update(self):

        self.image_index += 1
        if self.image_index >= len(airplane_images):
            self.image_index = 0

        self.image = airplane_images[self.image_index]
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, self.image_angle)

        self.rect.x = self.x
        self.rect.y = self.y

        if pygame.sprite.spritecollide(self,bird_group,True):
            self.lives -= 1


class Bullet(pygame.sprite.Sprite):

    def __init__(self,x,y):

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = 5

        self.rect = Rect(x,y,10,10)

    def draw(self):
        pygame.draw.circle(game_window,yellow,(self.x,self.y),self.radius)

    def update(self):

        self.x += 2

        self.rect.x = self.x
        self.rect.y = self.y


        if self.x > game_width:
            self.kill()

class Bird(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.x = game_width

        self.y = random.randint(padding_y,game_height-padding_y*2)

        self.color = random.choice(bird_colors)

        self.image_index = 0

        self.image = bird_images[self.color][self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):

        self.x -= 2

        self.image_index += 0.25
        if self.image_index >= len(bird_images[self.color]):
            self.image_index = 0


        self.image = bird_images[self.color][int(self.image_index)]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


        if pygame.sprite.spritecollide(self,bullet_group,True):
            self.kill()
            player.score += 1

        if self.x < 0:
            self.kill()

player_group = pygame.sprite.Group()
bullet_group= pygame.sprite.Group()
bird_group= pygame.sprite.Group()

player_x = 30
player_y = game_height // 2
player = Player(player_x,player_y)
player_group.add(player)

clock = pygame.time.Clock()
fps= 120
running=True
while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running= False

    keys = pygame.key.get_pressed()

    if keys[K_UP] and player.rect.top > padding_y:
        player.y -= 2
        player.image_angle = 15
    elif keys[K_DOWN] and player.rect.bottom < game_height -padding_y:
        player.y += 2
        player.image_angle = -15
    else:
        player.image_angle = 0

    if keys[K_SPACE] and last_bullet_time + bullet_cooldown < pygame.time.get_ticks():
        bullet_x = player.x + player.image.get_width()
        bullet_y = player.y + player.image.get_height() // 2
        bullet = Bullet(bullet_x, bullet_y)
        bullet_group.add(bullet)
        last_bullet_time = pygame.time.get_ticks()

    if next_bird < pygame.time.get_ticks():
        bird = Bird()
        bird_group.add(bird)

        next_bird = random.randint(pygame.time.get_ticks(),pygame.time.get_ticks()+3000)

    game_window.blit(bg,(0-bg_scroll,0))
    game_window.blit(bg,(game_width-bg_scroll,0))
    bg_scroll += 1
    if bg_scroll == game_width:
        bg_scroll = 0

    player_group.update()
    player_group.draw(game_window)

    bullet_group.update()
    for bullet in bullet_group:
        bullet.draw()

    bird_group.update()
    bird_group.draw(game_window)


    for i in range(player.lives):
        heart_image = heart_images[int(heart_image_index)]
        heart_x = 10 + i *(heart_image.get_width()+10)
        heart_y = 10
        game_window.blit(heart_image,(heart_x,heart_y))
    heart_image_index += 0.1
    if heart_image_index >= len(heart_images):
        heart_image_index = 0

    font = pygame.font.Font(pygame.font.get_default_font(),16)
    text = font.render(f"Score: {player.score}",True,black)
    text_rect = text.get_rect()
    text_rect.center = (200,20)
    game_window.blit(text,text_rect)

    pygame.display.update()

    while player.lives == 0:
        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()

        gameover_str = f"Game over. Play again (y or n)?"
        font = pygame.font.Font(pygame.font.get_default_font(),24)
        text = font.render(gameover_str, True, red)
        text_rect = text.get_rect()
        text_rect.center = (game_width/ 2, game_height / 2)
        game_window.blit(text,text_rect)

        keys = pygame.key.get_pressed()
        if keys[K_y]:

            player_group.empty()
            bullet_group.empty()
            bird_group.empty()

            player = Player(player_x,player_y)
            player_group.add(player)

        elif keys[K_n]:
            running = False
            break

pygame.quit()


