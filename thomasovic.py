import pygame
import sys

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Charger l'image du fond
background = pygame.image.load('/Users/thomadessarzin/Desktop/SD-project-G.10/Fond jeu.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Charger l'image du player
player = pygame.image.load('/Users/thomadessarzin/Desktop/SD-project-G.10/penis.png').convert_alpha()  # convert_alpha() pour conserver la transparence
# Redimensionner le player (par exemple à 50x50 pixels)
player_width = 70  # Nouvelle largeur
player_height = 70  # Nouvelle hauteur
player = pygame.transform.scale(player, (player_width, player_height))

# Positionner le joueur initialement
player_x = 100  # Position horizontale du joueur
player_y = 500  # Position verticale du joueur 

# Vitesse de défilement
scroll_speed = 2

# Position initiale du fond
bg_x1 = 0
bg_x2 = background.get_width()

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Mettre à jour la position des deux images de fond
    bg_x1 -= scroll_speed
    bg_x2 -= scroll_speed

    # Si l'une des images sort de l'écran, la replacer à droite de l'autre
    if bg_x1 <= -background.get_width():
        bg_x1 = bg_x2 + background.get_width()
    if bg_x2 <= -background.get_width():
        bg_x2 = bg_x1 + background.get_width()

    # Empêcher le joueur de descendre en dessous de la terre (on considère ici que la "terre" commence à y=450)
    if player_y > 450:
        player_y = 450

    # DESSINER LE FOND D'ABORD
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))

    # DESSINER LE PLAYER ENSUITE (PAR-DESSUS LE FOND)
    screen.blit(player, (player_x, player_y))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la vitesse de rafraîchissement
    pygame.time.Clock().tick(60)


