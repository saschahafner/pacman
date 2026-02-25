import pygame
import random
from settings import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # Draw ghost body
        pygame.draw.circle(self.image, color, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 2)
        # Rect for eyes? Maybe later.

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 2
        self.direction = pygame.math.Vector2(0, 0)
        self.last_move_time = 0

    def update(self, walls):
        # Simple AI: Move in current direction.
        # If hitting a wall, choose a new random direction.
        # Also change direction randomly occasionally at intersections?

        # Move
        self.pos.x += self.vel.x
        self.rect.center = self.pos
        self.collision('x', walls)

        self.pos.y += self.vel.y
        self.rect.center = self.pos
        self.collision('y', walls)

        # If stopped or hitting wall (speed is 0 or low), change direction
        if self.vel.length() == 0 or (random.randint(0, 100) < 2 and self.is_at_intersection(walls)):
             self.choose_direction(walls)

    def is_at_intersection(self, walls):
        # Check if multiple directions are open
        # This is a bit complex for pixel movement.
        # For now, just rely on collision handling.
        return True # Placeholder

    def collision(self, direction, walls):
        hit = False
        for wall in walls:
            if self.rect.colliderect(wall):
                hit = True
                if direction == 'x':
                    if self.vel.x > 0: # Moving right
                        self.rect.right = wall.left
                    elif self.vel.x < 0: # Moving left
                        self.rect.left = wall.right
                    self.pos.x = self.rect.centerx
                if direction == 'y':
                    if self.vel.y > 0: # Moving down
                        self.rect.bottom = wall.top
                    elif self.vel.y < 0: # Moving up
                        self.rect.top = wall.bottom
                    self.pos.y = self.rect.centery

        if hit:
            self.choose_direction(walls)

    def choose_direction(self, walls):
        directions = [
            pygame.math.Vector2(self.speed, 0),
            pygame.math.Vector2(-self.speed, 0),
            pygame.math.Vector2(0, self.speed),
            pygame.math.Vector2(0, -self.speed)
        ]
        random.shuffle(directions)

        # Try to pick a direction that doesn't immediately result in collision?
        # With current collision logic, we just set velocity. If it hits wall next frame, it will bounce/stop and call choose_direction again.
        # But we want to avoid getting stuck in a loop.

        self.vel = directions[0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
