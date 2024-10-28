# Game.py
import pygame
import sys
from player import Player
from stone import create_stones, detect_collision
from background import update_background

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Charger les images
background = pygame.image.load('Fond jeu.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
stone_image = pygame.image.load('stone.png').convert_alpha()

# Positions de sol pour le joueur et les pierres
player_floor = 510  # Sol visuel pour le joueur (ajusté pour marcher sur la terre)
stone_floor = 500   # Sol pour les pierres

# Paramètres du joueur et du jeu
player_x = 100
player_width = 60
player_height = 60
scroll_speed = 2
gravity = 1
default_gravity = gravity

# Créer une instance du joueur avec `player_floor` pour marcher sur le sol
player_instance = Player(player_floor, gravity, image_folder="player_frames")

# Créer les pierres en utilisant `stone_floor` pour les positionner correctement
stones = create_stones(stone_image, WIDTH, stone_floor, num_stones=3, min_distance=400)

# Initialiser les positions du fond pour le défilement
bg_x1 = 0
bg_x2 = background.get_width()

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturer les touches pressées
    keys = pygame.key.get_pressed()

    # Déplacer le joueur à droite et à gauche
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

    # Mettre à jour le joueur (position + animation)
    player_instance.update()

    # Empêcher le joueur de sortir de l'écran
    player_x = max(0, min(player_x, WIDTH - player_width))

    # Mettre à jour les positions du fond
    bg_x1, bg_x2 = update_background(bg_x1, bg_x2, background.get_width(), scroll_speed)

    # Faire défiler les obstacles et vérifier les collisions
    for stone in stones:
        stone["x"] -= scroll_speed
        if stone["x"] + stone["width"] < 0:
            # Réinitialiser la pierre qui sort de l'écran
            stone["x"] = max([s["x"] for s in stones]) + stone["width"] + 400  # Espacement de 400 pixels

        # Vérifier la collision
        if detect_collision(player_x, player_instance.y, player_instance, stone):
            print("Collision détectée!")
            player_x -= 50  # Collision, reculer le joueur

    # Affichage
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))
    player_instance.draw(screen, player_x)  # Dessiner le joueur avec l'animation
    for stone in stones:
        screen.blit(stone["image"], (stone["x"], stone["y"]))

    pygame.display.flip()
    pygame.time.Clock().tick(60)


