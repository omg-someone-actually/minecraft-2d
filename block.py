import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, image, x, y, screen, background, type, blocks) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.vec = pygame.math.Vector2

        self.image = image
        self.screen = screen
        self.background = background
        self.pos = self.vec(x, y)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos
        self.type = type
        self.blocks = blocks
        self.height = 100

        if self.type == 'sand':
            self.ACC = 0.5
            self.FRIC = -0.12
            self.vel = self.vec(0,0)
            self.acc = self.vec(0,0)
            self.is_grounded = False
            self.gravity(self.blocks)

    def show(self) -> None:
        if self.type == 'sand':
            self.gravity(self.blocks)
        self.screen.blit(self.image, self.pos)

    def gravity(self, blocks) -> None:
        self.acc = self.vec(0,0)
        for block in blocks:
            if (pygame.sprite.collide_rect(self, block) and block != self) and not (block.type == 'sand' and block.is_grounded == False):
                if not self.is_grounded:
                    self.pos.y = block.rect.top - self.height + 1
                    
                self.is_grounded = True
                self.vel.y = 0
                break
                
            self.is_grounded = False
            
        if not self.is_grounded:
            self.acc = self.vec(0,0.5)

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.x, self.rect.y = self.pos
        