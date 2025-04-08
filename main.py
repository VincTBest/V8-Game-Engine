import engine.deps as deps
try:
    import pygame
    # import pyopengl
    # engine.[...] stuff
    import engine.core as core
    import engine.object as object
except ImportError:
    deps.configure(["pygame-ce", "pyopengl"])
    deps.install()
    quit()

core.c_init()
root = core.c_globalWindow("example", 800, 400, "DefaultIcon")

while root.getRunning():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            root.stopSelf()

    screen = root.screen()
    screen.fill([84, 172, 237])
    pygame.display.flip()

if not root.hiding:
    pygame.quit()
