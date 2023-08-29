import random

import pygame

# Start the game
pygame.init()

width = 800
height = 800
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Space Game")

# My aircraft
aircraft_image = pygame.image.load("my_spacecraft.png")
aircraft_image = pygame.transform.scale(aircraft_image, (150, 150))
aircraft_rect = aircraft_image.get_rect()
aircraft_rect.center = (width // 2, height - 50)

# Enemy aircraft
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (150, 150))
enemy_rect = enemy_image.get_rect()
enemy_rect.center = (random.randint(0, width), -50)

# Shot
shot_image = pygame.image.load("shot.png")
shot_image = pygame.transform.scale(shot_image, (50, 50))
shot_rect = shot_image.get_rect()

score = 0
lives = 3
continueGame = True

# Convert the images to use masks for pixel-perfect collision detection
aircraft_mask = pygame.mask.from_surface(aircraft_image)
enemy_mask = pygame.mask.from_surface(enemy_image)
shot_mask = pygame.mask.from_surface(shot_image)

font = pygame.font.Font(None, 36)

aircraft_speed = 3
enemy_speed = 2
shot_speed = 5

while continueGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continueGame = False

    # Move my aircraft
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        aircraft_rect.x -= aircraft_speed
    if keys[pygame.K_RIGHT]:
        aircraft_rect.x += aircraft_speed
    if keys[pygame.K_UP]:
        aircraft_rect.y -= aircraft_speed
    if keys[pygame.K_DOWN]:
        aircraft_rect.y += aircraft_speed
    if keys[pygame.K_SPACE]:
        shot_rect.center = aircraft_rect.center

    # Keep the aircraft within the screen boundaries
    aircraft_rect.x = max(-30, min(aircraft_rect.x, width - aircraft_rect.width + 30))
    aircraft_rect.y = max(300, min(aircraft_rect.y, height - aircraft_rect.height))

    # Update the shot's position
    if shot_rect.y > 0:
        shot_rect.y -= shot_speed

    # Update the enemy's position
    enemy_rect.y += enemy_speed
    if enemy_rect.top > height:
        enemy_rect.center = (random.randint(0, width), -50)
        lives -= 1

    # Check for pixel-perfect collision using masks
    offset_shot_enemy = (enemy_rect.x - shot_rect.x, enemy_rect.y - shot_rect.y)
    if aircraft_mask.overlap(enemy_mask, offset_shot_enemy):
        enemy_rect.center = (random.randint(0, width), 50)
        shot_rect.y = -shot_rect.height
        score += 1

    offset_me_enemy = (enemy_rect.x - aircraft_rect.x, enemy_rect.y - aircraft_rect.y)
    if aircraft_mask.overlap(enemy_mask, offset_me_enemy):
        print("Game Over")
        print("Score: " + str(score))
        continueGame = False

    screen.fill((0, 0, 0))

    screen.blit(pygame.image.load("background.jpeg"), (0, 0))
    screen.blit(aircraft_image, aircraft_rect)
    screen.blit(enemy_image, enemy_rect)
    if shot_rect.y > 0:
        screen.blit(shot_image, shot_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (width - score_text.get_width() - 10, 10))

    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
