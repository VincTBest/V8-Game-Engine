# if it works, don't touch it (prime-example)

import pygame
import os

pygame.init()

# asset loading

textureLib = {}
basePath = ""
pack = "default"


def c_j(*paths):
    return os.path.join(*paths)


def c_changePack(newpack):
    """Changes the active texture pack and reloads assets."""
    global pack
    pack = newpack
    c_loadAssets()


def c_basePath(engine=False, secondaryLoad=""):
    global pack
    path2 = "game"
    if engine:
        path2 = "engine"
    else:
        if secondaryLoad != "":
            path2 = secondaryLoad

    return c_j(path2, pack)


def c_addAssets(name, *paths, engine=False, secondaryLoad=""):
    global textureLib
    global basePath
    basePath = c_basePath(engine, secondaryLoad)

    textureLib[name] = c_j(basePath, *paths)


def c_loadAssets(engine=False):
    global textureLib
    global basePath
    basePath = c_basePath(engine)

    textureLib = {
        "FallbackFont": c_j(basePath, "font", "bold.ttf")

    }

# debug (d_)


def d_log(msg, t=0, ext=""):
    ext2 = ""
    if ext != "":
        ext2 = f"::{ext}"

    if t == 0:
        print(f"[INFO{ext2}]: {msg}")
    elif t == 1:
        print(f"[WARN{ext2}]: {msg}")
    elif t == 2:
        print(f"[ERROR{ext2}]: {msg}")
    elif t == 3:
        print(f"[{ext2}]: {msg}")

# init


def c_init():
    c_changePack("pack")
    c_loadAssets(True)
    c_addAssets("DefaultIcon", "DefaultLogo.png", engine=True)

# windows


def c_loadImageLib(name, nSize=None):
    global textureLib

    if nSize is None:
        nSize = [1, 1]
    path = textureLib[name]

    try:
        image = pygame.image.load(path).convert_alpha()
        scaleAmount = 0
        width, height = image.get_size()
        new_size = (int(width * (1-scaleAmount/100)*nSize[0]), int(height * (1-scaleAmount/100))*nSize[1])
        scaled_image = pygame.transform.scale(image, new_size)
        return scaled_image
    except pygame.error:
        d_log(f"Error loading image: {path}", 3)
        return None


class c_globalWindow:
    def __init__(self, title, w, h, icon):
        self.w = w
        self.h = h
        self.title = title
        self.icon = icon
        self.screenV = pygame.display.set_mode((self.w, self.h))
        self.running = True
        self.hiding = False
        self.tick = 0
        pygame.display.set_caption(title)
        pygame.display.set_icon(c_loadImageLib(icon))

    def screen(self):
        return self.screenV

    def getRunning(self):
        return self.running

    def stopSelf(self):
        self.running = False
        self.hiding = True

    def hide(self):
        self.hiding = True
        self.running = False

    def show(self):
        self.running = True
        self.hiding = False

    def tick(self):
        self.tick = self.tick + 1
