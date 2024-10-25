# stone.py
import pygame
import random


def create_stones(stone_image, screen_width, floor, num_stones, min_distance=200):
    
    #Crée plusieurs pierres alignées avec une distance minimale entre elles, sans chevauchement.
    
    stones = []
    current_x = screen_width + 110  # Position de départ pour la première pierre

    for _ in range(num_stones):
        stone_width = random.randint(40, 100)
        stone_height = stone_width  # Assurer une taille carrée
        stone_y = floor # Toutes les pierres sont sur le même plan Y (niveau du sol)
        stone_x = current_x  # Position X actuelle
        stone = pygame.transform.scale(stone_image, (stone_width, stone_height))

        # Ajouter la pierre à la liste
        stones.append({
            "x": stone_x,
            "y": stone_y,
            "width": stone_width,
            "height": stone_height,
            "image": stone
        })

        # Déplacer current_x pour la prochaine pierre, en s'assurant qu'il y a un écart minimal
        current_x += stone_width + min_distance

    return stones

def detect_collision(player_x, player_y, player_width, player_height, stone):
    
    #Vérifie la collision entre le joueur et une pierre (stone).
    
    return (player_x < stone["x"] + stone["width"] and
            player_x + player_width > stone["x"] and
            player_y < stone["y"] + stone["height"] and
            player_y + player_height > stone["y"])
