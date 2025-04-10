import engine.deps as deps
try:
    import pygame
    # engine.[...] stuff
    import engine.core as core
    import engine.object as objects
except ImportError:
    deps.configure(["pygame"])
    deps.install()
    quit()

core.c_init()
root = core.c_globalWindow("V8 Engine", 1920/5*4, 1080/5*4, "DefaultIcon", 90)

while root.getRunning():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            root.stopSelf()

    root.allTick()
    screen = root.screen()

    pygame.display.flip()

if not root.hiding:
    pygame.quit()
