import engine.core as core
import engine.debug as c
c.d_log("Module \"object.py\" as \"objects\" loaded.")

import pygame
import os

pygame.init()

# ----------- NEW -----------


class o_img:
    def __init__(self, x, y, img, align="1 1", scale=False, smoothScale=False, w=None, h=None):
        self.x = x
        self.y = y
        self.align_x, self.align_y = map(int, align.split())
        if not scale:
            self.img = img
        else:
            if smoothScale:
                self.img = pygame.transform.smoothscale(img, (w, h))
            else:
                self.img = pygame.transform.scale(img, (w, h))

    def draw(self, screen):

        imgRect = self.img.get_rect()
        if self.align_y == 0:
            setattr(imgRect, "top", self.y)
        elif self.align_y == 1:
            setattr(imgRect, "centery", self.y)
        elif self.align_y == 2:
            setattr(imgRect, "bottom", self.y)

        if self.align_x == 0:
            setattr(imgRect, "left", self.x)
        elif self.align_x == 1:
            setattr(imgRect, "centerx", self.x)
        elif self.align_x == 2:
            setattr(imgRect, "right", self.x)

        screen.blit(self.img, imgRect)


class o_text:
    def __init__(self, x, y, text, fontname, fontsize, align="1 1", fontColor=(195, 195, 195)):
        self.x = x
        self.y = y
        self.align_x, self.align_y = map(int, align.split())
        self.text = text
        self.color = fontColor
        self.font = fontname
        self.fontsize = fontsize

    def draw(self, screen):
        font = pygame.font.Font(core.textureLib[self.font], self.fontsize)
        textSurface = font.render(self.text, True, self.color)
        textRect = textSurface.get_rect()
        if self.align_y == 0:
            setattr(textRect, "top", self.y)
        elif self.align_y == 1:
            setattr(textRect, "centery", self.y)
        elif self.align_y == 2:
            setattr(textRect, "bottom", self.y)

        if self.align_x == 0:
            setattr(textRect, "left", self.x)
        elif self.align_x == 1:
            setattr(textRect, "centerx", self.x)
        elif self.align_x == 2:
            setattr(textRect, "right", self.x)
        screen.blit(textSurface, textRect)

    def changeText(self, newText, newColor=None, newFont=None):
        if newColor is not None:
            self.color = newColor
        if newFont is not None:
            self.font = newFont
        self.text = newText


# --------- LEGACY ----------


class LegacyImg:
    def __init__(self, x, y, img, scale, w=0, h=0):
        self.x = x
        self.y = y
        if not scale:
            self.img = img
        else:
            self.img = pygame.transform.smoothscale(img, (w, h))

    def draw(self, screen):

        imgRect = self.img.get_rect()
        imgRect.center = (self.x, self.y)
        screen.blit(self.img, imgRect)

    def SetXY(self, x, y):
        self.x = x
        self.y = y


class LegacyImageBox:
    def __init__(self, x, y, width, height, image_path, border_size):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.border = border_size

        # Load and divide image
        self.image = pygame.image.load(image_path)
        self._slice_image()

    def _slice_image(self):
        """Cuts the image into 9 parts for 9-slice scaling"""
        img_w, img_h = self.image.get_size()
        b = self.border  # Border size alias

        # Extract 9 slices
        self.slices = {
            "tl": self.image.subsurface((0, 0, b, b)),  # Top-left
            "tm": self.image.subsurface((b, 0, img_w - 2 * b, b)),  # Top-middle
            "tr": self.image.subsurface((img_w - b, 0, b, b)),  # Top-right

            "ml": self.image.subsurface((0, b, b, img_h - 2 * b)),  # Middle-left
            "mm": self.image.subsurface((b, b, img_w - 2 * b, img_h - 2 * b)),  # Center
            "mr": self.image.subsurface((img_w - b, b, b, img_h - 2 * b)),  # Middle-right

            "bl": self.image.subsurface((0, img_h - b, b, b)),  # Bottom-left
            "bm": self.image.subsurface((b, img_h - b, img_w - 2 * b, b)),  # Bottom-middle
            "br": self.image.subsurface((img_w - b, img_h - b, b, b)),  # Bottom-right
        }

    def draw(self, screen):
        """Draws the 9-slice image with stretching"""
        b = self.border
        x, y, w, h = self.x, self.y, self.width, self.height

        # Draw corners (fixed)
        screen.blit(self.slices["tl"], (x, y))  # Top-left
        screen.blit(self.slices["tr"], (x + w - b, y))  # Top-right
        screen.blit(self.slices["bl"], (x, y + h - b))  # Bottom-left
        screen.blit(self.slices["br"], (x + w - b, y + h - b))  # Bottom-right

        # Stretch edges
        self._stretch_surface(screen, self.slices["tm"], x + b, y, w - 2 * b, b)  # Top
        self._stretch_surface(screen, self.slices["bm"], x + b, y + h - b, w - 2 * b, b)  # Bottom
        self._stretch_surface(screen, self.slices["ml"], x, y + b, b, h - 2 * b)  # Left
        self._stretch_surface(screen, self.slices["mr"], x + w - b, y + b, b, h - 2 * b)  # Right

        # Stretch center
        self._stretch_surface(screen, self.slices["mm"], x + b, y + b, w - 2 * b, h - 2 * b)

    def _stretch_surface(self, screen, surf, x, y, width, height):
        """Scales a surface to fit a given area"""
        stretched = pygame.transform.scale(surf, (width, height))
        screen.blit(stretched, (x, y))


class LegacyImgTL:
    def __init__(self, x, y, img, scale, w=0, h=0):
        self.x = x
        self.y = y
        if not scale:
            self.img = img
        else:
            self.img = pygame.transform.smoothscale(img, (w, h))

    def draw(self, screen):

        imgRect = self.img.get_rect()
        imgRect.topleft = (self.x, self.y)
        screen.blit(self.img, imgRect)

    def SetXY(self, x, y):
        self.x = x
        self.y = y


class LegacyText:
    def __init__(self, x, y, text, fontsize=24, color=(236, 236, 236), font="Teardown-Regular"):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.fontsize = fontsize

    def draw(self, screen):

        font = pygame.font.Font(core.textureLib[self.font], self.fontsize)
        textSurface = font.render(self.text, True, self.color)
        textRect = textSurface.get_rect()
        textRect.center = (self.x, self.y)
        screen.blit(textSurface, textRect)


class LegacyTextCTL:
    def __init__(self, x, y, text, fontsize=24, custom="", color=(236, 236, 236), font="Teardown-Regular"):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.fontsize = fontsize
        self.ctms = custom
        self.data1 = None
        self.data2 = None
        self.data3 = None
        self.data4 = None
        self.data5 = None

    def draw(self, screen):

        font = pygame.font.Font(core.textureLib[self.font], self.fontsize)
        textSurface = font.render(self.text, True, self.color)
        textRect = textSurface.get_rect()
        textRect.midtop = (self.x, self.y)
        screen.blit(textSurface, textRect)


class LegacyTextTL:
    def __init__(self, x, y, text, fontsize=24, color=(236, 236, 236), font="Teardown-Regular"):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.fontsize = fontsize

    def draw(self, screen):

        font = pygame.font.Font(core.textureLib[self.font], self.fontsize)
        textSurface = font.render(self.text, True, self.color)
        textRect = textSurface.get_rect()
        textRect.topleft = (self.x, self.y)
        screen.blit(textSurface, textRect)


class LegacyTextTLLimit:
    def __init__(self, x, y, text, max_width, fontsize=24, color=(236, 236, 236), font="Teardown-Regular"):
        self.x = x
        self.y = y
        self.text = text
        self.max_width = max_width
        self.color = color
        self.font = font
        self.fontsize = fontsize
        self.lines = []
        self._split_text()

    def _split_text(self):
        font = pygame.font.Font(core.textureLib[self.font], self.fontsize)
        words = self.text.split()
        line = ""
        self.lines = []

        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] <= self.max_width:
                line = test_line
            else:
                self.lines.append(line.strip())
                line = word + " "

        if line:
            self.lines.append(line.strip())

    def draw(self, screen):
        font = pygame.font.Font(core.textureLib[self.font], self.fontsize)
        y_offset = 0

        for line in self.lines:
            text_surface = font.render(line, True, self.color)
            text_rect = text_surface.get_rect(topleft=(self.x, self.y + y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += self.fontsize

    def setText(self, text):
        self.text = text


class LegacyButton:
    def __init__(self, x, y, img, ctms, command, scale=False, w=0, h=0):
        self.x = x
        self.y = y
        self.command = command
        self.ctms = ctms

        if scale and w > 0 and h > 0:
            self.img = pygame.transform.smoothscale(img, (w, h))
        else:
            self.img = img

        self.rect = self.img.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.command:
                    self.command()

    def SetXY(self, x, y):
        self.x = x
        self.y = y

    def resetImg(self, img, scale=False, w=0, h=0):
        if scale and w > 0 and h > 0:
            self.img = pygame.transform.smoothscale(img, (w, h))
        else:
            self.img = img

    def getCtms(self):
        return self.ctms

    def setCtms(self, ctms):
        self.ctms = ctms


class LegacyButtonTL:
    def __init__(self, x, y, img, ctms, command, scale=False, w=0, h=0):
        self.x = x
        self.y = y
        self.command = command
        self.ctms = ctms
        self.clicks = 0
        self.timer = 0
        self.timeout = 650
        self.needClicks = 1

        if scale and w > 0 and h > 0:
            self.img = pygame.transform.smoothscale(img, (w, h))
        else:
            self.img = img

        self.rect = self.img.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicks += 1
                self.timer = self.timeout

                if self.clicks == self.needClicks:
                    if self.command:
                        self.command()
                    self.clicks = 0

    def SetXY(self, x, y):
        self.x = x
        self.y = y

    def resetImg(self, img, scale=False, w=0, h=0):
        if scale and w > 0 and h > 0:
            self.img = pygame.transform.smoothscale(img, (w, h))
        else:
            self.img = img

    def getCtms(self):
        return self.ctms

    def setCtms(self, ctms):
        self.ctms = ctms

    def update(self, dt):
        if self.timer > 0:
            self.timer -= dt
            if self.timer <= 0:
                self.timer = 0
                if self.clicks > 0:
                    self.clicks -= 1
