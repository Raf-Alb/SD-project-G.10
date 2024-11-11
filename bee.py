# bee.py
import pygame
import os
import random

def load_bee_images(folder, size=(50, 50)):
    # Charger toutes les images de l'abeille depuis un dossier et les redimensionner à une taille fixe
    images = []
    for img in sorted(os.listdir(folder)):
        if img.endswith(".png"):
            image = pygame.image.load(os.path.join(folder, img)).convert_alpha()
            # Redimensionner l'image à une taille fixe (50x50 par défaut)
            resized_image = pygame.transform.scale(image, size)
            images.append(resized_image)
    return images

def create_bees(screen_width, y_range=(20, 300), num_bees=2, min_distance=500, image_folder="bee_frame", animation_speed=3):
    bees = []
    bee_images = load_bee_images(image_folder, size=(50, 50))  # Charger les frames de l'abeille redimensionnées
    current_x = screen_width + 150

    for _ in range(num_bees):
        bee_width, bee_height = 50, 50  # Dimensions fixes
        bee_y = random.randint(*y_range)
        bee_x = current_x
        bee_speed = random.uniform(1.5, 3.0)
        bee_mask = pygame.mask.from_surface(bee_images[0])  # Créer le masque pour la première image redimensionnée

        bees.append({
            "x": bee_x,
            "y": bee_y,
            "width": bee_width,
            "height": bee_height,
            "images": bee_images,         # Les frames d'animation de l'abeille redimensionnées
            "current_image": 0,           # Index de l'image courante
            "animation_counter": 0,       # Compteur d'animation
            "animation_speed": animation_speed,  # Vitesse de l'animation
            "mask": bee_mask,             # Masque de collision
            "speed": bee_speed            # Vitesse de défilement spécifique pour cette abeille
        })

        current_x += bee_width + min_distance

    return bees

def update_bee(bee, screen_width):
    # Déplace et anime l'abeille
    bee["x"] -= bee["speed"]

    # Gérer l'animation
    bee["animation_counter"] += 1
    if bee["animation_counter"] >= bee["animation_speed"]:
        bee["current_image"] = (bee["current_image"] + 1) % len(bee["images"])
        bee["animation_counter"] = 0
        # Mettre à jour le masque pour l'image actuelle redimensionnée
        bee["mask"] = pygame.mask.from_surface(bee["images"][bee["current_image"]])

    # Réinitialiser l'abeille si elle sort de l'écran
    if bee["x"] + bee["width"] < 0:
        bee["x"] = screen_width + random.randint(100, 300)
        bee["y"] = random.randint(20, 300)  # Réinitialiser la position en hauteur
        bee["speed"] = random.uniform(1.5, 3.0)

def draw_bee(screen, bee):
    # Dessine l'abeille avec l'image actuelle redimensionnée
    screen.blit(bee["images"][bee["current_image"]], (bee["x"], bee["y"]))
