import pygame
from support import import_folder, get_mouse_pos_directions
from entity import Entity
from settings import *

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, slow_sprites, create_attack, destroy_attack, cast_spell):
        # setup 
        self.frame_index = 0
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.old_hitbox = self.hitbox.copy()

        super().__init__(groups, self.hitbox)

        # graphics
        self.import_player_assets()
        self.status = 'down'

        # movement
        self.mouse_pos = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 0
        self.attack_time = None

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.mouse_pos_directions = get_mouse_pos_directions(WIDTH, HEIGHT)
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 250

        # magic
        self.cast_spell = cast_spell
        self.spell_index = 0
        self.spell = list(spell_data.keys())[self.spell_index]
        self.can_switch_spell = True
        self.spell_switch_time = None


        # stats
        self.stats = {'health' : 100, 'mana' : 100, 'attack' : 10, 'magic' : 4, 'speed' : 200}
        self.health = self.stats['health']
        self.mana = self.stats['mana']
        self.speed = self.stats['speed']
        self.exp = 0

        # sprites
        self.obstacle_sprites = obstacle_sprites
        self.slow_sprites = slow_sprites
        self.sprite_type = 'player'

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'up' : [], 'down' : [], 'left' : [], 'right' : [],
                    'up_idle' : [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : [],
                    'up_attack' : [], 'down_attack' : [], 'left_attack' : [], 'right_attack' : [],}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        self.mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed(num_buttons=3)
        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # attack input
        if mouse[0] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.status = self.mouse_pos_directions[str(self.mouse_pos)]

        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_index += 1
            if self.weapon_index > len(list(weapon_data.keys())) - 1:
                self.weapon_index = 0
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon = list(weapon_data.keys())[self.weapon_index]


        # magic input
        if keys[pygame.K_1] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

            style = list(spell_data.keys())[self.spell_index]
            strength = spell_data[style]['strength'] + self.stats['magic']
            cost = spell_data[style]['cost']
            self.cast_spell(style, strength, cost)

        if keys[pygame.K_e] and self.can_switch_spell:
            self.can_switch_spell = False
            self.spell_index += 1
            if self.spell_index > len(list(spell_data.keys())) - 1:
                self.spell_index = 0
            self.spell_switch_time = pygame.time.get_ticks()
            self.spell = list(spell_data.keys())[self.spell_index]

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        if self.attacking:
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
            else:
                self.status = self.status.replace('_atack', '')

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_spell:
            if current_time - self.spell_switch_time >= self.switch_duration_cooldown:
                self.can_switch_spell = True
        
    def animate(self, dt):
        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
    def update(self, dt):
        self.old_hitbox = self.hitbox.copy()
        self.input()
        self.destroy_attack()
        self.create_attack()
        self.cooldowns()
        self.get_status()
        self.animate(dt)
        self.move(self.speed, dt)