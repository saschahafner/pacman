import pygame
import sys
from settings import *
from maze import Maze
from player import Pacman
from ghost import Ghost

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start' # start, playing, game_over, win
        self.maze = Maze()
        self.player = Pacman(self.maze.player_start_pos)
        self.ghosts = []
        self.make_ghosts()
        self.score = 0

    def make_ghosts(self):
        colors = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]
        for i, pos in enumerate(self.maze.ghost_spawn_pos):
            if i < 4:
                self.ghosts.append(Ghost(pos, colors[i % 4]))

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game_over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            elif self.state == 'win':
                self.win_events()
                self.win_update()
                self.win_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    # --- Start Screen Functions ---
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('1 PLAYER ONLY', self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        self.draw_text('HIGH SCORE', self.screen, [4, 0], START_TEXT_SIZE, (255, 255, 255), START_FONT)
        pygame.display.update()

    # --- Playing Functions ---
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def playing_update(self):
        self.player.update(self.maze.walls)
        for ghost in self.ghosts:
            ghost.update(self.maze.walls)
            if ghost.rect.colliderect(self.player.rect):
                self.state = 'game_over'

        # Check for dot collisions
        # Create a copy to iterate safely while removing
        for dot in self.maze.dots[:]:
            if self.player.rect.colliderect(dot):
                self.maze.dots.remove(dot)
                self.score += 10

        if len(self.maze.dots) == 0:
            self.state = 'win'

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.maze.draw(self.screen)
        self.player.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        self.draw_text(f'SCORE: {self.score}', self.screen, [10, 10], 18, WHITE, START_FONT)
        pygame.display.update()

    # --- Game Over Functions ---
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'start' # Return to start screen
                self.__init__()

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2], START_TEXT_SIZE, RED, START_FONT, centered=True)
        self.draw_text('PRESS SPACE TO RESTART', self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50], START_TEXT_SIZE, WHITE, START_FONT, centered=True)
        pygame.display.update()

    # --- Win Functions ---
    def win_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'start'
                # Reset game? Ideally yes.
                self.__init__()

    def win_update(self):
        pass

    def win_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('YOU WIN!', self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2], START_TEXT_SIZE, (255, 215, 0), START_FONT, centered=True)
        self.draw_text('PRESS SPACE TO RESTART', self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50], START_TEXT_SIZE, WHITE, START_FONT, centered=True)
        pygame.display.update()

    # --- Helper Functions ---
    def draw_text(self, text, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, False, color)
        text_size = text_surface.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text_surface, pos)

if __name__ == '__main__':
    game = Game()
    game.run()
