# Game.py
import pygame, sys, random
from player import Player
from stone import Stone, create_stones
from bee import Bee, create_bees
from background import update_background

# Window settings
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (225, 225, 225) #white

# Game management class
class Game:
    def __init__(self):
        # Pygame initialization
        pygame.init()
        # Window size
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption("Bee Running")
        self.clock = pygame.time.Clock()

        # Charger les ressources
        self.background = pygame.image.load('Fond jeu.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOWWIDTH, WINDOWHEIGHT))
        self.stone_image = pygame.image.load('stone.png').convert_alpha()
        #font creation
        self.font_large = pygame.font.SysFont("courier new", 62)
        self.font_score = pygame.font.SysFont("arial", 36)
        #set up sounds
        self.gameOverSound = pygame.mixer.Sound('finalmusic.wav')
        pygame.mixer.music.load('background.mid')

        # Paramètres du joueur et du jeu
        self.player_floor = 510
        self.stone_floor = 500
        self.scroll_speed = 2
        self.gravity = 1
        self.default_gravity = self.gravity
        self.score_increment = 1
        self.top_score = 0
    
    #function for quitting properly
    def terminate(self):
        pygame.quit()
        sys.exit()

    def wait_for_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
    #function to draw score on screen
    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(topleft=(x, y))
        self.screen.blit(text_obj, text_rect)
    #function to start the screen
    def show_start_screen(self):
        #show the background picture
        self.screen.blit(self.background, (0, 0)) #sets background at (0,0) position
        #initial text "Bee running"
        text_surface1 = self.font_large.render("Bee Running", True, (0, 40, 0))
        text_surface2 = self.font_large.render("Press a key to start", True, (0, 40, 0))
        text_rect1 = text_surface1.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 3))
        text_rect2 = text_surface2.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 3 + 50))
        #show text on screen
        self.screen.blit(text_surface1, text_rect1)
        self.screen.blit(text_surface2, text_rect2)
        pygame.display.update() #update the display
        self.wait_for_key() #wait for player to start the game

    #function for game over screen
    def show_game_over_screen(self, score):
        #text for game over
        game_over_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4))
        #text for score
        score_text = self.font_score.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
        #text for top score
        top_score_text = self.font_score.render(f"Top Score: {self.top_score}", True, (255, 255, 255))
        top_score_rect = top_score_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 50))
        #text for restart instructions
        restart_text = self.font_score.render("Press any key to restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 100))
        #game over final display
        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text, game_over_rect) #game over
        self.screen.blit(score_text, score_rect) #score
        self.screen.blit(top_score_text, top_score_rect) #top score
        self.screen.blit(restart_text, restart_rect)
        pygame.display.update()
        self.wait_for_key()

    def run(self):
        # Écran de démarrage
        self.show_start_screen()

        while True:
            # Réinitialisation des variables pour une nouvelle partie
            score = 0
            player_x = 100
            player = Player(self.player_floor, self.gravity, image_folder="player_frames")
            stones = create_stones(self.stone_image, WINDOWWIDTH, self.stone_floor, num_stones=3, min_distance=400)
            bees = create_bees(WINDOWWIDTH, y_range=(20, 300), num_bees=2, min_distance=500, image_folder="bee_frame")
            bg_x1, bg_x2 = 0, self.background.get_width()
            running = True
            pygame.mixer.music.play(-1, 0.0)

            # Boucle principale du jeu
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()

                # Gérer les mouvements du joueur
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player_x -= 5
                if keys[pygame.K_RIGHT]:
                    player_x += 5
                if keys[pygame.K_SPACE]:
                    player.jump()
                if keys[pygame.K_DOWN]:
                    self.gravity = 3
                else:
                    self.gravity = self.default_gravity
                player.gravity = self.gravity
                player.update()

                # Empêcher le joueur de sortir de l'écran et Game Over s'il sort à gauche
                player_x = max(0, min(player_x, WINDOWWIDTH - player.width))
                if player_x <= 0:
                    running = False

                # Augmenter la difficulté
                if score % 500 == 0:
                    self.scroll_speed += 1

                # Mettre à jour le fond
                bg_x1, bg_x2 = update_background(bg_x1, bg_x2, self.background.get_width(), self.scroll_speed)

                # Dessiner le fond
                self.screen.blit(self.background, (bg_x1, 0))
                self.screen.blit(self.background, (bg_x2, 0))

                # Dessiner les pierres
                for stone in stones:
                    stone.update(self.scroll_speed, WINDOWWIDTH, 400)
                    stone.draw(self.screen)
                    if stone.detect_collision(player_x, player.y, player):
                        player_x -= 50

                # Maintenir au moins 3 pierres
                if len(stones) < 3:
                    new_stone = Stone(
                        x=WINDOWWIDTH + random.randint(400, 600),
                        y=self.stone_floor - random.randint(40, 100),
                        width=random.randint(40, 100),
                        height=random.randint(40, 100),
                        image=self.stone_image
                    )
                    stones.append(new_stone)

                # Dessiner les abeilles
                for bee in bees:
                    bee.update(WINDOWWIDTH, player.y, scroll_speed=self.scroll_speed)
                    bee.draw(self.screen)
                    if bee.detect_collision(player_x, player.y, player):
                        running = False


                # Dessiner le joueur
                player.draw(self.screen, player_x)

                # Afficher les scores
                self.draw_text(f"Score: {score}", self.font_score, TEXTCOLOR, 10, 10)
                self.draw_text(f"Top Score: {self.top_score}", self.font_score, TEXTCOLOR, 10, 50)

                # Mettre à jour l'affichage
                pygame.display.flip()
                self.clock.tick(60)

                # Mise à jour du score
                score += self.score_increment * self.scroll_speed

            # Fin de partie
            pygame.mixer.music.stop()
            if score > self.top_score:
                self.top_score = score
            self.gameOverSound.play()
            self.show_game_over_screen(score)
            self.scroll_speed = 2
            self.gameOverSound.stop()


if __name__ == "__main__":
    game = Game()
    game.run()


    
     



#Background : https://fr.vecteezy.com/art-vectoriel/4277175-foret-jeu-fond
#Abeille : https://pixabay.com/gifs/wasp-hornet-insect-fly-pixel-art-12292/
#Personnage : https://www.gifsanimes.com/img-course-a-pied-image-animee-0008-60786.htm
#Rocher : https://fr.vecteezy.com/png/8502483-pierres-de-roche-et-rochers-de-style-dessin-anime 



