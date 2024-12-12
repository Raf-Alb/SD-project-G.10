import pygame, random

class Stone:
    def __init__(self, x, y, width, height, image):
        # Initializes a stone with its properties
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.mask = pygame.mask.from_surface(self.image)  

    def update(self, scroll_speed, screen_width, min_distance):
        # Updates the stone's position
        self.x -= scroll_speed
        if self.x + self.width < 0:  # Resets the stone if it leaves the screen
            self.reset(screen_width, min_distance, floor=500)

    def reset(self, screen_width, min_distance, floor):
        # Resets stone position and size
        self.width = random.randint(40, 100)
        self.height = self.width
        self.x = screen_width + random.randint(min_distance, min_distance + 200)
        self.y = floor - self.height  # Floor-based vertical position
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        # Draws the stone on the screen
        screen.blit(self.image, (self.x, self.y))

    def detect_collision(self, player_x, player_y, player):
        # Checks for collision between player and stone
        offset_x = self.x - player_x
        offset_y = self.y - player_y
        return player.mask.overlap(self.mask, (offset_x, offset_y))

def create_stones(stone_image, screen_width, floor, num_stones, min_distance=400):
    # Creates a list of stone instances aligned with a minimum distance between them
    stones = []
    current_x = screen_width + 110  # Initial position for the first stone

    for _ in range(num_stones):
        stone_width = random.randint(40, 100)
        stone_height = stone_width
        stone_y = floor - stone_height
        stone_x = current_x

        # Add a stone instance to the list
        stones.append(Stone(stone_x, stone_y, stone_width, stone_height, stone_image))

        # Move current_x for the next stone, respecting the minimum distance
        current_x += stone_width + min_distance

    return stones



