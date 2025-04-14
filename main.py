import engine.deps as deps
try:
    import pygame
    import engine.v8 as v8
except ImportError:
    deps.configure(["pygame"])
    deps.install()
    quit()

pygame.init()

v8.core.c_init()
root = v8.core.c_globalWindow("V8 Engine", 1920/5*4, 1080/5*4, "DefaultIcon", 90)
root.configure(v8logoDisable=True)

map1 = v8.tile_map.tm_loadTmxMap(".\\map1.tmx")

xScroll, yScroll = root.w/2, root.h/2

while root.getRunning():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            root.stopSelf()

    root.allTick()

    screen = root.screen()
    v8.tile_map.tm_drawTileMap(screen, map1, xScroll, yScroll)

    stepValue = 0.35

    if v8.key.k_isPressed(pygame.K_q):
        stepValue = 0.5

    stepAmount = stepValue * root.deltaTime()

    if v8.key.k_isPressed(pygame.K_w):
        yScroll += stepAmount

    if v8.key.k_isPressed(pygame.K_s):
        yScroll -= stepAmount

    if v8.key.k_isPressed(pygame.K_a):
        xScroll += stepAmount

    if v8.key.k_isPressed(pygame.K_d):
        xScroll -= stepAmount

    pygame.display.flip()

if not root.hiding:
    pygame.quit()
