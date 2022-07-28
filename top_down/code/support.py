import pygame
import numpy as np
from csv import reader
from os import walk

def import_csv_layout(path):

    with open(path) as level_map:
        terrain_map = []
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))

        return terrain_map

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def get_mouse_pos_directions(width, height, diagonal_offset=300):
    master_dict = {}
    coords = np.array([[x for x in range(width)] for y in range(height)])
    forward_diag = coords.diagonal(offset=diagonal_offset)
    backward_diag = np.fliplr(coords).diagonal(offset=diagonal_offset)

    top, right, bot, left = [], [], [], []
    for y_coord, fd, bd in zip(coords, forward_diag, backward_diag):
        top_list, right_list, bot_list, left_list = [], [], [], []
        for x_coord in y_coord:
            if x_coord >= fd:
                if x_coord >= bd:
                    right_list.append(x_coord)
                else:
                    top_list.append(x_coord)
            else:
                if x_coord >= bd:
                    bot_list.append(x_coord)
                else:
                    left_list.append(x_coord)
                    
        top.append(top_list)
        right.append(right_list)
        bot.append(bot_list)
        left.append(left_list)
    
    for y, y_coord in enumerate(top):
        for x, x_coord in enumerate(y_coord):
            master_dict[str((x_coord, y))] = 'up'
    
    for y, y_coord in enumerate(right):
        for x, x_coord in enumerate(y_coord):
            master_dict[str((x_coord, y))] = 'right'
            
    for y, y_coord in enumerate(bot):
        for x, x_coord in enumerate(y_coord):
            master_dict[str((x_coord, y))] = 'down'
            
    for y, y_coord in enumerate(left):
        for x, x_coord in enumerate(y_coord):
            master_dict[str((x_coord, y))] = 'left'
    
    return master_dict

# offset = 300
# thing = np.array([[x for x in range(1280)] for y in range(720)])
# forward_diagonal = np.diagonal(thing, offset)
# backward_diagonal = np.diagonal(np.fliplr(thing), offset)
# for y, (y_coord, fd, bd) in enumerate(zip(thing, forward_diagonal, backward_diagonal)):
#     for x_coord in y_coord:
#         if x_coord == fd:
#             thing[y][x_coord] = str(x_coord) + str(000) 
#         if x_coord == bd:
#             thing[y][x_coord] = str(x_coord) + str(000) 
# np.savetxt('thing.csv', thing, delimiter=',')