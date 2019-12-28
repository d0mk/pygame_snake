import pygame
import random
import time
import os
from audio_manager import AudioManager
from snake import Snake


class Game:
    def __init__(self):
        pygame.init()
        self.set_game_parameters()
        self.set_window_parameters()
        self.audio_manager = AudioManager()


    def set_game_parameters(self):
        self.num_of_cells = 30
        self.cell_size = 20
        self.cell_spacing = 3
        self.FPS = 60
        self.background_color = pygame.Color(0, 0, 0)
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.score = 0
        self.running = True


    def set_window_parameters(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '10,10'
        pygame.display.set_caption('Snake game')
        self.screen_width = self.cell_size * self.num_of_cells + self.cell_spacing * (self.num_of_cells + 1)
        self.screen_heigth = self.cell_size * self.num_of_cells + self.cell_spacing * (self.num_of_cells + 1)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_heigth))


    def start(self):
        snake = self.create_snake()
        mouse = self.place_mouse(snake.segments)
        
        time_point = time.time()

        while self.running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # if time.time() - time_point > self.audio_manager.delay:
            #     time_point = time.time()
            #     self.audio_manager.play_next()

            if pygame.sprite.collide_rect(snake.head, mouse):
                self.score += 1

            snake.update(pygame.key.get_pressed())
            self.draw()

        self.game_over_screen()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


    def create_snake(self):
        snake_start_x = snake_start_y = self.num_of_cells // 2
        snake = Snake(snake_start_x, snake_start_y)
        snake.initialize()
        return snake


    def place_mouse(self, snake_segments):
        while True:
            mouse_x = random.randint(0, self.num_of_cells - 1)
            mouse_y = random.randint(0, self.num_of_cells - 1)
            if not any(seg.x == mouse_x and seg.y == mouse_y for seg in snake_segments):
                return Mouse(mouse_x, mouse_y)


    def game_over_screen(self):
        background_color = pygame.Color(200, 0, 0)
        message_color = pygame.Color(128, 128, 0)
        score_color = pygame.Color(0, 128, 128)
        
        message_font = pygame.font.SysFont('consolas', 50)
        score_font = pygame.font.SysFont('consolas', 30)

        end_message = 'Game over'
        score_message = f'Score: {self.score}'

        surf = pygame.Surface((self.screen_width, self.screen_height))
        surf.fill(background_color)
        surf.set_alpha(0)

        message_text = message_font.render(end_message, True, message_color)
        score_text = score_font.render(score_message, True, score_color)

        center_v = surf.get_height() // 2
        center_h = surf.get_width() // 2

        surf.blit(message_text, (center_h - message_text.get_width() // 2, center_v - message_text.get_height()))
        surf.blit(score_text, (center_h - score_text.get_width() // 2, center_v + score_text.get_height()))

        while (alpha := surf.get_alpha()) < 255:
            surf.set_alpha(alpha + 1)
            self.screen.blit(surf, (0, 0))
            pygame.time.delay(10)
            pygame.display.flip()

    
    def draw(self):
        self.screen.fill(self.background_color)

        for entity in self.sprites:
            entity.draw(self.screen)

        pygame.display.flip()