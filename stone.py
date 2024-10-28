# stone.py
import pygame
import random

def create_stones(stone_image, screen_width, floor, num_stones, min_distance=400):
    #Crée plusieurs pierres alignées avec une distance minimale entre elles, sans chevauchement.
    stones = []
    current_x = screen_width + 110  # Position de départ pour la première pierre

    for _ in range(num_stones):
        stone_width = random.randint(40, 100)
        stone_height = stone_width  # Assurer une taille carrée
        stone_y = floor - stone_height  # Positionner chaque pierre au niveau du sol des pierres
        stone_x = current_x  # Position X actuelle
        stone = pygame.transform.scale(stone_image, (stone_width, stone_height))
        
        # Créer un masque de collision pour l'image de la pierre
        stone_mask = pygame.mask.from_surface(stone)

        # Ajouter la pierre à la liste avec son masque
        stones.append({
            "x": stone_x,
            "y": stone_y,
            "width": stone_width,
            "height": stone_height,
            "image": stone,
            "mask": stone_mask
        })

        # Déplacer current_x pour la prochaine pierre, en s'assurant qu'il y a un écart minimal
        current_x += stone_width + min_distance

    return stones

def detect_collision(player_x, player_y, player, stone):
    #Vérifie la collision précise entre le joueur et une pierre en utilisant des masques.
    # Position relative entre le joueur et la pierre
    offset_x = stone["x"] - player_x
    offset_y = stone["y"] - player_y

    # Utiliser les masques pour vérifier une collision
    if player.mask.overlap(stone["mask"], (offset_x, offset_y)):
        return True
    return False


