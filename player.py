
class Player:
    def __init__(self, floor, gravity, image_folder, animation_speed=5):
        # Initializes the player's vertical position so that his feet touch the ground
        self.y = floor
        self.y_speed = 0
        self.jumping = 0
        self.floor = floor  # Fixed floor height
        self.gravity = gravity

        # Load images for animation
        self.images = self.load_images(image_folder)
        self.current_image = 0

        # Player size (based on first image)
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()

        # Create a mask for the player (based on first image)
        self.mask = pygame.mask.from_surface(self.images[self.current_image])

        # Animation speed
        self.animation_speed = animation_speed
        self.animation_counter = 0

    def load_images(self, folder):
        # Loads all images from a folder
        images = [pygame.image.load(os.path.join(folder, img)) for img in sorted(os.listdir(folder)) if img.endswith(".png")]
        return images

    def jump(self):
        if self.jumping == 0:
            self.y_speed = -20  # Initialize jump speed
            self.jumping = 1
        elif self.jumping == 1 and self.y_speed >= 0:
            self.y_speed = -15  # Double jump
            self.jumping = 2
        elif self.jumping == 2 and self.y_speed >= 0:
            self.y_speed = -15  # Triple jump
            self.jumping = 3

    def update(self):
        # Updates player position and animation
        self.y_speed += self.gravity  # Apply gravity
        # Adjusts so that the feet touch the ground
        self.y = min(self.y + self.y_speed, self.floor - self.height)

        if self.y == self.floor - self.height:  # If the player touches the ground
            self.jumping = 0 # No jump when game starts
            self.y_speed = 0  # Initial vertical speed
            
        # Animation management
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.animation_counter = 0

            # Update mask with current image
            self.mask = pygame.mask.from_surface(self.images[self.current_image])

    def draw(self, screen, player_x):
        # Displays player at current position with animation
        screen.blit(self.images[self.current_image], (player_x, self.y))

