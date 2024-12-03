# bee.py
import pygame
import os
import random
import math

class Bee:
    def __init__(self, x, y, speed, images, animation_speed):
        """Initialise une abeille avec ses propriétés."""
        self.x = x
        self.y = y
        self.speed = speed
        self.speed_multiplier = random.uniform(1, 2)  # Multiplier de vitesse entre 1x et 2x
        self.images = images
        self.current_image = 0
        self.animation_counter = 0
        self.animation_speed = animation_speed
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.mask = pygame.mask.from_surface(self.images[0])

    def update(self, screen_width, player_y=None, scroll_speed=2):
        """Met à jour la position et l'animation de l'abeille."""
        # Déplacement horizontal proportionnel à la vitesse du fond
        self.x -= scroll_speed * self.speed_multiplier

        # Suivre le joueur en ajustant la position verticale
        if player_y is not None:
            tracking_speed = 1.5  # Limite la vitesse verticale
            if self.y < player_y:
                self.y += min(tracking_speed, abs(player_y - self.y))
            elif self.y > player_y:
                self.y -= min(tracking_speed, abs(player_y - self.y))

        # Ajouter un mouvement sinusoïdal pour dynamisme
        self.y += math.sin(pygame.time.get_ticks() / 500) * 2

        # Animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.animation_counter = 0
            self.mask = pygame.mask.from_surface(self.images[self.current_image])

        # Réinitialisation si l'abeille sort de l'écran
        if self.x + self.width < 0:
            self.reset(screen_width)

    def reset(self, screen_width):
        """Réinitialise l'abeille lorsqu'elle sort de l'écran."""
        self.x = screen_width + random.randint(100, 300)
        self.y = random.randint(20, 300)
        self.speed = random.uniform(1.5, 3.0)  # Vitesse initiale aléatoire
        self.speed_multiplier = random.uniform(1, 2)  # Multiplier de vitesse entre 1x et 2x

    def draw(self, screen):
        """Dessine l'abeille sur l'écran."""
        screen.blit(self.images[self.current_image], (self.x, self.y))

    def detect_collision(self, player_x, player_y, player):
        """Vérifie la collision précise entre le joueur et cette abeille."""
        offset_x = self.x - player_x
        offset_y = self.y - player_y
        return player.mask.overlap(self.mask, (offset_x, offset_y))

def load_bee_images(folder, size=(50, 50)):
    """Charge toutes les images de l'abeille depuis un dossier et les redimensionne à une taille fixe."""
    images = []
    for img in sorted(os.listdir(folder)):
        if img.endswith(".png"):
            image = pygame.image.load(os.path.join(folder, img)).convert_alpha()
            images.append(pygame.transform.scale(image, size))
    return images

def create_bees(screen_width, y_range=(20, 300), num_bees=2, min_distance=500, image_folder="bee_frame", animation_speed=3):
    """Crée une liste d'instances d'abeilles avec des positions et vitesses aléatoires."""
    bees = []
    bee_images = load_bee_images(image_folder, size=(50, 50))  # Charger les frames de l'abeille
    current_x = screen_width + 150

    for _ in range(num_bees):
        bee_y = random.randint(*y_range)
        bee_x = current_x
        bee_speed = random.uniform(1.5, 3.0)
        bees.append(Bee(bee_x, bee_y, bee_speed, bee_images, animation_speed))
        current_x += 50 + min_distance

    return bees

