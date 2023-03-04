import pygame
from pygame import  mixer
import random

pygame.init()
mixer.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 1100, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

RUNNING = [pygame.image.load('Assets/Dino/DinoRun1.png'), pygame.image.load('Assets/Dino/DinoRun2.png')]
DUCKING = [pygame.image.load('Assets/Dino/DinoDuck1.png'), pygame.image.load('Assets/Dino/DinoDuck2.png')]
JUMP = pygame.image.load('Assets/Dino/DinoJump.png')

LARGE_CACTUS = [pygame.image.load('Assets/Cactus/LargeCactus1.png'), pygame.image.load('Assets/Cactus/LargeCactus2.png'), pygame.image.load('Assets/Cactus/LargeCactus3.png')]

BIRD = [pygame.image.load('Assets/Bird/Bird1.png'), pygame.image.load('Assets/Bird/Bird2.png')]

CLOUD, GROUND = pygame.image.load('Assets/Other/Cloud.png'), pygame.image.load('Assets/Other/Track.png')
GAMOVER = pygame.image.load('Assets/Other/GameOver.png')
GAMOVER_WIDTH, GAMOVER_HEIGHT = GAMOVER.get_width(), GAMOVER.get_height()

score_sound = mixer.Sound('Assets/sound/score.mp3')
jump_sound = mixer.Sound('Assets/sound/jump.mp3')
death_sound = mixer.Sound('Assets/sound/death.mp3')

global points, gameSpeed, run, scores

class Dino:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5
    DUCK_POS = 340

    def __init__(self):
        self.run_img = RUNNING
        self.duck_img = DUCKING
        self.jump_img = JUMP
        self.dino_jump = False
        self.dino_duck = False
        self.dino_run = True
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.dino_rect.height = 10
        self.dino_rect.width = 15

    def update(self):
        User_Input = pygame.key.get_pressed()

        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()


        if ((User_Input[pygame.K_SPACE]) and not self.dino_jump):
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            mixer.Sound.play(jump_sound)
        if User_Input[pygame.K_DOWN] and not self.dino_duck:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif (not self.dino_jump and not User_Input[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        
            

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = self.run_img[self.step_index//5]
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.dino_rect.y = self.Y_POS

    def restart_pos(self):
        self.dino_rect.x = self.X_POS
        

    def duck(self):
        if self.dino_duck:
            self.image = self.duck_img[self.step_index//5]
            self.dino_rect.y = self.DUCK_POS
            self.step_index += 1
            

    def draw(self):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))



class Background:
    def __init__(self, gameSpeed):
        self.x_bg_pos = 0
        self.Y_BG_POS = 384
        self.game_speed = gameSpeed
        self.bg_img = GROUND
        self.BG_WIDTH = self.bg_img.get_width()

    def draw(self):
        SCREEN.blit(self.bg_img, (self.x_bg_pos, self.Y_BG_POS))
        SCREEN.blit(self.bg_img, (self.x_bg_pos+self.BG_WIDTH, self.Y_BG_POS))
        if self.x_bg_pos <= -self.BG_WIDTH:
            self.x_bg_pos = 0
        self.x_bg_pos -= self.game_speed


class Cloud:
    def __init__(self, gameSpeed):
        self.image = CLOUD
        self.IMG_WIDTH = self.image.get_width()
        self.x_pos_1 = random.randint(700, 1000)
        self.y_pos_1 = random.randint(20, 100)
        self.game_speed = gameSpeed

    def draw(self):
        SCREEN.blit(self.image, (self.x_pos_1, self.y_pos_1))

    def update(self):
        self.x_pos_1 -= self.game_speed
        if self.x_pos_1 <= -self.IMG_WIDTH:
            self.x_pos_1 = SCREEN_WIDTH + random.randint(500, 1000)

class LargeCactus:
    def __init__(self, gameSpeed):
        self.images = LARGE_CACTUS
        self.Y_POS = 310
        self.x_pos = SCREEN_WIDTH
        self.img_type = random.randint(0, 2)
        self.rect = self.images[self.img_type].get_rect()
        self.rect.height = 12
        self.rect.width = 30
        self.rect.y = self.Y_POS
        self.rect.x = self.x_pos  + random.randint(30, 50)
        self.game_speed = gameSpeed

    def draw(self):
        SCREEN.blit(self.images[self.img_type], (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x -= self.game_speed
        if self.rect.x <= -self.images[self.img_type].get_width():
            obstacles.pop()
            self.__init__(self.game_speed)


class Bird:
    def __init__(self, gameSpeed):
        self.images = BIRD
        self.step_index = 0
        self.x_pos = SCREEN_WIDTH
        self.y_pos = 250
        self.game_speed = gameSpeed
        self.rect = self.images[self.step_index].get_rect()
        self.rect.x = self.x_pos + random.randint(1, 7)
        self.rect.y = self.y_pos
        self.rect.height = 15
        self.rect.width = 20

    def draw(self):
        SCREEN.blit(self.images[self.step_index//5], (self.rect.x, self.rect.y))

    def update(self):
        if self.step_index >= 9:
            self.step_index = 0
        self.step_index += 1
        self.rect.x -= self.game_speed
        if self.rect.x < -self.images[self.step_index//5].get_width():
            obstacles.pop()
            self.__init__(self.game_speed)


def main():
    global obstacles, points, death, gameSpeed, run, scores
    gameSpeed = 12
    run = True
    clock = pygame.time.Clock()
    player = Dino()
    bg = Background(gameSpeed)
    cloud = Cloud(gameSpeed + 2)
    L_cactus = LargeCactus(gameSpeed)
    bird = Bird(gameSpeed)
    obstacles = []
    points = 1
    scores = 1
    font = pygame.font.Font('freesansbold.ttf', 32)
    
    def Score():
        global points, scores, gameSpeed
        points += 1
        if points%10 == 0:
            scores += 1
        if(scores%100 == 0):
            gameSpeed +=1
            mixer.Sound.play(score_sound)
        text = font.render(f"Points: {scores}", True, (128,128,128))
        textRect = text.get_rect()
        textRect.x, textRect.y = 500, 20 
        SCREEN.blit(text, textRect)
        


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        if len(obstacles) == 0:
            if random.randint(0, 1) == 0:
                obstacles.append(L_cactus)
            elif random.randint(0, 2) == 1:
                obstacles.append(bird)


        Score()
        player.draw()
        player.update()
        bg.draw()
        cloud.draw()
        cloud.update()

        for obstacle in obstacles:
            obstacle.draw()
            obstacle.update()
            if (player.dino_rect.colliderect(obstacle.rect) or (obstacle == bird and (not player.dino_duck and player.dino_rect.x >= obstacle.rect.x))):
                mixer.Sound.play(death_sound)
                GameOver()
 


        clock.tick(30)
        pygame.display.update()


def GameOver():
    pygame.time.delay(1500)
    main()


main()

