import pygame
from settings import *
from entity import Entity
from support import import_folder


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, slow_sprites):
        # graphics
        self.import_graphics(monster_name)
        self.frame_index = 0
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.hitbox = self.rect.inflate(0, -10)
        self.old_hitbox = self.hitbox.copy()
        super().__init__(groups, self.hitbox)
        # stats
        self.monster_name = monster_name
        self.stats = monster_data[self.monster_name]
        self.health = self.stats['health']
        self.exp = self.stats['exp']
        self.speed = self.stats['speed']
        self.attack_damage = self.stats['damage']
        self.resistance = self.stats['resistance']
        self.attack_radius = self.stats['attack_radius']
        self.notice_radius = self.stats['notice_radius']
        self.attack_type = self.stats['attack_type']

        # graphics
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # sprites
        self.obstacle_sprites = obstacle_sprites
        self.slow_sprites = slow_sprites
        self.sprite_type = 'enemy'

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 4000


    def import_graphics(self, monster_name):
        self.animations = {'idle' : [], 'move' : [], 'attack' : []}
        main_path = f'../graphics/monsters/{monster_name}/'

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self, dt):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        
        # set image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def attack_cooldown(self, dt):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time * dt >= self.attack_cooldown:
                self.can_attack = True


    def update(self, dt):
        self.old_hitbox = self.hitbox.copy()
        self.move(self.speed, dt)
        self.animate(dt)

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
