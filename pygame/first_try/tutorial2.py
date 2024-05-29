import pygame
import random

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_RETURN,
    QUIT
)

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("/Users/spencer/Documents/workspace/pygame/first_try/jet2.png").convert_alpha()
        self.surf = pygame.transform.smoothscale(self.surf, (100, 32.5))
        self.surf.set_colorkey("white", RLEACCEL)
        self.rect = self.surf.get_rect()
        self.radius = 10
        self.lives = 3

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def lose_life(self):
        self.lives -= 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("/Users/spencer/Documents/workspace/pygame/first_try/bullet.png").convert_alpha()
        self.surf = pygame.transform.smoothscale(self.surf, (50, 50))
        self.surf.set_colorkey("white", RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(2, 3)
        self.radius = 15

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("/Users/spencer/Documents/workspace/pygame/first_try/clound.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (500, 500))
        self.surf.set_colorkey("black", RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )

    def update(self):
        self.rect.move_ip(-1, 0)
        if self.rect.right < 0:
            self.kill()

def display_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 750)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

def start_game():
    player = Player()
    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
            elif event.type == QUIT:
                return False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        enemies.update()
        clouds.update()

        screen.fill((135, 206, 250))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        if hits:
            player.lose_life()
            if player.lives == 0:
                game_over(score)
                return True

        score += 1
        font = pygame.font.Font(None, 36)
        display_text(f'Score: {score}', font, (0, 0, 0), screen, SCREEN_WIDTH // 2, 20)
        display_text(f'Lives: {player.lives}', font, (0, 0, 0), screen, SCREEN_WIDTH // 2, 60)

        pygame.display.flip()
        clock.tick(60)

    return False

def game_over(score):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    display_text('Game Over', font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    font = pygame.font.Font(None, 36)
    display_text(f'Your score: {score}', font, (255, 255, 255), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    display_text('Press Enter to restart or Esc to quit', font, (255, 255, 255), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    waiting = False
                    return
                elif event.key == K_ESCAPE:
                    waiting = False
                    pygame.quit()
                    exit()
            elif event.type == QUIT:
                waiting = False
                pygame.quit()
                exit()

def main_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    display_text('Press Enter to Start', font, (255, 255, 255), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    waiting = False
                    return
                elif event.key == K_ESCAPE:
                    waiting = False
                    pygame.quit()
                    exit()
            elif event.type == QUIT:
                waiting = False
                pygame.quit()
                exit()

while True:
    main_menu()
    if not start_game():
        break
