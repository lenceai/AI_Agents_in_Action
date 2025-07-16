######################
import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 5, 10
BULLET_SPEED = 7

# Colors
SAND_COLOR = (194, 178, 128)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dune Inspired Game")

# Load images
#player_image = pygame.image.load(os.path.join('player.png')).convert_alpha()
#bullet_image = pygame.image.load(os.path.join('bullet.png')).convert_alpha()

# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)

    def move(self, dx):
        if 0 <= self.rect.x + dx <= SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x += dx

    def draw(self, surface):
        #surface.blit(player_image, self.rect)
        pygame.draw.rect(surface, (0, 0, 255), self.rect)  # Blue rectangle for player

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)

    def update(self):
        self.rect.y -= BULLET_SPEED

    def draw(self, surface):
        #surface.blit(bullet_image, self.rect)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)  # Red rectangle for bullet

# Game loop
def main():
    clock = pygame.time.Clock()
    player = Player()
    bullets = []
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-5)
        if keys[pygame.K_RIGHT]:
            player.move(5)
        if keys[pygame.K_SPACE]:
            bullets.append(Bullet(player.rect.centerx - BULLET_WIDTH // 2, player.rect.top))

        # Update bullets
        bullets = [bullet for bullet in bullets if bullet.rect.y > 0]  # Remove bullets off the top of the screen
        for bullet in bullets:
            bullet.update()

        # Drawing
        screen.fill(SAND_COLOR)
        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()