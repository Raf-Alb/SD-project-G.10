# Game.py
import pygame
import sys
from player import Player
from stone import create_stones, detect_collision
from background import update_background
from bee import create_bees, update_bee, draw_bee  # Importer les fonctions pour gérer les abeilles

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Charger les images
background = pygame.image.load('Fond jeu.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
stone_image = pygame.image.load('stone.png').convert_alpha()

# Police pour l'écran d'accueil
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

# Fonction pour afficher l'écran de démarrage            
def show_start_screen():
    screen.fill((0, 100, 25))  # Fond vert
    text_surface1 = font_large.render("Bee Running", True, TEXTCOLOR)
    text_surface2 = font_large.render("Press a key to start", True, TEXTCOLOR)
    text_rect1 = text_surface1.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    text_rect2 = text_surface2.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 50))
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)
    pygame.display.update()
    waitForPlayerToPressKey()


# Fonction pour afficher du texte (score) sur l'écran
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_rect)

# Afficher l'écran de démarrage
show_start_screen()

# Positions de sol pour le joueur et les pierres
player_floor = 510  # Sol visuel pour le joueur (ajusté pour marcher sur la terre)
stone_floor = 500   # Sol pour les pierres

# Paramètres du joueur et du jeu
player_x = 100
scroll_speed = 2
gravity = 1
default_gravity = gravity

# Initialiser le score
score = 0
top_score = 0 
score_increment = 1 # Points ajoutés à chaque cycle de jeu

# Créer une instance du joueur
player_instance = Player(player_floor, gravity, image_folder="player_frames")

# Créer les pierres
stones = create_stones(stone_image, WIDTH, stone_floor, num_stones=3, min_distance=400)

# Créer des abeilles ennemies avec animation et redimensionnement
bees = create_bees(WIDTH, y_range=(20, 300), num_bees=2, min_distance=500, image_folder="bee_frame") 

# Initialiser les positions du fond pour le défilement
bg_x1 = 0
bg_x2 = background.get_width()

# Boucle principale du jeu
running = True
while running:
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
    player_x = max(0, min(player_x, WIDTH - player_instance.width))

    # Mettre à jour les positions du fond
    bg_x1, bg_x2 = update_background(bg_x1, bg_x2, background.get_width(), scroll_speed)

    # Faire défiler les pierres et vérifier les collisions
    for stone in stones:
        stone["x"] -= scroll_speed
        if stone["x"] + stone["width"] < 0:
            # Réinitialiser la pierre qui sort de l'écran
            stone["x"] = max([s["x"] for s in stones]) + stone["width"] + 400

        # Vérifier la collision
        if detect_collision(player_x, player_instance.y, player_instance, stone):
            print("Collision avec une pierre !")
            player_x -= 50  # Collision, reculer le joueur

    # Mise à jour de l'affichage
    # Dessiner le fond en premier
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))

    # Dessiner les abeilles
    for bee in bees:
        update_bee(bee,  WIDTH)  # Mettre à jour la position et l'animation de l'abeille
        draw_bee(screen, bee)  # Dessiner l'abeille animée

        # Vérifier la collision avec l'abeille
        if detect_collision(player_x, player_instance.y, player_instance, bee):
            print("Collision avec une abeille ! Game Over")
            running = False  # Arrêter le jeu en cas de collision avec l'abeille

    # Dessiner les pierres
    for stone in stones:
        screen.blit(stone["image"], (stone["x"], stone["y"]))

    # Dessiner le joueur avec l'animation
    player_instance.draw(screen, player_x)

    # Afficher le score et le top score **APRÈS** tous les éléments visuels
    draw_text(screen, f"Score: {score}", font_score, TEXTCOLOR, 10, 10)
    draw_text(screen, f"Top Score: {top_score}", font_score, TEXTCOLOR, 10, 50)
    
    # Mettre à jour l'affichage
    pygame.display.flip()
    pygame.time.Clock().tick(60)

    # Mettre à jour le score
    score += score_increment * scroll_speed

# Mettre à jour le top score si nécessaire
if score > top_score:
    top_score = score

