# if it works, don't touch it (prime-example)

import pygame
import os
import engine.object as objects

pygame.init()

# asset loading

textureLib = {}
basePath = ""
pack = "default"

# CONSTANTS

ENGINE_VER = "0.0.2"

# not CONSTANTS


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


def c_loadImage(path, newW=None, newH=None):
    image = pygame.image.load(path)
    if newW is not None and newH is not None:
        image = pygame.transform.smoothscale(image, [newW, newH])
    return image


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


class c_timer:
    def __init__(self, msTime, command, tick, adjust=0, elseCommand=None, times=1):
        self.time = msTime
        self.command = command
        self.elseCommand = elseCommand
        self.adjust = adjust
        self.startTick = tick
        self.endTick = tick + msTime + adjust
        self.maxRuns = times

    def allTick(self, tick):
        if self.maxRuns > 0:
            if tick >= self.endTick:
                self.command()
                self.maxRuns -= 1
                if self.maxRuns > 0:
                    self.startTick = tick
                    self.endTick = tick + self.time + self.adjust
            elif self.elseCommand is not None:
                self.elseCommand()


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
    c_addAssets("V8Logo2048", "v8-2048x.png", engine=True)
    c_addAssets("noto", "notosans.ttf", engine=True)

# windows


class c_globalWindow:
    def __init__(self, title=f"V8 Engine {ENGINE_VER} Window", w=1920/5*3, h=1080/5*3, icon="DefaultIcon", FPS=90):
        self.w = w
        self.h = h
        self.title = title
        self.icon = icon
        self.screenV = pygame.display.set_mode((self.w, self.h))
        self.e = 5
        self.running = True
        self.hiding = False
        self.tick = 0
        self.clockV = pygame.time.Clock()
        self.dtV = 1
        self.targetFps = FPS
        self.v8logo = objects.o_img(self.w/2, self.h/2, c_loadImage(textureLib["V8Logo2048"]), "1 1", True, True, self.w/8*3.5, self.w/8*3.5)
        self.versionText = objects.o_text(self.w/2, self.h/32*1.70, ENGINE_VER, "noto", 38, "1 1", (39, 39, 39))
        self.scene = "startup"
        self.scenario = 0
        self.tasks = {}
        self.deleteBlacklist = [0]
        self.addTask(0, "V8Logo", "230 Tick long V8 logo", "Can not be deleted")
        pygame.display.set_caption(title)
        pygame.display.set_icon(c_loadImageLib(icon))

    def addTask(self, taskId, taskInfo1="", taskInfo2="", taskInfo3=""):
        self.tasks[taskId] = {}
        self.tasks[taskId]["info1"] = taskInfo1
        self.tasks[taskId]["info2"] = taskInfo2
        self.tasks[taskId]["info3"] = taskInfo3
        self.tasks[taskId]["isDone"] = False

    def changeTask(self, taskId, isDone):
        self.tasks[taskId]["isDone"] = isDone

    def deleteTask(self, taskId):
        if taskId not in self.deleteBlacklist:
            del self.tasks[taskId]

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

    def tickSelf(self):
        self.tick = self.tick + 1

    def allTick(self):
        self.dtV = self.clockV.tick(self.targetFps)
        self.tickSelf()
        if self.tick <= 230:
            self.screenV.fill([121, 99, 255])
            self.v8logo.draw(self.screenV)
            self.versionText.draw(self.screenV)
            self.e = 1
        else:
            if self.e == 1:
                self.changeTask(0, True)
            self.e -= 1
            self.screenV.fill([21, 21, 21])

    def deltaTime(self):
        return self.dtV

    def changeScene(self, newScene, newScenario=0):
        self.scene = newScene
        self.scenario = newScenario

    def getFps(self):
        return self.clockV.get_fps()

    def doneWithTask(self, taskId):
        return self.tasks[taskId]["isDone"]
