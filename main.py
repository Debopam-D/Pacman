import pygame
import sys
from random import randint

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pac-Man settings
pacman_radius = 15
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
pacman_speed = 10

# Food settings
food_radius = 5
food_x, food_y = randint(food_radius, WIDTH - food_radius), randint(food_radius, HEIGHT - food_radius)

# Obstacles for levels
levels = [
    # Level 1: Simple obstacle
    [pygame.Rect(200, 150, 200, 20)],

    # Level 2: Two horizontal barriers
    [pygame.Rect(150, 100, 300, 20), pygame.Rect(150, 250, 300, 20)],

    # Level 3: Maze-like structure
    [
        pygame.Rect(100, 50, 400, 20),
        pygame.Rect(100, 330, 400, 20),
        pygame.Rect(200, 150, 20, 100),
        pygame.Rect(380, 150, 20, 100)
    ]
]

current_level = 0
obstacles = levels[current_level]

# Timer and Score
score = 0
font = pygame.font.Font(None, 36)
total_time = 60  # 60 seconds to play
start_ticks = pygame.time.get_ticks()

# Game loop
clock = pygame.time.Clock()

def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), pacman_radius)

def draw_food(x, y):
    pygame.draw.circle(screen, RED, (x, y), food_radius)

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, obstacle)

def display_info(score, level, time_left):
    text = font.render(f"Score: {score} | Level: {level + 1} | Time: {time_left}s", True, WHITE)
    screen.blit(text, (10, 10))

running = True
while running:
    screen.fill(BLACK)

    # Calculate remaining time
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = total_time - elapsed_time

    if time_left <= 0:
        print("Time's up! Game over.")
        print(f"Your final score: {score}")
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement keys
    keys = pygame.key.get_pressed()
    new_x, new_y = pacman_x, pacman_y
    if keys[pygame.K_LEFT]:
        new_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        new_x += pacman_speed
    if keys[pygame.K_UP]:
        new_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        new_y += pacman_speed

    # Check collision with obstacles
    pacman_rect = pygame.Rect(new_x - pacman_radius, new_y - pacman_radius, pacman_radius * 2, pacman_radius * 2)
    collision = any(pacman_rect.colliderect(obstacle) for obstacle in obstacles)

    if collision:
        print("You hit an obstacle! Game over.")
        print(f"Your final score: {score}")
        running = False

    # Update Pac-Man's position if no collision with obstacles
    if not collision:
        pacman_x, pacman_y = new_x, new_y

    # Check collision with food
    distance = ((pacman_x - food_x)**2 + (pacman_y - food_y)**2)**0.5
    if distance < pacman_radius + food_radius:
        score += 1
        # Move the food to a new random position
        food_x = randint(food_radius, WIDTH - food_radius)
        food_y = randint(food_radius, HEIGHT - food_radius)

        # Progress to the next level
        if score % 5 == 0:  # Every 5 points, go to the next level
            current_level += 1
            if current_level < len(levels):
                obstacles = levels[current_level]
            else:
                print("You completed all levels!")
                running = False

    # Draw everything
    draw_pacman(pacman_x, pacman_y)
    draw_food(food_x, food_y)
    draw_obstacles(obstacles)
    display_info(score, current_level, time_left)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
