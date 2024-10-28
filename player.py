# player.py
import pygame
import os

class Player:
    def __init__(self, floor, gravity, image_folder, animation_speed=5):
        # Initialiser la position verticale du joueur pour que ses pieds soient sur le sol
        self.y = floor
        self.y_speed = 0
        self.jumping = 0
        self.floor = floor  # Hauteur du sol fixée
        self.gravity = gravity

        # Charger les images pour l'animation
        self.images = self.load_images(image_folder)
        self.current_image = 0

        # Taille du joueur (basée sur la première image)
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()

        # Créer un masque pour le joueur basé sur la première image
        self.mask = pygame.mask.from_surface(self.images[self.current_image])

        # Vitesse d'animation
        self.animation_speed = animation_speed
        self.animation_counter = 0

    def load_images(self, folder):
        #Charge toutes les images depuis un dossier
        images = [pygame.image.load(os.path.join(folder, img)) for img in sorted(os.listdir(folder)) if img.endswith(".png")]
        return images

    def jump(self):
        if self.jumping == 0:
            self.y_speed = -20  # Initialiser la vitesse du saut
            self.jumping = 1
        elif self.jumping == 1 and self.y_speed >= 0:
            self.y_speed = -15  # Double saut
            self.jumping = 2
        elif self.jumping == 2 and self.y_speed >= 0:
            self.y_speed = -15  # Triple saut
            self.jumping = 3

    def update(self):
        #Met à jour la position et l'animation du joueur
        self.y_speed += self.gravity  # Appliquer la gravité
        # Ajuster pour que les pieds soient sur le sol
        self.y = min(self.y + self.y_speed, self.floor - self.height)

        if self.y == self.floor - self.height:  # Si le joueur touche le sol
            self.jumping = 0
            self.y_speed = 0  # Réinitialiser la vitesse

        # Gestion de l'animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.animation_counter = 0

            # Mettre à jour le masque avec l'image actuelle
            self.mask = pygame.mask.from_surface(self.images[self.current_image])

    def draw(self, screen, player_x):
        #Affiche le joueur à la position actuelle avec l'animation#
        screen.blit(self.images[self.current_image], (player_x, self.y))

