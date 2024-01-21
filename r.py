import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

OBSTACLE_SIZE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Battle Game")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, direction):
        super().__init__()
        self.image = pygame.transform.scale(image, (OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = direction

    def update(self):
        if self.direction == "left":
            self.image = pygame.transform.flip(pygame.transform.scale(player2_image, (OBSTACLE_SIZE, OBSTACLE_SIZE)),
                                               True, False)
        else:
            self.image = pygame.transform.scale(player2_image, (OBSTACLE_SIZE, OBSTACLE_SIZE))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction

    def update(self):
        self.rect.x += bullet_speed if self.direction == "right" else -bullet_speed


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))


class HealthPack(pygame.sprite.Sprite):
    def __init__(self, x, y, heal_amount):
        super().__init__()
        self.image = pygame.image.load("healme.png")  # Замените "health_pack.png" на ваш файл с текстурой аптечки
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.heal_amount = heal_amount


def load_obstacles(file_path):
    obstacles = []
    with open(file_path, "r") as file:
        for line in file:
            obstacles.append(list(line.strip()))
    return obstacles


def create_obstacles(obstacles):
    player1_start, player2_start = None, None

    for row_index, row in enumerate(obstacles):
        for col_index, cell in enumerate(row):
            x, y = col_index * OBSTACLE_SIZE, row_index * OBSTACLE_SIZE
            if cell == '#':
                obstacle = Obstacle(x, y)
                all_sprites.add(obstacle)
                obstacles_group.add(obstacle)
            elif cell == '@':
                if player1_start is None:
                    player1_start = (x, y)
                else:
                    player2_start = (x, y)
            elif cell == 'H':
                health_pack = HealthPack(x, y, heal_amount=20)
                all_sprites.add(health_pack)
                health_packs_group.add(health_pack)

    return player1_start, player2_start


def generate_health_pack():
    x = random.randrange(0, WIDTH - OBSTACLE_SIZE, OBSTACLE_SIZE)
    y = random.randrange(0, HEIGHT - OBSTACLE_SIZE, OBSTACLE_SIZE)

    # Удаляем все текущие аптечки
    health_packs_group.empty()

    # Проверка, что аптечка не пересекается с препятствиями и игроками
    colliding_sprites = pygame.sprite.spritecollide(HealthPack(x, y, 0), obstacles_group, False)
    colliding_sprites.extend(pygame.sprite.spritecollide(HealthPack(x, y, 0), player_sprites, False))

    while colliding_sprites:
        x = random.randrange(0, WIDTH - OBSTACLE_SIZE, OBSTACLE_SIZE)
        y = random.randrange(0, HEIGHT - OBSTACLE_SIZE, OBSTACLE_SIZE)
        colliding_sprites = pygame.sprite.spritecollide(HealthPack(x, y, 0), obstacles_group, False)
        colliding_sprites.extend(pygame.sprite.spritecollide(HealthPack(x, y, 0), player_sprites, False))

    health_pack = HealthPack(x, y, heal_amount=20)
    all_sprites.add(health_pack)
    health_packs_group.add(health_pack)


all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()
health_packs_group = pygame.sprite.Group()

player1_image = pygame.image.load("dino_up.png")
player2_image = pygame.image.load("dino_up.png")

player1 = Player(50, HEIGHT // 2 - OBSTACLE_SIZE // 2, player1_image, 5, "right")
player2 = Player(WIDTH - 100, HEIGHT // 2 - OBSTACLE_SIZE // 2, player2_image, 5, "left")
all_sprites.add(player1, player2)
player_sprites.add(player1, player2)

player1_health, player2_health = 100, 100

health_bar_height, health_bar_offset = 5, 20

bullet_speed = 10

font = pygame.font.Font(None, 36)
winner_text = None

game_over = False

obstacles = load_obstacles("obstacles.txt")
player1_start, player2_start = create_obstacles(obstacles)
player1.rect.topleft = player1_start
player2.rect.topleft = player2_start

# Интервал появления аптечек
HEALTH_PACK_INTERVAL_MIN = 30000
HEALTH_PACK_INTERVAL_MAX = 30000
next_health_pack_time = pygame.time.get_ticks() + random.randint(HEALTH_PACK_INTERVAL_MIN, HEALTH_PACK_INTERVAL_MAX)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_SPACE:
                    player = player1
                elif event.key == pygame.K_RETURN:
                    player = player2
                else:
                    continue

                bullet = Bullet(
                    player.rect.x + player.rect.width if player.direction == "right" else player.rect.x - 10,
                    player.rect.y + player.rect.height // 2 - 2, player.direction)
                all_sprites.add(bullet)
                bullet_sprites.add(bullet)

            elif event.key == pygame.K_r and game_over:
                # Сброс игры
                obstacles = load_obstacles("obstacles.txt")
                player1_start, player2_start = create_obstacles(obstacles)
                player1.rect.topleft = player1_start
                player2.rect.topleft = player2_start
                player1_health, player2_health = 100, 100
                game_over = False
                winner_text = None

    keys = pygame.key.get_pressed()

    if not game_over:
        players = [(player1, keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_w], keys[pygame.K_s]),
                   (player2, keys[pygame.K_LEFT], keys[pygame.K_RIGHT], keys[pygame.K_UP], keys[pygame.K_DOWN])]

        for player, left_key, right_key, up_key, down_key in players:
            if left_key:
                player.direction = "left"
            elif right_key:
                player.direction = "right"

            new_player_rect = player.rect.copy()

            if up_key:
                new_player_rect.y -= player.speed
            if down_key:
                new_player_rect.y += player.speed
            if left_key:
                new_player_rect.x -= player.speed
            if right_key:
                new_player_rect.x += player.speed

            dummy_player = pygame.sprite.Sprite()
            dummy_player.rect = new_player_rect

            obstacles_hits_player = pygame.sprite.spritecollide(dummy_player, obstacles_group, False)
            if not obstacles_hits_player:
                player.rect = new_player_rect

        bullet_hits_obstacles = pygame.sprite.groupcollide(bullet_sprites, obstacles_group, True, False)
        for bullet, obstacles in bullet_hits_obstacles.items():
            bullet.kill()  # Удаляем пулю

        bullet_hits_player1 = pygame.sprite.spritecollide(player1, bullet_sprites, True)
        bullet_hits_player2 = pygame.sprite.spritecollide(player2, bullet_sprites, True)

        if bullet_hits_player1:
            player1_health -= 10
            if player1_health <= 0:
                winner_text = font.render("Player 2 Wins! Press R to Restart", True, GREEN)
                game_over = True
        if bullet_hits_player2:
            player2_health -= 10
            if player2_health <= 0:
                winner_text = font.render("Player 1 Wins! Press R to Restart", True, GREEN)
                game_over = True

        if pygame.sprite.collide_rect(player1, player2):
            for player, opponent in [(player1, player2), (player2, player1)]:
                if player.direction == "left" and keys[pygame.K_a]:
                    player.rect.x += player.speed
                elif player.direction == "right" and keys[pygame.K_d]:
                    player.rect.x -= player.speed

                if player.rect.colliderect(opponent.rect):
                    if keys[pygame.K_w]:
                        player.rect.y += player.speed
                    elif keys[pygame.K_s]:
                        player.rect.y -= player.speed

        # Проверка на столкновение с аптечкой
        health_pack_hits_player1 = pygame.sprite.spritecollide(player1, health_packs_group, True)
        health_pack_hits_player2 = pygame.sprite.spritecollide(player2, health_packs_group, True)

        for health_pack_hits_player in [health_pack_hits_player1, health_pack_hits_player2]:
            for health_pack in health_pack_hits_player:
                # Восстановление здоровья и удаление аптечки
                if health_pack_hits_player is health_pack_hits_player1:
                    player1_health = min(100, player1_health + health_pack.heal_amount)
                elif health_pack_hits_player is health_pack_hits_player2:
                    player2_health = min(100, player2_health + health_pack.heal_amount)

        # Генерация аптечек
        current_time = pygame.time.get_ticks()
        if current_time >= next_health_pack_time:
            generate_health_pack()
            next_health_pack_time = current_time + random.randint(HEALTH_PACK_INTERVAL_MIN, HEALTH_PACK_INTERVAL_MAX)

    screen.fill(WHITE)
    all_sprites.update()
    player_sprites.draw(screen)
    bullet_sprites.draw(screen)
    obstacles_group.draw(screen)
    health_packs_group.draw(screen)

    for player, player_health in [(player1, player1_health), (player2, player2_health)]:
        pygame.draw.rect(screen, GREEN,
                         (player.rect.x, player.rect.y - health_bar_offset, player_health / 100 * player.rect.width,
                          health_bar_height))

    if winner_text:
        text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(winner_text, text_rect)

    pygame.display.flip()
    clock.tick(30)
