import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, DEFAULT_TYPE, FONT_STYLE, FRONT_PAGE, GAME_OVER, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS,HEART


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(FRONT_PAGE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

        self.running = False
        self.score = 0
        self.max_score = 0
        self.death_count = 0
        self.lives = 3

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu(self.screen)
        
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 20
        self.score = 0
        self.lives = 3
        self.playing = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.update_score()
        self.live_verification()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.game_speed, self.score, self.player)

    def update_score(self):
        self.score += 1
        if self.score % 200 == 0:
            self.game_speed += 5

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.best_score()
        self.draw_lives(self.screen)
        self.draw_power_up_time()
        self.player.draw(self.screen, self.lives)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        color = (0, 0, 0)
        self.screen_printing(1000, 50 , f"Score: {self.score}", color)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time_up - pygame.time.get_ticks()) /1000 , 2)
            if time_to_show >= 0:
                self.screen_printing(500, 40,f"{self.player.type.capitalize()} enabled for {time_to_show} seconds.", (0, 0, 0))
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def draw_lives(self, screen):
        color = (0, 0, 0)
        self.screen_printing(50, 50 , str(self.lives) , color)
        self.heart_rect = HEART.get_rect()
        screen.blit(HEART,(60, 35))

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def live_verification(self):
        if self.lives == 0:
            self.playing = False


    def show_menu(self, screen):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2 

        if self.death_count == 0:
            color = (0, 0, 0)
            self.screen_printing(550, 400, "Press any key to start", color)
        else:
            color = (0, 0, 0)
            self.heart_rect = GAME_OVER.get_rect()
            screen.blit(GAME_OVER,(370, 270))
            self.screen_printing(half_screen_width, half_screen_height + 30, f"Score: {self.score}", color)
            self.screen_printing(half_screen_width, half_screen_height + 60, f"High Score: {self.max_score}", color)
            self.screen_printing(half_screen_width, half_screen_height + 90, "Press any key to retry", color)

        self.screen.blit(FRONT_PAGE, (300 , 100))
        pygame.display.flip()
        self.handle_events_on_menu()

    def best_score(self):
        if self.max_score < self.score:
            self.max_score = self.score
        color = (0, 0, 0)
        self.screen_printing(950, 80 , f"High Score: {self.max_score}", color)

    
    def screen_printing(self, pos_x, pos_y, message, color):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(message, True, color)
        text_rect = text.get_rect()
        text_rect.center = (pos_x, pos_y)
        self.screen.blit(text, text_rect)