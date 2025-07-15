import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SNAKE_WIDTH, SNAKE_HEIGHT = 50, 50
DANGER_WIDTH, DANGER_HEIGHT = 50, 50
FPS = 30
FIRE_LIMIT = 10
OBJECTS_TO_DESTROY = 3

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

class GameOverException(Exception):
    pass

class Snake:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - SNAKE_HEIGHT, SNAKE_WIDTH, SNAKE_HEIGHT)
        self.fire_count = 0
        self.destroyed_objects = 0

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - SNAKE_WIDTH:
            self.rect.x = WIDTH - SNAKE_WIDTH

    def fire(self):
        if self.fire_count < FIRE_LIMIT:
            self.fire_count += 1
            return True
        return False

    def reset(self):
        self.rect.x = WIDTH // 2
        self.fire_count = 0
        self.destroyed_objects = 0

class Danger:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - DANGER_WIDTH), 0, DANGER_WIDTH, DANGER_HEIGHT)
        self.active = True

    def move(self):
        self.rect.y += 5
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH - DANGER_WIDTH)

    def deactivate(self):
        self.active = False

def check_game_over(snake, dangers):
    for danger in dangers:
        if danger.active and danger.rect.colliderect(snake.rect):
            raise GameOverException("Game Over! You hit a danger.")

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    dangers = [Danger() for _ in range(5)]
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            snake.move(-5)
        if keys[pygame.K_RIGHT]:
            snake.move(5)
        if keys[pygame.K_SPACE]:
            if snake.fire():
                for danger in dangers:
                    if danger.rect.colliderect(snake.rect) and danger.active:
                        snake.destroyed_objects += 1
                        danger.deactivate()  # Move out of screen to simulate destruction
                        if snake.destroyed_objects >= OBJECTS_TO_DESTROY:
                            game_over = True
                        break

        for danger in dangers:
            danger.move()

        try:
            check_game_over(snake, dangers)
        except GameOverException:
            game_over = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, snake.rect)
        for danger in dangers:
            if danger.active:
                pygame.draw.rect(screen, RED, danger.rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    while True:
        main()
        should_restart = input("Game over! Do you want to restart? (y/n): ")
        if should_restart.lower() != 'y':
            break