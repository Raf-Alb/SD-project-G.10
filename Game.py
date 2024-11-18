# Game.py
import pygame
import sys
import os
from player import Player
from stone import create_stones, detect_collision
from background import update_background
from bee import create_bees, update_bee, draw_bee

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bee Running")

# Charger les ressources
background = pygame.image.load('Fond jeu.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
stone_image = pygame.image.load('stone.png').convert_alpha()

# Police pour l'écran
font_large = pygame.font.SysFont("courier new", 62)
font_score = pygame.font.SysFont("arial", 36)
TEXTCOLOR = (225, 225, 225)  # Blanc

# Fonction pour quitter proprement
def terminate():
    pygame.quit()
    sys.exit()

# Fonction pour attendre une action de l'utilisateur
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

# Fonction pour afficher du texte (score) sur l'écran
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

# Fonction pour afficher l'écran de démarrage
def show_start_screen():
    # Afficher l'image de fond du jeu
    screen.blit(background, (0, 0))  # Affiche le fond à la position (0, 0)

    # Texte "Bee Running"
    text_surface1 = font_large.render("Bee Running", True, (0, 40, 0))
    text_surface2 = font_large.render("Press a key to start", True, (0, 40, 0))
    text_rect1 = text_surface1.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    text_rect2 = text_surface2.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 50))

    # Afficher les textes sur l'écran
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)

    pygame.display.update()  # Mettre à jour l'affichage
    waitForPlayerToPressKey()  # Attendre une action de l'utilisateur


# Fonction pour afficher l'écran Game Over avec animation
def show_game_over_screen(score, top_score):
    # Texte "GAME OVER" en haut
    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))  # Position plus haute

    # Texte du score
    score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Score centré

    # Texte du top score
    top_score_text = font_score.render(f"Top Score: {top_score}", True, (255, 255, 255))
    top_score_rect = top_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    # Texte des instructions pour redémarrer
    restart_text = font_score.render("Press any key to restart", True, (200, 200, 200))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    # Dessiner l'écran noir avec les textes
    screen.fill((0, 0, 0))  # Fond noir
    screen.blit(game_over_text, game_over_rect)  # Texte "GAME OVER"
    screen.blit(score_text, score_rect)         # Score
    screen.blit(top_score_text, top_score_rect) # Top score
    screen.blit(restart_text, restart_rect)     # Instructions

    pygame.display.update()
    waitForPlayerToPressKey()  # Attend que le joueur appuie sur une touche


# Afficher l'écran de démarrage
show_start_screen()

# Paramètres du joueur et du jeu
player_floor = 510  # Sol pour le joueur
stone_floor = 500   # Sol pour les pierres
scroll_speed = 2
gravity = 1
default_gravity = gravity
score_increment = 1

# Variables globales pour les scores
top_score = 0

# Boucle principale
while True:
    # Réinitialisation des variables pour une nouvelle partie
    score = 0
    player_x = 100
    player_instance = Player(player_floor, gravity, image_folder="player_frames")
    stones = create_stones(stone_image, WIDTH, stone_floor, num_stones=3, min_distance=400)
    bees = create_bees(WIDTH, y_range=(20, 300), num_bees=2, min_distance=500, image_folder="bee_frame")
    bg_x1, bg_x2 = 0, background.get_width()
    running = True

    # Boucle de jeu
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        # Gestion des touches
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5
        if keys[pygame.K_SPACE]:
            player_instance.jump()

        # Appliquer la gravité
        if keys[pygame.K_DOWN]:
            gravity = 3
        else:
            gravity = default_gravity
        player_instance.gravity = gravity
        player_instance.update()

        # Empêcher le joueur de sortir des limites
        player_x = max(0, min(player_x, WIDTH - player_instance.width))

        # Vérifier si le joueur sort de l'écran à gauche
        if player_x <= 0:
            running = False

        # Défilement et collisions des pierres
        for stone in stones:
            stone["x"] -= scroll_speed
            if stone["x"] + stone["width"] < 0:
                stone["x"] = max([s["x"] for s in stones]) + stone["width"] + 400
            if detect_collision(player_x, player_instance.y, player_instance, stone):
                player_x -= 50

        # Défilement et collisions des abeilles
        for bee in bees:
            update_bee(bee, WIDTH)
            if detect_collision(player_x, player_instance.y, player_instance, bee):
                running = False

        # Mise à jour du fond
        bg_x1, bg_x2 = update_background(bg_x1, bg_x2, background.get_width(), scroll_speed)

        # Affichage des éléments
        screen.blit(background, (bg_x1, 0))
        screen.blit(background, (bg_x2, 0))
        for stone in stones:
            screen.blit(stone["image"], (stone["x"], stone["y"]))
        for bee in bees:
            draw_bee(screen, bee)
        player_instance.draw(screen, player_x)

        # Affichage des scores
        draw_text(screen, f"Score: {score}", font_score, TEXTCOLOR, 10, 10)
        draw_text(screen, f"Top Score: {top_score}", font_score, TEXTCOLOR, 10, 50)

        # Mise à jour de l'écran
        pygame.display.flip()
        pygame.time.Clock().tick(60)

        # Mise à jour du score
        score += score_increment * scroll_speed

    # Fin de la partie
    if score > top_score:
        top_score = score
    show_game_over_screen(score, top_score)


  




