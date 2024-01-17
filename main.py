import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Battle Game")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, direction):
        super().__init__()
        self.image = pygame.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = direction

    def update(self):
        if self.direction == "left":
            self.image = pygame.transform.flip(pygame.transform.scale(player2_image, (100, 100)), True, False)
        else:
            self.image = pygame.transform.scale(player2_image, (100, 100))


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


all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

player1_image = pygame.image.load("dino.png")
player2_image = pygame.image.load("dino.png")

player1 = Player(50, HEIGHT // 2 - 25, player1_image, 5, "right")
player2 = Player(WIDTH - 100, HEIGHT // 2 - 25, player2_image, 5, "left")
all_sprites.add(player1, player2)
player_sprites.add(player1, player2)

player1_health = 100
player2_health = 100

health_bar_width = 50
health_bar_height = 5
health_bar_offset = 20

bullet_speed = 10

font = pygame.font.Font(None, 36)
winner_text = None

game_over = False

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
                player1.rect.topleft = (50, HEIGHT // 2 - 25)
                player2.rect.topleft = (WIDTH - 100, HEIGHT // 2 - 25)
                player1_health = 100
                player2_health = 100
                game_over = False
                winner_text = None

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_w] and player1.rect.top > 0:
            player1.rect.y -= player1.speed
        if keys[pygame.K_s] and player1.rect.bottom < HEIGHT:
            player1.rect.y += player1.speed
        if keys[pygame.K_a] and player1.rect.left > 0:
            player1.rect.x -= player1.speed
            player1.direction = "left"
        if keys[pygame.K_d] and player1.rect.right < WIDTH:
            player1.rect.x += player1.speed
            player1.direction = "right"

        if keys[pygame.K_UP] and player2.rect.top > 0:
            player2.rect.y -= player2.speed
        if keys[pygame.K_DOWN] and player2.rect.bottom < HEIGHT:
            player2.rect.y += player2.speed
        if keys[pygame.K_LEFT] and player2.rect.left > 0:
            player2.rect.x -= player2.speed
            player2.direction = "left"
        if keys[pygame.K_RIGHT] and player2.rect.right < WIDTH:
            player2.rect.x += player2.speed
            player2.direction = "right"

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

    pygame.draw.rect(screen, GREEN,
                     (player1.rect.x, player1.rect.y - health_bar_offset, player1_health, health_bar_height))
    pygame.draw.rect(screen, GREEN,
                     (player2.rect.x, player2.rect.y - health_bar_offset, player2_health, health_bar_height))

    if winner_text:
        text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(winner_text, text_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(30)
