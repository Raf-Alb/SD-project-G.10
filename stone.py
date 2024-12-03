# stone.py
import pygame
import random

class Stone:
    def __init__(self, x, y, width, height, image):
        """Initialise une pierre avec ses propriétés."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.mask = pygame.mask.from_surface(self.image)  # Masque pour les collisions

    def update(self, scroll_speed, screen_width, min_distance):
        """Met à jour la position de la pierre et la réinitialise si elle sort de l'écran."""
        self.x -= scroll_speed
        if self.x + self.width < 0:  # Réinitialiser si la pierre sort de l'écran
            self.reset(screen_width, min_distance, floor=500)

    def reset(self, screen_width, min_distance, floor):
        """Réinitialise la position et la taille de la pierre."""
        self.width = random.randint(40, 100)
        self.height = self.width
        self.x = screen_width + random.randint(min_distance, min_distance + 200)
        self.y = floor - self.height  # Position verticale basée sur le sol
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        """Dessine la pierre sur l'écran."""
        screen.blit(self.image, (self.x, self.y))

    def detect_collision(self, player_x, player_y, player):
        """Vérifie la collision précise entre le joueur et cette pierre."""
        offset_x = self.x - player_x
        offset_y = self.y - player_y
        return player.mask.overlap(self.mask, (offset_x, offset_y))

def create_stones(stone_image, screen_width, floor, num_stones, min_distance=400):
    """Crée une liste d'instances de pierres alignées avec une distance minimale entre elles."""
    stones = []
    current_x = screen_width + 110  # Position de départ pour la première pierre

    for _ in range(num_stones):
        stone_width = random.randint(40, 100)
        stone_height = stone_width
        stone_y = floor - stone_height
        stone_x = current_x

        # Ajouter une instance de Stone à la liste
        stones.append(Stone(stone_x, stone_y, stone_width, stone_height, stone_image))

        # Déplacer current_x pour la prochaine pierre, en respectant l'écart minimal
        current_x += stone_width + min_distance

    return stones



