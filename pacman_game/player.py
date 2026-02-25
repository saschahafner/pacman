import pygame
from settings import *

class Pacman(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLAYER_COLOR, (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 2)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 2

    def update(self, walls):
        self.handle_keys()
        self.pos.x += self.vel.x
        self.rect.center = self.pos
        self.collision('x', walls)

        self.pos.y += self.vel.y
        self.rect.center = self.pos
        self.collision('y', walls)

    def collision(self, direction, walls):
        for wall in walls:
            if self.rect.colliderect(wall):
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

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel = pygame.math.Vector2(-self.speed, 0)
        elif keys[pygame.K_RIGHT]:
            self.vel = pygame.math.Vector2(self.speed, 0)
        elif keys[pygame.K_UP]:
            self.vel = pygame.math.Vector2(0, -self.speed)
        elif keys[pygame.K_DOWN]:
            self.vel = pygame.math.Vector2(0, self.speed)
        # Note: In real Pacman, you keep moving until you hit a wall.
        # Here, if no key is pressed, we keep moving in the last direction (as set by self.vel).
        # To stop when key is released (not Pacman style), we would reset self.vel here.
        # But for Pacman, we usually want to queue the next direction.

    def draw(self, screen):
        screen.blit(self.image, self.rect)
