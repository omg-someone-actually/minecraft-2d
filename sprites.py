import pygame
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, image, width, height, screen) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.vec = pygame.math.Vector2
        self.ACC = 0.5
        self.FRIC = -0.12
        
        self.image = image
        self.pos = self.vec(200, 200)
        self.width, self.height = (width, height)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.vel = self.vec(0,0)
        self.acc = self.vec(0,0)
        self.is_grounded = False
        self.is_in_water = False
        
    def move(self, move, blocks, x, y) -> int:
        self.acc = self.vec(0, 0)
        for block in blocks:
            if block.type == 'water' and pygame.sprite.collide_rect(self, block):
                self.vel.y /= 1.05
                self.vel.y += 0.005
                self.is_grounded = False
                self.is_in_water = True
                break
            elif pygame.sprite.collide_rect(self, block):
                if not self.is_grounded:
                    self.pos.y = block.rect.top - self.height + 1
                    
                self.is_grounded = True
                self.vel.y = 0
                break
                
            self.is_grounded = False
            self.is_in_water = False
            
        if not self.is_grounded and not self.is_in_water:
            self.acc = self.vec(0,0.5)
            
              
        if move == 'left':
            valid_move = True
            
            for block in blocks:
                if pygame.sprite.collide_rect(self, block) and block.type != 'water':
                    if self.rect.left - 10 < block.rect.right and self.rect.bottom > block.rect.bottom:
                        valid_move = False
                        
            if valid_move:
                self.acc.x -= self.ACC if not self.is_in_water else self.ACC / 2
        elif move == 'right':
            valid_move = True
            
            for block in blocks:
                if pygame.sprite.collide_rect(self, block) and block.type != 'water':
                    if self.rect.right + 10 > block.rect.left and self.rect.bottom > block.rect.bottom:
                        valid_move = False
                        
            if valid_move:
                self.acc.x = self.ACC if not self.is_in_water else self.ACC / 2
        elif move == 'jump' and (self.is_grounded or self.is_in_water):
            self.vel.y = -10

        elif move == 'down' and self.is_in_water:
            self.vel.y += 0.25
             
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.x, self.rect.y = self.pos
        self.screen.blit(self.image, self.pos)

        if self.pos.x < 0:
            x -= 1
            self.pos.x = self.screen.get_width() - self.width
        elif self.pos.x > self.screen.get_width() - self.width:
            x += 1
            self.pos.x = 0
        if self.pos.y < 0 and y < 1:
            y += 1
            self.pos.y = 700
        elif self.pos.y > self.screen.get_height():
            y -= 1
            self.pos.y = 100

        return x, y


class Zombie(pygame.sprite.Sprite):
    def __init__(self, image, width, height, screen) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.vec = pygame.math.Vector2
        self.ACC = 0.1
        self.FRIC = -0.12
        
        self.image = image
        self.pos = self.vec(randint(100, 500), 200)
        self.width, self.height = (width, height)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.vel = self.vec(0,0)
        self.acc = self.vec(0,0)
        self.is_grounded = False
        self.is_in_water = False
        
    def move(self, blocks, player) -> int:
        if player:
            move = self.calculate_move(player, blocks)
            self.acc = self.vec(0, 0)
            for block in blocks:
                if block.type == 'water' and pygame.sprite.collide_rect(self, block):
                    self.vel.y += 0.0005
                    self.is_grounded = False
                    self.is_in_water = True
                    break
                elif pygame.sprite.collide_rect(self, block):
                    if not self.is_grounded:
                        self.pos.y = block.rect.top - self.height + 1
                        
                    self.is_grounded = True
                    self.vel.y = 0
                    break
                    
                self.is_grounded = False
                self.is_in_water = False
                
            if not self.is_grounded and not self.is_in_water:
                self.acc = self.vec(0,0.5)
                
                  
            if move == 'left':
                valid_move = True
                
                for block in blocks:
                    if pygame.sprite.collide_rect(self, block):
                        if self.rect.left - 10 < block.rect.right and self.rect.bottom > block.rect.bottom:
                            valid_move = False
                            
                if valid_move:
                    self.acc.x -= self.ACC
            elif move == 'right':
                valid_move = True
                
                for block in blocks:
                    if pygame.sprite.collide_rect(self, block):
                        if self.rect.right + 10 > block.rect.left and self.rect.bottom > block.rect.bottom:
                            valid_move = False
                            
                if valid_move:
                    self.acc.x = self.ACC
            elif move == 'jump' and (self.is_grounded or self.is_in_water):
                self.vel.y = -10
                 
            self.acc.x += self.vel.x * self.FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
    
            self.rect.x, self.rect.y = self.pos
        self.screen.blit(self.image, self.pos)

    def calculate_move(self, player, blocks) -> str:
        if self.pos.y > player.pos.y + 10 and player.is_grounded:
            return 'jump'
        elif self.pos.x < player.pos.x:
            return 'right'
        elif self.pos.x > player.pos.x:
            return 'left'
            
        return None