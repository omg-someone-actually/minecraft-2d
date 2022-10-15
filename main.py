import pygame
from random import choice, choices

class Minecraft:
    def __init__(self) -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode()
        self.width, self.height = pygame.display.get_surface().get_size()
        pygame.display.set_caption('Hello World!')
        
        self.background = pygame.transform.scale(pygame.image.load('assets/sky.PNG').convert(), (self.width, self.height))
        self.screen.blit(self.background, (0,0))
        
        self.load_assets()
        self.generate_map()
        self.screen_update()

    def load_assets(self) -> None:
        assets = ['Tnt', 'Dirt', 'Stone', 'Coal', 'Gold', 'Redstone']
        self.textures = {}
        for asset in assets:
            self.textures[asset.lower()] = pygame.transform.scale(pygame.image.load(f'assets/{asset}.PNG').convert(), (100,100))

    def generate_map(self) -> None:
        bottom_layer = choices(['stone', 'coal', 'gold', 'redstone'], weights=[30, 4, 1, 2], k=15)
        for i, texture in enumerate(bottom_layer):
            self.screen.blit(self.textures[texture], (i*100, self.height-100))

    def screen_update(self) -> None:
        while True:
            pygame.display.update()
                


if __name__ == '__main__':
    Minecraft()