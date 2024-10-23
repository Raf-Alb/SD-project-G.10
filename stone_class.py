# stone.py
import pygame
import random

def create_stone(stone_image, screen_width, floor):
    #"""Crée un obstacle avec une taille et une position aléatoires."""
    stone_width = random.randint(40, 100)
    stone_height = stone_width
    stone_x = random.randint(screen_width, screen_width + 300)
    stone_y = floor
    stone = pygame.transform.scale(stone_image, (stone_width, stone_height))

    return {
        "x": stone_x,
        "y": stone_y,
        "width": stone_width,
        "height": stone_height,
        "image": stone
    }

def detect_collision(player_x, player_y, player_width, player_height, stone):
    #"""Vérifie la collision entre le joueur et un obstacle."""
    return (player_x < stone["x"] + stone["width"] and
            player_x + player_width > stone["x"] and
            player_y < stone["y"] + stone["height"] and
            player_y + player_height > stone["y"])
