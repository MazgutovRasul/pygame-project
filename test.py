import pygame
import sys

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
        if self.direction == "right":
            self.rect.x += bullet_speed
        else:
            self.rect.x -= bullet_speed


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))


def load_obstacles(file_path):
    obstacles = []
    with open(file_path, "r") as file:
        for line in file:
            obstacles.append(list(line.strip()))
    return obstacles


def create_obstacles(obstacles):
    player1_start = None
    player2_start = None

    for row_index, row in enumerate(obstacles):
        for col_index, cell in enumerate(row):
            if cell == '#':
                obstacle = Obstacle(col_index * OBSTACLE_SIZE, row_index * OBSTACLE_SIZE)
                all_sprites.add(obstacle)
                obstacles_group.add(obstacle)
            elif cell == '@':
                if player1_start is None:
                    player1_start = (col_index * OBSTACLE_SIZE, row_index * OBSTACLE_SIZE)
                else:
                    player2_start = (col_index * OBSTACLE_SIZE, row_index * OBSTACLE_SIZE)

    player1.rect.topleft = player1_start
    player2.rect.topleft = player2_start




all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
obstacles_group = pygame.sprite.Group()

player1_image = pygame.image.load("dino_up.png")
player2_image = pygame.image.load("dino_up.png")

# Уменьшаем начальное положение игроков
player1 = Player(50, HEIGHT // 2 - OBSTACLE_SIZE // 2, player1_image, 5, "right")
player2 = Player(WIDTH - 100, HEIGHT // 2 - OBSTACLE_SIZE // 2, player2_image, 5, "left")
all_sprites.add(player1, player2)
player_sprites.add(player1, player2)

player1_health = 100
player2_health = 100

health_bar_height = 5
health_bar_offset = 20

bullet_speed = 10

font = pygame.font.Font(None, 36)
winner_text = None

game_over = False

obstacles = load_obstacles("obstacles.txt")
create_obstacles(obstacles)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet = Bullet(
                    player1.rect.x + player1.rect.width if player1.direction == "right" else player1.rect.x - 10,
                    player1.rect.y + player1.rect.height // 2 - 2, player1.direction)
                all_sprites.add(bullet)
                bullet_sprites.add(bullet)

            elif event.key == pygame.K_RETURN and not game_over:
                bullet = Bullet(
                    player2.rect.x + player2.rect.width if player2.direction == "right" else player2.rect.x - 10,
                    player2.rect.y + player2.rect.height // 2 - 2, player2.direction)
                all_sprites.add(bullet)
                bullet_sprites.add(bullet)

            elif event.key == pygame.K_r and game_over:
                # Сброс игры
                player1.rect.topleft = (50, HEIGHT // 2 - OBSTACLE_SIZE // 2)
                player2.rect.topleft = (WIDTH - 100, HEIGHT // 2 - OBSTACLE_SIZE // 2)
                player1_health = 100
                player2_health = 100
                game_over = False
                winner_text = None

    keys = pygame.key.get_pressed()

    if not game_over:
        # Player 1 direction
        if keys[pygame.K_a]:
            player1.direction = "left"
        elif keys[pygame.K_d]:
            player1.direction = "right"

        # Player 2 direction
        if keys[pygame.K_LEFT]:
            player2.direction = "left"
        elif keys[pygame.K_RIGHT]:
            player2.direction = "right"
        # Player 1 movement
        new_player1_rect = player1.rect.copy()
        if keys[pygame.K_w]:
            new_player1_rect.y -= player1.speed
        if keys[pygame.K_s]:
            new_player1_rect.y += player1.speed
        if keys[pygame.K_a]:
            new_player1_rect.x -= player1.speed
        if keys[pygame.K_d]:
            new_player1_rect.x += player1.speed

        # Create a dummy sprite for collision detection
        dummy_player1 = pygame.sprite.Sprite()
        dummy_player1.rect = new_player1_rect

        # Check for collisions with obstacles
        obstacles_hits_player1 = pygame.sprite.spritecollide(dummy_player1, obstacles_group, False)
        if not obstacles_hits_player1:
            player1.rect = new_player1_rect

        # Player 2 movement
        new_player2_rect = player2.rect.copy()
        if keys[pygame.K_UP]:
            new_player2_rect.y -= player2.speed
        if keys[pygame.K_DOWN]:
            new_player2_rect.y += player2.speed
        if keys[pygame.K_LEFT]:
            new_player2_rect.x -= player2.speed
        if keys[pygame.K_RIGHT]:
            new_player2_rect.x += player2.speed

        # Create a dummy sprite for collision detection
        dummy_player2 = pygame.sprite.Sprite()
        dummy_player2.rect = new_player2_rect

        # Check for collisions with obstacles
        obstacles_hits_player2 = pygame.sprite.spritecollide(dummy_player2, obstacles_group, False)
        if not obstacles_hits_player2:
            player2.rect = new_player2_rect

        obstacles_hits_player1 = pygame.sprite.spritecollide(player1, obstacles_group, False)
        obstacles_hits_player2 = pygame.sprite.spritecollide(player2, obstacles_group, False)


        # Обработка столкновений пуль с преградами
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
            if player1.direction == "left" and keys[pygame.K_a]:
                player1.rect.x += player1.speed
            elif player1.direction == "right" and keys[pygame.K_d]:
                player1.rect.x -= player1.speed
            if player1.rect.colliderect(player2.rect):
                if keys[pygame.K_w]:
                    player1.rect.y += player1.speed
                elif keys[pygame.K_s]:
                    player1.rect.y -= player1.speed

            if player2.direction == "left" and keys[pygame.K_LEFT]:
                player2.rect.x += player2.speed
            elif player2.direction == "right" and keys[pygame.K_RIGHT]:
                player2.rect.x -= player2.speed
            if player2.rect.colliderect(player1.rect):
                if keys[pygame.K_UP]:
                    player2.rect.y += player2.speed
                elif keys[pygame.K_DOWN]:
                    player2.rect.y -= player2.speed

    screen.fill(WHITE)
    all_sprites.update()
    player_sprites.draw(screen)
    bullet_sprites.draw(screen)
    obstacles_group.draw(screen)

    pygame.draw.rect(screen, GREEN,
                     (player1.rect.x, player1.rect.y - health_bar_offset, player1_health / 100 * player1.rect.width, health_bar_height))
    pygame.draw.rect(screen, GREEN,
                     (player2.rect.x, player2.rect.y - health_bar_offset, player2_health / 100 * player2.rect.width, health_bar_height))

    if winner_text:
        text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(winner_text, text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(30)
