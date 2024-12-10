# bee.py
import pygame, random, math
import os

class Bee:
    def __init__(self, x, y, speed, images, animation_speed):
        # Initializes a bee with its properties
        self.x = x
        self.y = y
        self.speed = speed
        self.speed_multiplier = random.uniform(1, 2)  # Random speed variation (between 1 and 2)
        self.images = images
        self.current_image = 0
        self.animation_counter = 0
        self.animation_speed = animation_speed
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.mask = pygame.mask.from_surface(self.images[0])

    def update(self, screen_width, player_y=None, scroll_speed=2):
        # Update the bee's position and animation
        self.x -= scroll_speed * self.speed_multiplier # Horizontal movement proportional to background speed

        # Follow the player by adjusting the vertical position
        if player_y is not None:
            tracking_speed = 1  # Limits vertical speed
            if self.y < player_y:
                self.y += min(tracking_speed, abs(player_y - self.y))
            elif self.y > player_y:
                self.y -= min(tracking_speed, abs(player_y - self.y))

        # Add an oscillating movement for dynamism
        self.y += math.sin(pygame.time.get_ticks() / 500) * 2

        # Animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.animation_counter = 0
            self.mask = pygame.mask.from_surface(self.images[self.current_image])

        if self.x + self.width < 0:
            self.reset(screen_width)

    def reset(self, screen_width):
    # Resets when bee leaves screen on the left
        self.x = screen_width + random.randint(100, 300)
        self.y = random.randint(20, 300)
        self.speed = random.uniform(1.5, 3.0)  # Random initial speed
        self.speed_multiplier = random.uniform(1, 2)  # Random speed variation

    def draw(self, screen):
        # Draw the bee on the screen
        screen.blit(self.images[self.current_image], (self.x, self.y))

    def detect_collision(self, player_x, player_y, player):
        # Checks for precise collision between player and bee
        offset_x = self.x - player_x
        offset_y = self.y - player_y
        return player.mask.overlap(self.mask, (offset_x, offset_y))

def load_bee_images(folder, size=(50, 50)):
    # Loads all bee images from a folder and resizes them to a fixed size
    images = []
    for img in sorted(os.listdir(folder)):
        if img.endswith(".png"):
            image = pygame.image.load(os.path.join(folder, img)).convert_alpha()
            images.append(pygame.transform.scale(image, size))
    return images

def create_bees(screen_width, y_range=(20, 300), num_bees=2, min_distance=500, image_folder="bee_frame", animation_speed=3):
    # Creates a list of bee instances with random positions and speeds
    bees = []
    bee_images = load_bee_images(image_folder, size=(50, 50))  # Load bee frames
    current_x = screen_width + 150

    for _ in range(num_bees):
        bee_y = random.randint(*y_range)
        bee_x = current_x
        bee_speed = random.uniform(1.5, 3.0)
        bees.append(Bee(bee_x, bee_y, bee_speed, bee_images, animation_speed))
        current_x += 50 + min_distance

    return bees

