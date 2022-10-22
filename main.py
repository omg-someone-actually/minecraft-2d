import pygame
from random import choices
import math
from block import Block
from sprites import Player, Zombie

class Minecraft:
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode()
        self.width, self.height = pygame.display.get_surface().get_size()
        pygame.display.set_caption('Minecraft!')
        self.font = pygame.font.Font('freesansbold.ttf', 50)
        self.y_offset = self.height - math.floor(self.height/100)*100 
        self.total_blocks_x = math.ceil(self.width / 100)
        self.total_blocks_y = math.ceil(self.height / 100)
        
        self.background = pygame.transform.scale(pygame.image.load('assets/sky.PNG').convert(), (self.width, self.height))
        self.screen.blit(self.background, (0,0))

        self.paused_icon = pygame.transform.scale(pygame.image.load('assets/paused.PNG').convert(), (self.width, self.height))
        
        self.player = pygame.transform.scale(pygame.image.load('assets/steve.PNG').convert_alpha(), (75, 150))
        self.player = Player(self.player, 75, 150, self.screen)
        self.player.move(None, [], 1, 1)

        self.zombies = []
        
        self.x, self.y, = 1, 1
        self.blocks = {}
        self.selected_block = 'stone'
        self.selectable_blocks = ['stone', 'coal', 'gold','redstone', 'grass', 'sand', 'water', 'dirt', 'glass', 'plank']
        self.paused = False
        self.y_level = 0
        self.x_level = 0

        self.load_assets()
        self.generate_map()
        self.screen_update()

    def load_assets(self) -> None:
        assets = ['dirt', 'stone', 'coal', 'gold', 'redstone', 'grass', 'sand', 'water', 'glass', 'plank']
        self.textures = {}
        
        for asset in assets:
            self.textures[asset.lower()] = pygame.transform.scale(pygame.image.load(f'assets/{asset}.PNG').convert(), (100,100))

    def generate_map(self) -> None:
        x, y = self.x, self.y
        biomes = ['desert', 'plains', 'ocean']
        
        if not x in self.blocks:
            self.blocks[x] = {}
            self.blocks[x][1] = []

            selected_biome = choices(biomes, weights=[6, 10, 4], k=1)[0]
            if x == 1:
                selected_biome = 'plains'
            if selected_biome == 'plains':
                for i in range(2):    
                    for x_cord, texture in enumerate(['dirt' for i in range(self.total_blocks_x)]):
                        self.blocks[x][1].append(Block(self.textures[texture], x_cord*100, self.height-((i+1)*100), self.screen, self.background, texture, self.blocks[x][1]))
                for x_cord, texture in enumerate(['grass' for i in range(self.total_blocks_x)]):
                    self.blocks[x][1].append(Block(self.textures[texture], x_cord*100, self.height-(300), self.screen, self.background, texture, self.blocks[x][1]))
            elif selected_biome == 'ocean':
                for x_cord, texture in enumerate(['stone' for i in range(self.total_blocks_x)]):
                    self.blocks[x][1].append(Block(self.textures[texture], x_cord*100, self.height-100, self.screen, self.background, texture, self.blocks[x][1]))
                for i in range(2):
                    for x_cord, texture in enumerate(['water' for i in range(self.total_blocks_x)]):
                        self.blocks[x][1].append(Block(self.textures[texture], x_cord*100, self.height-((i+2)*100), self.screen, self.background, texture, self.blocks[x][1]))
            elif selected_biome == 'desert':
                for x_cord, texture in enumerate(['stone' for i in range(self.total_blocks_x)]):
                    self.blocks[x][1].append(Block(self.textures[texture], x_cord*100, self.height-100, self.screen, self.background, texture, self.blocks[x][1]))
                for i in range(2):
                    for x_cord, texture in enumerate(['sand' for i in range(self.total_blocks_x)]):
                        self.blocks[x][1].append(Block(self.textures[texture], x_cord*100, self.height-((i+1)*100), self.screen, self.background, texture, self.blocks[x][1]))
        if not y in self.blocks[x]:
            self.blocks[x][y] = []
            for i in range(self.total_blocks_y):
                for x_cord, texture in enumerate(choices(['stone', 'coal', 'gold', 'redstone'], weights=[50, 10, 1, 2], k=self.total_blocks_x)):
                    self.blocks[x][y].append(Block(self.textures[texture], x_cord*100, self.height-((i+1)*100), self.screen, self.background, texture, self.blocks[x][y]))

    def spawn_zombie(self) -> None:
        zombie = pygame.transform.scale(pygame.image.load('assets/zombie.PNG').convert_alpha(), (75, 150))
        zombie = Zombie(zombie, 75, 150, self.screen)
        self.zombies.append(zombie)

    def add_block(self, x, y) -> None:
        for block in self.blocks[self.x][self.y]:
            if block.pos == (x, y):
                return
        new_block = Block(self.textures[self.selected_block], x, y, self.screen, self.background, self.selected_block, self.blocks[self.x][self.y])
        if not pygame.sprite.collide_rect(new_block, self.player) and not any([pygame.sprite.collide_rect(zombie, new_block) for zombie in self.zombies]):
            self.blocks[self.x][self.y].append(new_block)

    def remove_block(self, x, y) -> None:
        for block in self.blocks[self.x][self.y]:                    
            if block.rect.collidepoint(x, y):
                self.blocks[self.x][self.y].remove(block)

    def render_screen(self) -> None:
        self.screen.blit(self.background, (0,0))
        self.text = self.font.render(f'x={self.x_level} y={self.y_level}', True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(self.text, (0, 0))
        self.screen.blit(pygame.transform.scale(pygame.image.load(f'assets/{self.selected_block}.PNG').convert(), (50,50)), (0, 50))
        
        for block in self.blocks[self.x][self.y]:
            block.show()

    def event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                if event.button == 1:
                    x, y = event.pos
                    self.remove_block(x, y)
                    
                elif event.button == 3:
                    x, y = event.pos
                    x, y = round(x/100)*100, (round(y/100)*100)+self.y_offset
                    self.add_block(x, y)
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not self.paused:
                    self.blocks = {}
                    self.zombies = []
                    self.x, self.y = 1, 1
                    self.generate_map()
                    
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    
                elif event.key in range(48, 58) and not self.paused:
                    self.selected_block = self.selectable_blocks[event.key-48]
                    
                elif event.key == pygame.K_z and not self.paused:
                    self.spawn_zombie()
                    
            elif event.type == pygame.QUIT:
                pygame.quit()
                
    def move_entities(self) -> None:
        keys = pygame.key.get_pressed()
        moves = {pygame.K_UP: 'jump', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right', pygame.K_DOWN: 'down'}
        new_move = None
        
        for move in moves:
            if keys[move]:
                new_move = moves[move]
                break

        self.x, self.y = self.player.move(new_move if not self.paused else None, self.blocks[self.x][self.y], self.x, self.y)
        self.y_level = int(int(self.height - self.player.pos.y) / 100) + ((self.y-1) * 9)
        self.x_level = int(int(self.player.pos.x - self.width) / 100) + ((self.x-1) * 16)
        self.generate_map()
        
        for zombie in self.zombies:
            zombie.move(self.blocks[self.x][self.y], self.player if not self.paused else None)

    def screen_update(self) -> None:
        while True:
            pygame.display.update()
            if not self.paused:
                self.render_screen()
                
            self.event_handler()
            self.move_entities()
            
            if self.paused:    
                self.screen.blit(self.paused_icon, (0, 0))

            pygame.event.pump()
            self.clock.tick(100)
                
if __name__ == '__main__':
    Minecraft()