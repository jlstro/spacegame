import pygame
import os
pygame.font.init()
pygame.mixer.init()

# Game window, dimensions 
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('space game')
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT) # Barrier in the middle of the screen

# Load sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shot.wav'))

# RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 5 #Velocity
BULLET_VEL = 7 # Bullet Velocity
AMMO = 5 # max number of bullets on screen at same time for each player

# Load fonts and declare size
HEALTH_FONT = pygame.font.SysFont('Ani', 40)
WINNER_FONT = pygame.font.SysFont('Ani', 80)

# Collision event if hit
YELLOW_HIT = pygame.USEREVENT + 1 
RED_HIT = pygame.USEREVENT +2

# Load sprites, background
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP, 90) # make spaceships face each other

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'red.png'))
RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP, 270) # make spaceships face each other

SPACE = pygame.image.load(os.path.join('Assets', 'space.png')) # Background image
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0)) # draw background
    pygame.draw.rect(WIN, BLACK, BORDER) # draw barrier in middle

    # draw health indicators
    red_health_text = HEALTH_FONT.render("Power: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Power: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # draw the spaceships and each bullet in bullet lists
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # Left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + SPACESHIP_WIDTH < BORDER.x + 15: # Right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # Up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + SPACESHIP_HEIGHT < HEIGHT - 15: # Down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # Left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - SPACESHIP_WIDTH + 15: # Right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + SPACESHIP_HEIGHT < HEIGHT - 15: # Down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL # move each bullet with BULLET_VEL
        if red.colliderect(bullet): # check collissions
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH: # check if bullet left screen
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL # move each bullet with BULLET_VEL
        if yellow.colliderect(bullet): # check collissions
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0: # check if bullet left screen
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update() # draw winner
    pygame.time.delay(5000) # pause game for 5 secs



def main():
    # create hitboxes
    red = pygame.Rect(700, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # init bullet lists
    red_bullets = []
    yellow_bullets = []

    # init health
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock() 
    run = True
    while run:
        clock.tick(FPS) # make sure while loop is capped at FPS value
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close window when user clicks X
                run = False
                pygame.quit()
            
            # check if player hit fire then add bullet to list
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < AMMO:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < AMMO:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # bullet handler function checks collission, updates events
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # initialize winner text and fill in when health lower than 1
        winner_text = ""
        if red_health < 1:
            winner_text = "YELLOW HAS WON"

        if yellow_health < 1:
            winner_text = "RED HAS WON"
        
        if winner_text != "":
            draw_winner(winner_text)
            break # break loop when winner declared

        # pygame.key.get_pressed() can handle multiple keystrokes at the same time
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        # draw it all
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main() #restart game after win

if __name__ == "__main__":
    main()