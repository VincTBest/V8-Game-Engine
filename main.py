import engine.deps as deps
try:
    import pygame
    import pyopengl
except ImportError:
    deps.configure(["pygame", "pyopengl"])
    deps.install()


