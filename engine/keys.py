import pygame
import engine.debug as c
c.d_log("Module \"keys.py\" as \"key\" loaded.")

pygame.init()


def k_getKeys():
    """
    Get the current held keys.
    """
    return pygame.key.get_pressed(), pygame.key.get_mods()


def k_isPressed(key: pygame.constants):
    """
    Get if a key is currently pressed.
    """
    return pygame.key.get_pressed()[key] or pygame.key.get_mods() == key
