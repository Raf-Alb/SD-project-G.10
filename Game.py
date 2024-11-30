# Game.py
import pygame, sys
import os
from player import Player
from stone import create_stones, detect_collision
from background import update_background
from bee import create_bees, update_bee, draw_bee
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (225, 225, 225)  #white

# Function for quitting properly
def terminate():
    pygame.quit()
    sys.exit()

# Function strating the game
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

# Function to draw score on screen
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

# Start Pygame
pygame.init()
# Window size
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Bee Running")

# Download background
background = pygame.image.load('Fond jeu.png').convert()
background = pygame.transform.scale(background, (WINDOWWIDTH, WINDOWHEIGHT))  #allows to adjust the background image to the window size  
stone_image = pygame.image.load('stone.png').convert_alpha()

# font creation
font_large = pygame.font.SysFont("courier new", 62)
font_score = pygame.font.SysFont("arial", 36)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Function to set start screen
def show_start_screen():
    # Show the background picture
    screen.blit(background, (0, 0))  # sets background at (0, 0) position

    # Initial text "Bee Running"
    text_surface1 = font_large.render("Bee Running", True, (0, 40, 0))
    text_surface2 = font_large.render("Press a key to start", True, (0, 40, 0))
    text_rect1 = text_surface1.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 3))
    text_rect2 = text_surface2.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 3 + 50))

    # Show text on screen
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)

    pygame.display.update()  # Update the display
    waitForPlayerToPressKey()  # Wait for player to start the game


# Fonction for Game Over screen
def show_game_over_screen(score, top_score):
    # Text "GAME OVER" 
    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4))  # higher position

    # Text for score
    score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))  # score in the middle

    # Text for top score
    top_score_text = font_score.render(f"Top Score: {top_score}", True, (255, 255, 255))
    top_score_rect = top_score_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 50))

    # Text for restart instructions
    restart_text = font_score.render("Press any key to restart", True, (200, 200, 200))
    restart_rect = restart_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 100))

    # Game over final display
    screen.fill((0, 0, 0))  #Black background
    screen.blit(game_over_text, game_over_rect)  # Text "GAME OVER"
    screen.blit(score_text, score_rect)         # Score
    screen.blit(top_score_text, top_score_rect) # Top score
    screen.blit(restart_text, restart_rect)     # Instructions

    pygame.display.update()
    waitForPlayerToPressKey() # Wait for player to start the game


# Show starting screen
show_start_screen()

# Player and game settings
player_floor = 510  # choose player's floor level
stone_floor = 500   # choose stones' floor level
scroll_speed = 2
gravity = 1
default_gravity = gravity
score_increment = 1

# set first top score
top_score = 0

# Main loop
while True:
    #Set up the start of the game
    score = 0
    player_x = 100
    player_instance = Player(player_floor, gravity, image_folder="player_frames")
    stones = create_stones(stone_image, WINDOWWIDTH, stone_floor, num_stones=3, min_distance=400) #settings for stones creation
    bees = create_bees(WINDOWWIDTH, y_range=(20, 300), num_bees=2, min_distance=500, image_folder="bee_frame") #settings for bees creation
    bg_x1, bg_x2 = 0, background.get_width() #allows the background to follow the screen 
    running = True #the player starts running
    pygame.mixer.music.play(-1, 0.0)


    # Game loop
    while running: # The game loop runs while the game part is playing.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        # the keys that allow the player to move 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5
        if keys[pygame.K_SPACE]:
            player_instance.jump()

        # Increases gravity
        if keys[pygame.K_DOWN]:
            gravity = 3
        else:
            gravity = default_gravity #applies normal gravity
        player_instance.gravity = gravity
        player_instance.update()

        # prevents the player from getting out of the screen
        player_x = max(0, min(player_x, WINDOWWIDTH - player_instance.width))

        # Stops the game if the player cannot stay on the left side of the screen
        if player_x <= 0:
            running = False
        
         # increases difficulty of the game
        if score % 500 == 0:  # each 500 points
            scroll_speed += 1  # increases the scroll speed
        
        # Upload the bees
        for bee in bees:
            bee["x"] -= scroll_speed  # allows the bees to follow the speed of the screen

        # Scrolling and collision for stones
        for stone in stones:
            stone["x"] -= scroll_speed
            if stone["x"] + stone["width"] < 0:
                stone["x"] = max([s["x"] for s in stones]) + stone["width"] + 400
            if detect_collision(player_x, player_instance.y, player_instance, stone):
                player_x -= 50

        # Scrolling and collision for bees
        for bee in bees:
            update_bee(bee, WINDOWWIDTH)
            if detect_collision(player_x, player_instance.y, player_instance, bee):
                running = False #stops the game if there is a collision

        # updating the background to follow the scrolling speed
        bg_x1, bg_x2 = update_background(bg_x1, bg_x2, background.get_width(), scroll_speed)

        # For game fluidity
        screen.blit(background, (bg_x1, 0))
        screen.blit(background, (bg_x2, 0))
        for stone in stones:
            screen.blit(stone["image"], (stone["x"], stone["y"]))
        for bee in bees:
            draw_bee(screen, bee)
        player_instance.draw(screen, player_x)

        # Show scores
        draw_text(screen, f"Score: {score}", font_score, TEXTCOLOR, 10, 10)
        draw_text(screen, f"Top Score: {top_score}", font_score, TEXTCOLOR, 10, 50)

        # Screen upload
        pygame.display.flip()
        pygame.time.Clock().tick(60)

        # Score upload
        score += score_increment * scroll_speed

    # end of the game
    pygame.mixer.music.stop()
    if score > top_score:
        top_score = score
    gameOverSound.play()
    show_game_over_screen(score, top_score)
    scroll_speed = 2  # Reset the scroll speed after Game Over

    gameOverSound.stop()
    
     



#Background : https://fr.vecteezy.com/art-vectoriel/4277175-foret-jeu-fond
#Abeille : https://pixabay.com/gifs/wasp-hornet-insect-fly-pixel-art-12292/
#Personnage : https://www.gifsanimes.com/img-course-a-pied-image-animee-0008-60786.htm
#Rocher : https://fr.vecteezy.com/png/8502483-pierres-de-roche-et-rochers-de-style-dessin-anime 



