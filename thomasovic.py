import pygame
import sys

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Charger l'image du fond
background = pygame.image.load('Fond jeu.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Charger l'image du player
player = pygame.image.load('penis.png').convert_alpha()  # Assure-toi d'avoir la bonne image
# Redimensionner le player 
player_width = 60  # Nouvelle largeur
player_height = 60  # Nouvelle hauteur
player = pygame.transform.scale(player, (player_width, player_height))

# Position initiale du joueur
player_x = 100  # Position horizontale du joueur

# Définir la gravité et la position du sol
gravity = 1  # gravité (accélération vers le bas)
floor = 450  # position du sol en y (doit correspondre à la position Y du sol)

# Définir la vitesse du joueur et du défilement
player_speed = 5  # Vitesse du joueur (horizontal)
scroll_speed = 2  # Vitesse de défilement du fond

# Initialiser les positions des images de fond
bg_x1 = 0  # Position initiale du premier fond
bg_x2 = background.get_width()  # Position initiale du deuxième fond, à droite du premier

class Player():  # Adaptons la logique de la classe Frog pour le joueur
    def __init__(self):
        self.y = floor  # La position verticale initiale du joueur est sur le sol
        self.y_speed = 0  # vitesse verticale
        self.jumping = 0  # état du saut

    def jump(self):
        if self.jumping == 0:  # Saut initial (grand saut)
            self.y_speed = -20  # un grand saut (vers le haut, donc valeur négative)
            self.jumping = 1  # changer l'état du saut
        elif self.jumping == 1 and self.y_speed >= 0:  # Deuxième (plus grand saut)
            self.y_speed = -15  # un petit saut (valeur négative pour monter)
            self.jumping = 2  # changer l'état du saut
        elif self.jumping ==2 and self.y_speed >= 0 :# Troisième saut ( plus petit saut)
            self.y_speed = -15
            self.jumping = 3 

    def update(self):
        self.y_speed += gravity  # Appliquer la gravité (ralentit la montée, accélère la chute)
        self.y = min(self.y + self.y_speed, floor)  # Ne pas tomber sous le sol
        if self.y == floor:  # Le joueur touche le sol
            self.jumping = 0  # Réinitialiser l'état de saut
            self.y_speed = 0  # Réinitialiser la vitesse verticale

# Créer une instance du joueur
player_instance = Player()

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturer les touches pressées
    keys = pygame.key.get_pressed()

    # Déplacer le player à droite et à gauche (avec flèche)
    if keys[pygame.K_LEFT]:  # Si flèche gauche est pressée
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:  # Si flèche droite est pressée
        player_x += player_speed

    # Sauter avec la touche espace (utiliser la logique de saut de la classe)
    if keys[pygame.K_SPACE]:
        player_instance.jump()  # Appeler la méthode de saut

    # Mettre à jour la position verticale avec la physique du saut
    player_instance.update()

    # Empêcher le joueur de sortir de l'écran
    if player_x < 0:  # Ne pas aller à gauche en dehors de l'écran
        break 
    if player_x > WIDTH - player_width:  # Ne pas dépasser la droite de l'écran
        player_x = WIDTH - player_width

    # Mettre à jour la position des deux images de fond
    bg_x1 -= scroll_speed  # Déplacer la première image de fond vers la gauche
    bg_x2 -= scroll_speed  # Déplacer la deuxième image de fond vers la gauche

    # Si l'une des images sort de l'écran, la replacer à droite de l'autre
    if bg_x1 <= -background.get_width():
        bg_x1 = bg_x2 + background.get_width()
    if bg_x2 <= -background.get_width():
        bg_x2 = bg_x1 + background.get_width()

    # DESSINER LE FOND D'ABORD
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))

    # DESSINER LE PLAYER ENSUITE (PAR-DESSUS LE FOND)
    screen.blit(player, (player_x, player_instance.y))  # Utiliser la position y du saut

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la vitesse de rafraîchissement
    pygame.time.Clock().tick(60)
