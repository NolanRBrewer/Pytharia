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
    # surface_list = []
    for _, __, img_file in walk(path):
        # print(img_file)
        for image in img_file:
            # print(image)
            full_path = f"{path}/{image}"
            # print(full_path)
            image_surface = pygame.image.load(full_path).convert_alpha()
            # surface_list.append(image_surface)
        return image_surface


# import_folder('./level_graphics/environment/bush')
