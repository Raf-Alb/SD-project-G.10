# main.py
import pygame
import sys
from player_class import Player
from stone_class import create_stone, detect_collision
from background_class import update_background

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Charger les images
background = pygame.image.load('Fond jeu.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_image = pygame.image.load('penis.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (60, 60))
stone_image = pygame.image.load('stone.png').convert_alpha()

# Position initiale du joueur
player_x = 100
player_y = 450
player_width = 60
player_height = 60
floor = 450
scroll_speed = 2
gravity = 1
default_gravity = gravity

# Initialiser les positions du fond
bg_x1 = 0
bg_x2 = background.get_width()

# Créer une instance du joueur
player_instance = Player(floor, gravity)

# Créer les obstacles
stones = []
for _ in range(3):
    stones.append(create_stone(stone_image, WIDTH, floor))

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturer les touches pressées
    keys = pygame.key.get_pressed()

    # Déplacer le player à droite et à gauche
    if keys[pygame.K_LEFT]:
        player_x -= 5
    if keys[pygame.K_RIGHT]:
        player_x += 5

    # Sauter avec la touche espace
    if keys[pygame.K_SPACE]:
        player_instance.jump()

    # Redescendre plus vite
    if keys[pygame.K_DOWN]:
        gravity = 3
    else:
        gravity = default_gravity
    player_instance.gravity = gravity

    # Mettre à jour le joueur
    player_instance.update()

    # Empêcher le joueur de sortir de l'écran
    player_x = max(0, min(player_x, WIDTH - player_width))

    # Mettre à jour les positions du fond
    bg_x1, bg_x2 = update_background(bg_x1, bg_x2, background.get_width(), scroll_speed)

    # Faire défiler les obstacles
    for stone in stones:
        stone["x"] -= scroll_speed
        if stone["x"] + stone["width"] < 0:
            new_stone = create_stone(stone_image, WIDTH, floor)
            stone.update(new_stone)

        # Vérifier la collision
        if detect_collision(player_x, player_instance.y, player_width, player_height, stone):
            player_x -= 5  # Collision, reculer le joueur

    # Affichage
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))
    screen.blit(player_image, (player_x, player_instance.y))
    for stone in stones:
        screen.blit(stone["image"], (stone["x"], stone["y"]))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
