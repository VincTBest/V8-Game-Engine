import os
import pygame
try:
    import pytmx
except ImportError:
    os.system("pip install pytmx")
    import pytmx


def tm_loadTmxMap(path: str) -> pytmx.TiledMap:
    """
    Loads a TMX map from the given file path.
    """
    return pytmx.load_pygame(path)


def tm_getMapDimensions(tmx_data: pytmx.TiledMap) -> tuple[int, int]:
    """
    Returns the pixel width and height of the map.
    """
    width = tmx_data.width * tmx_data.tilewidth
    height = tmx_data.height * tmx_data.tileheight
    return width, height


def tm_drawTileMap(screen: pygame.Surface, tmx_data: pytmx.TiledMap, offset_x=0, offset_y=0):
    """
    Draws the TMX tilemap on the screen with optional x/y offsets (for camera, etc.).
    """
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth + offset_x,
                                       y * tmx_data.tileheight + offset_y))


def tm_getObjectsByType(tmx_data: pytmx.TiledMap, obj_type: str) -> list:
    """
    Returns a list of objects from all object layers that match a specific type.
    """
    result = []
    for obj_group in tmx_data.objectgroups:
        for obj in obj_group:
            if getattr(obj, 'type', '') == obj_type:
                result.append(obj)
    return result


def tm_getLayerByName(tmx_data: pytmx.TiledMap, name: str) -> pytmx.TiledTileLayer:
    """
    Returns a layer by name (usually useful for collision or logic).
    """
    return tmx_data.get_layer_by_name(name)
