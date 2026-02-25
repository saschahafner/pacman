import pygame
from settings import *

class Maze:
    def __init__(self):
        self.walls = []
        self.dots = []
        self.player_start_pos = (0, 0)
        self.ghost_spawn_pos = []
        self.load_maze()

    def load_maze(self):
        self.walls = []
        self.dots = []
        self.ghost_spawn_pos = []
        # Calculate offset to center the maze
        layout_width_px = len(MAZE_LAYOUT[0]) * TILE_SIZE
        layout_height_px = len(MAZE_LAYOUT) * TILE_SIZE

        self.offset_x = (SCREEN_WIDTH - layout_width_px) // 2
        self.offset_y = (SCREEN_HEIGHT - layout_height_px) // 2

        for row_idx, row in enumerate(MAZE_LAYOUT):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE + self.offset_x
                y = row_idx * TILE_SIZE + self.offset_y
                if cell == "1":
                    self.walls.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                elif cell == "0":
                    # Add a smaller rect for the dot
                    dot_size = 4
                    dot_x = x + (TILE_SIZE - dot_size) // 2
                    dot_y = y + (TILE_SIZE - dot_size) // 2
                    self.dots.append(pygame.Rect(dot_x, dot_y, dot_size, dot_size))
                elif cell == "P":
                    self.player_start_pos = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    # No dot under player start usually, or maybe yes?
                    # Let's assume no dot for now to keep it simple, or add it if needed.
                    pass
                elif cell == "2":
                    self.ghost_spawn_pos.append((x + TILE_SIZE // 2, y + TILE_SIZE // 2))

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall)
            # Optional: Draw outline for better visibility
            pygame.draw.rect(screen, BLACK, wall, 1)
        for dot in self.dots:
            pygame.draw.rect(screen, (255, 184, 174), dot) # Salmon/Pinkish color for dots
