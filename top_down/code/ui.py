import pygame
from settings import *

class UI:
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar_rect = pygame.Rect(10, 34, MANA_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictonary
        self.weapon_graphics = [pygame.image.load(weapon['graphic']).convert_alpha() for weapon in weapon_data.values()]
        self.spell_graphics = [pygame.image.load(spell['graphic']).convert_alpha() for spell in spell_data.values()]

    def show_bar(self, current_amount, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # convert stat to pixel
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(topright = (WIDTH - 10, 7))

        self.display_surface.blit(text_surf, text_rect)

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index):
        bg_rect = self.selection_box(25, 590)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def spell_overlay(self, spell_index):
        bg_rect = self.selection_box(105, 600)
        spell_surf = self.spell_graphics[spell_index]
        spell_rect = spell_surf.get_rect(center = bg_rect.center)
        self.display_surface.blit(spell_surf, spell_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.mana, player.stats['health'], self.mana_bar_rect, MANA_COLOR)

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index)
        self.spell_overlay(player.spell_index)