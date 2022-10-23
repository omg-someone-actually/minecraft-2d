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

        self.paused_icon = pygame.transform.scale(pygame.image.load('assets/paused.PNG').convert_alpha(), (self.width/2, self.height/2))
        self.block_outline = pygame.transform.scale(pygame.image.load('assets/block-outline.png').convert_alpha(), (100, 100))
        self.selected_block_outline = pygame.transform.scale(pygame.image.load('assets/block-outline.png').convert_alpha(), (50, 50))
        self.full_heart = pygame.transform.scale(pygame.image.load('assets/heart.png').convert_alpha(), (30,30))
        self.half_heart = pygame.transform.flip(pygame.transform.scale(pygame.image.load('assets/halfheart.png').convert_alpha(), (30,30)), True, False)
        self.empty_heart = pygame.transform.scale(pygame.image.load('assets/noheart.png').convert_alpha(), (30,30))
        self.damaged_heart = pygame.transform.scale(pygame.image.load('assets/damagedheart.png').convert_alpha(), (20,20))
        
        self.player = pygame.transform.scale(pygame.image.load('assets/steve.PNG').convert_alpha(), (75, 150))
        self.player = Player(self.player, 75, 150, self.screen)
        self.player.move(None, [], 1, 1, False)

        self.zombies = {}
        
        self.x, self.y, = 1, 1
        self.blocks = {}
        self.selected_block = 'stone'
        self.selectable_blocks = ['stone', 'coal', 'gold', 'redstone', 'grass', 'sand', 'water', 'dirt', 'glass', 'plank', 'leaves', 'log', 'tnt']
        self.paused = False

        self.load_assets()
        self.generate_map()
        self.screen_update()

    def load_assets(self) -> None:
        assets = ['dirt', 'stone', 'coal', 'gold', 'redstone', 'grass', 'sand', 'water', 'glass', 'plank', 'leaves', 'log', 'tnt']
        self.textures = {}
        self.mini_blocks = {}
        
        for asset in assets:
            self.textures[asset.lower()] = pygame.transform.scale(pygame.image.load(f'assets/{asset}.PNG').convert(), (100,100))
            self.mini_blocks[asset.lower()] = pygame.transform.scale(pygame.image.load(f'assets/{asset}.PNG').convert(), (50,50))

    def generate_map(self) -> None:
        x, y = self.x, self.y
        biomes = ['desert', 'plains', 'ocean']
        
        if not x in self.blocks:
            self.blocks[x] = {}
            self.blocks[x][1] = []
            self.zombies[x] = {}
            self.zombies[x][1] = []

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
            self.zombies[x][y] = []
            for i in range(self.total_blocks_y):
                for x_cord, texture in enumerate(choices(['stone', 'coal', 'gold', 'redstone'], weights=[50, 10, 1, 2], k=self.total_blocks_x)):
                    self.blocks[x][y].append(Block(self.textures[texture], x_cord*100, self.height-((i+1)*100), self.screen, self.background, texture, self.blocks[x][y]))

    def spawn_zombie(self) -> None:
        zombie = pygame.transform.scale(pygame.image.load('assets/zombie.PNG').convert_alpha(), (75, 150))
        zombie = Zombie(zombie, 75, 150, self.screen)
        self.zombies[self.x][self.y].append(zombie)

    def add_block(self, x: int, y: int) -> None:
        for block in self.blocks[self.x][self.y]:
            if block.pos == (x, y):
                return
        new_block = Block(self.textures[self.selected_block], x, y, self.screen, self.background, self.selected_block, self.blocks[self.x][self.y])
        if not pygame.sprite.collide_rect(new_block, self.player) and not any([pygame.sprite.collide_rect(zombie, new_block) for zombie in self.zombies[self.x][self.y]]):
            self.blocks[self.x][self.y].append(new_block)

    def remove_block(self, x: int, y: int, tnt_blast=False) -> None:
        for block in self.blocks[self.x][self.y]:                    
            if block.rect.collidepoint(x, y):
                if tnt_blast and block.type == 'water':
                    continue
                self.blocks[self.x][self.y].remove(block)
                if block.type == 'tnt':
                    coordinates_to_remove = [(x-100, y), (x+100, y), (x-100, y-100), (x-100, y+100), (x+100, y-100), (x+100, y+100), (x, y-100), (x, y+100)]
                    for coords in coordinates_to_remove:
                        self.remove_block(*coords, tnt_blast=True)
                        if self.player.rect.collidepoint(*coords) and self.player.last_damaged_time > 50:
                            self.player.health -= 8
                            self.player.last_damaged_time = 0
                        for zombie in self.zombies[self.x][self.y]:
                            if zombie.rect.collidepoint(*coords) and zombie.last_damaged_time > 10:
                                zombie.health -= 5
                                zombie.last_damaged_time = 0

    def render_screen(self) -> None:
        self.screen.blit(self.background, (0,0))
        
        for block in self.blocks[self.x][self.y]:
            block.show()

        hearts_shown = 0
        for i in range(10):
            if hearts_shown + 2 <= self.player.health:
                self.screen.blit(self.full_heart, (self.width-((i+1)*35), 10))
                hearts_shown += 2
            elif hearts_shown + 1 <= self.player.health:
                self.screen.blit(self.half_heart, (self.width-((i+1)*35), 10))
                hearts_shown += 1
            else:
                self.screen.blit(self.empty_heart, (self.width-((i+1)*35), 10))

        for zombie in self.zombies[self.x][self.y]:
            if zombie.last_damaged_time < 100 and zombie.health < 10:
                self.screen.blit(self.damaged_heart, (zombie.rect.x+20, zombie.rect.y-25))

        if self.player.last_damaged_time < 100 and self.player.health < 20:
            self.screen.blit(self.damaged_heart, (self.player.rect.x+20, self.player.rect.y-25))

        
        x, y = pygame.mouse.get_pos()
        x, y = round((x-50)/100)*100, (round((y-100)/100)*100)+self.y_offset
        self.screen.blit(self.block_outline, (x, y))
            
        self.text = self.font.render(f'x={self.player.x_level} y={self.player.y_level}', True, (255, 255, 255), (0, 0, 0))
        self.screen.blit(self.text, (0, 0))
        if self.selectable_blocks.index(self.selected_block)-1 >= 0:
            self.screen.blit(self.mini_blocks[self.selectable_blocks[self.selectable_blocks.index(self.selected_block)-1]], (0, 50))
        if self.selectable_blocks.index(self.selected_block)+1 < len(self.selectable_blocks)-1:
            self.screen.blit(self.mini_blocks[self.selectable_blocks[self.selectable_blocks.index(self.selected_block)+1]], (100, 50))
        self.screen.blit(self.mini_blocks[self.selected_block], (50, 50))
        self.screen.blit(self.selected_block_outline, (50, 50))

    def restart_game(self) -> None:
        self.blocks = {}
        self.zombies = {}
        self.x, self.y = 1, 1
        self.player.health = 20
        self.player.last_damaged_time = 0
        self.generate_map()
    

    def event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                if event.button == 1:
                    for zombie in self.zombies[self.x][self.y]:
                        if zombie.rect.collidepoint(event.pos) and zombie.last_damaged_time > 10:
                            zombie.health -= 2
                            zombie.last_damaged_time = 0
                    x, y = event.pos
                    self.remove_block(x, y)
                    
                elif event.button == 3:
                    x, y = event.pos
                    x, y = round((x-50)/100)*100, (round((y-100)/100)*100)+self.y_offset
                    self.add_block(x, y)
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not self.paused:
                    self.restart_game()
                    
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    
                elif event.key == pygame.K_z and not self.paused:
                    self.spawn_zombie()
                    
            elif event.type == pygame.MOUSEWHEEL:
                selected_block_index = self.selectable_blocks.index(self.selected_block)
                new_index = selected_block_index + event.y
                self.selected_block = self.selectable_blocks[new_index if not new_index < 0 and not new_index > len(self.selectable_blocks)-1 else selected_block_index]
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

        self.x, self.y = self.player.move(new_move if not self.paused else None, self.blocks[self.x][self.y], self.x, self.y, keys[pygame.K_LSHIFT])
        self.player.y_level = int(int(self.height - self.player.pos.y) / 100) + ((self.y-1) * 9)
        self.player.x_level = int(int(self.player.pos.x - self.width) / 100) + ((self.x-1) * 16)
        self.generate_map()
        
        for zombie in self.zombies[self.x][self.y]:
            zombie.move(self.blocks[self.x][self.y], self.player if not self.paused else None)
            if pygame.sprite.collide_rect(zombie, self.player) and self.player.last_damaged_time > 50:
                self.player.health -= 1
                self.player.last_damaged_time = 0
                
    def check_health(self) -> None:
        self.player.last_damaged_time += 1
        self.player.heal_time += 1
        for zombie in self.zombies[self.x][self.y]:
            zombie.last_damaged_time += 1
            zombie.heal_time += 1
            if zombie.health <= 0:
                self.zombies[self.x][self.y].remove(zombie)
            if zombie.last_damaged_time > 1000 and zombie.heal_time > 200 and zombie.health < 10:
                zombie.health += 1
                zombie.heal_time = 0
        if self.player.health <= 0:
            self.paused = True
            self.restart_game()
        if self.player.last_damaged_time > 500 and self.player.heal_time > 100 and self.player.health < 20:
            self.player.health += 1
            self.player.heal_time = 0
                

    def screen_update(self) -> None:
        while True:
            pygame.display.update()
            if not self.paused:
                self.render_screen()
                
            self.event_handler()
            self.move_entities()
            
            if self.paused:    
                self.screen.blit(self.paused_icon, self.paused_icon.get_rect(center = self.screen.get_rect().center))
                
            self.check_health()
            
            pygame.event.pump()
            self.clock.tick(100)
                
if __name__ == '__main__':
    Minecraft()