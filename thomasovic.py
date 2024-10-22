import pygame
import sys
import random

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Charger l'image du fond
background = pygame.image.load('Fond jeu.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Charger l'image du player
player = pygame.image.load('penis.png').convert_alpha()
# Redimensionner le player 
player_width = 60
player_height = 60
player = pygame.transform.scale(player, (player_width, player_height))

# Charger l'image de l'obstacle (stone)
stone_image = pygame.image.load('stone.png').convert_alpha()

# Position initiale du joueur
player_x = 100
player_y = 450

# Niveau du sol
floor = 450

# Définir la gravité et la vitesse
default_gravity = 1
gravity = default_gravity
player_speed = 5
scroll_speed = 2  # Vitesse de défilement du fond

# Initialiser les positions des images de fond
bg_x1 = 0
bg_x2 = background.get_width()

class Player:
    def __init__(self):
        self.y = floor
        self.y_speed = 0
        self.jumping = 0

    def jump(self):
        if self.jumping == 0:
            self.y_speed = -20
            self.jumping = 1
        elif self.jumping == 1 and self.y_speed >= 0:
            self.y_speed = -15
            self.jumping = 2
        elif self.jumping == 2 and self.y_speed >= 0:
            self.y_speed = -15
            self.jumping = 3

    def update(self):
        self.y_speed += gravity
        self.y = min(self.y + self.y_speed, floor)
        if self.y == floor:
            self.jumping = 0
            self.y_speed = 0

# Créer une instance du joueur
player_instance = Player()

# Fonction pour créer un stone avec une taille et une position aléatoires
def create_stone(stones, min_distance = 600):
    while True:
        stone_width = random.randint(40, 100)
        stone_height = stone_width
        stone_x = random.randint(WIDTH, WIDTH + 800)
        stone_y = floor 
        stone = pygame.transform.scale(stone_image, (stone_width, stone_height))
     
        # Vérifier que la nouvelle pierre n'est pas trop proche des autres
        too_close = False
        for other_stone in stones:
            if abs(stone_x - other_stone["x"]) < min_distance:
                too_close = True
                break        
        if not too_close:  # Si la pierre n'est pas trop proche des autres, on l'accepte
            return {"image": stone, "x": stone_x, "y": stone_y, "width": stone_width, "height": stone_height}

# Créer plusieurs stones
stones = []
for _ in range(3):
    stones.append(create_stone(stones, min_distance=600))  # Passer la liste des stones existants ici

# Fonction de détection de collision
def detect_collision(player_x, player_y, player_width, player_height, stone):
    return (player_x < stone["x"] + stone["width"] and
            player_x + player_width > stone["x"] and
            player_y < stone["y"] + stone["height"] and
            player_y + player_height > stone["y"])

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
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Sauter avec la touche espace 
    if keys[pygame.K_SPACE]:
        player_instance.jump()

    # Redescendre plus vite d'un saut
    if keys[pygame.K_DOWN]:
        gravity = 3
    else:
        gravity = default_gravity

    # Mettre à jour la position verticale avec la physique du saut
    player_instance.update()

    # Empêcher le joueur de sortir de l'écran
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width

    # Mettre à jour la position des deux images de fond
    bg_x1 -= scroll_speed
    bg_x2 -= scroll_speed

    if bg_x1 <= -background.get_width():
        bg_x1 = bg_x2 + background.get_width()
    if bg_x2 <= -background.get_width():
        bg_x2 = bg_x1 + background.get_width()

    # Faire défiler les stones
    for stone in stones:
        stone["x"] -= scroll_speed  # Faire défiler les stones avec le fond

        # Réinitialiser la position de la pierre lorsqu'elle sort de l'écran
        if stone["x"] + stone["width"] < 0:
            new_stone = create_stone(stones, min_distance=600)
            stone["x"] = new_stone["x"]
            stone["width"] = new_stone["width"]
            stone["image"] = new_stone["image"]
            stone["y"] = new_stone["y"]
            stone["height"] = new_stone["height"]

        # Vérifier la collision avec le joueur
    if detect_collision(player_x, player_instance.y, player_width, player_height, stone):
        print("Collision détectée! Game Over.")
    
    # Option pour afficher un message de Game Over
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        pygame.display.flip()
    
    # Attendre 2 secondes avant de quitter
        pygame.time.wait(2000)
        pygame.quit()  # Fermer Pygame après une pause
        sys.exit()  # Quitter proprement
    # DESSINER LE FOND
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))

    # DESSINER LE PLAYER
    screen.blit(player, (player_x, player_instance.y))

    # DESSINER LES STONES
    for stone in stones:
        screen.blit(stone["image"], (stone["x"], stone["y"]))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la vitesse de rafraîchissement
    pygame.time.Clock().tick(60)
