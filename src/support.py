import pygame
from csv import reader
from os import walk


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    image_surface = pygame.image.load(path).convert_alpha()
    return image_surface



