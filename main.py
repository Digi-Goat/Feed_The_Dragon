import pygame
import random

# Set display surface
pygame.init()

# Set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed The Dragon")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

# Set Game Variables
score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set fonts
font = pygame.font.Font('assets/AttackGraffiti.ttf', 32)

# Set Text for Score
score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

# Set Text for Title (Similar to Score)
title_text = font.render("Feed the Dragon: ", True, GREEN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.y = 10

# Set Text for Lives
lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

# Set Text for Game Over
game_over_text = font.render("GAMEOVER", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Set Text for Continue
continue_text = font.render("Press any key to play again", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 32)

# Set the sound and music
coin_sound = pygame.mixer.Sound('assets/coin_sound.wav')
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
miss_sound.set_volume(0.1)
pygame.mixer.music.load('assets/ftd_background_music.wav')

# Set the images
player_image = pygame.image.load("assets/dragon_right.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT // 2

coin_image = pygame.image.load("assets/coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

# Start background music
pygame.mixer.music.play(-1, 0.0)

# Function to reset coin position
def reset_coin():
    coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

# The main game loop
running = True
while running:
    # Check for user input/events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player (Dragon movement logic)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    # Move the coin independently from dragon movement
    coin_rect.x -= coin_velocity  # Always move the coin to the left

    # Check if the coin goes off the screen (missed coin)
    if coin_rect.x < 0:
        miss_sound.play()
        player_lives -= 1
        reset_coin()

    # Check for collision with the coin
    if player_rect.colliderect(coin_rect):
        coin_sound.play()
        score += 1
        reset_coin()
        coin_velocity += COIN_ACCELERATION

    # Update the score and lives text
    score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
    lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)

    # Fill the display
    display_surface.fill(BLACK)

    # Blit text and images
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)

    # Check for game over
    if player_lives <= 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until player presses a key
        pygame.mixer.music.stop()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    # Reset game values
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    coin_velocity = COIN_STARTING_VELOCITY
                    reset_coin()
                    pygame.mixer.music.play(-1, 0.0)
                    waiting = False

    # Update display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()