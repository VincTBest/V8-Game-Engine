import engine.deps as deps
try:
    import pygame
    import engine.v8 as v8
except ImportError:
    deps.configure(["pygame"])
    deps.install()
    quit()

v8.core.c_init()
root = v8.core.c_globalWindow("V8 Engine", 1920/5*4, 1080/5*4, "DefaultIcon", 90)

map1 = v8.tile_map.tm_loadTmxMap(".\\map1.tmx")

while root.getRunning():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            root.stopSelf()

    root.allTick()
    screen = root.screen()

    pygame.display.flip()

if not root.hiding:
    pygame.quit()
