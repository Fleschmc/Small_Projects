from email.errors import ObsoleteHeaderDefect
import pygame
from player import Player
from tile import Tile
from weapon import Weapon
from ui import UI
from enemy import Enemy
from support import *
from settings import *
from debug import debug
from random import choice


class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.slow_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # weapon
        self.current_attack = None

        # user interface
        self.ui = UI()

    def create_map(self):

        layouts = {
            'boundary' : import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass' : import_csv_layout('../map/map_Grass.csv'),
            'object' : import_csv_layout('../map/map_Objects.csv'),
            'entities' : import_csv_layout('../map/map_Entities.csv')
        }

        graphics = {
            'grass' : import_folder('../graphics/Grass'),
            'objects' : import_folder('../graphics/objects')
        }

        for style, layout in  layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.slow_sprites], 'grass', random_grass_image)

                        elif style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        elif style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.slow_sprites, self.create_attack, self.destroy_attack, self.cast_spell)
                            elif col == '390': monster_name = 'bamboo'
                            elif col == '391': monster_name = 'spirit'
                            elif col == '392': monster_name ='raccoon'
                            else: monster_name = 'squid'
                            self.enemy = Enemy(monster_name, (x, y), [self.visible_sprites], self.obstacle_sprites, self.slow_sprites)

    def create_attack(self):
        if self.player.attacking:
            self.current_attack = Weapon(self.player, [self.visible_sprites])

    def cast_spell(self, style, strength, cost):
        print(style, strength, cost)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self, dt):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update(dt)
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)

        debug((self.player.speed, self.player.status, self.player.mouse_pos))

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
        # General Setup
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0)) 
    
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)