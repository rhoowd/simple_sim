# Simple_simulator guiObjects
# Wan Ju Kang
# Dec. 1, 2017

# ----------------------------------------------------------------
# Purpose of Simple Simulator guiObjects is to provide abstraction
# for the drawn target and drones on the Simple Simulator Canvas.
# To use guiObjects, make an instance and blit it on a surface.
# ----------------------------------------------------------------

import pygame
from math import cos, sin, pi
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 100, 0, 128)
BLUE = (0, 128, 255, 128)

class guiTarget():
    def __init__(self, xi = 1, yi = 1, zi = 10, tr = 10):
        # Take initial (x, y, z, radius) as argument
        self.x = xi
        self.y = yi
        self.z = zi
        self.tr = tr
        self.a = None # Not used
        self.name = "target"

        # Label the target
        self.color = ORANGE
        self.fs = 15 # font size
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.fs)
        self.text = "T"
        self.label = self.font.render(self.text, True, BLACK)
        
    def setup(self, sx = 20, sy = 20):
        # Set up target's surface
        self.sx = sx
        self.sy = sy
        self.surface = pygame.Surface((self.sx, self.sy), pygame.SRCALPHA)
        self.surface = self.surface.convert_alpha()

class guiDrone():
    def __init__(self, xi = 1, yi = 1, zi = 10, ai = 0, drone_id = 0):
        # Take initial (x, y, z, yaw, drone_id) as argument
        self.x = xi
        self.y = yi
        self.z = zi
        self.a = ai
        self.drone_id = drone_id
        self.name = "drone" + str(drone_id)

        # Label the drone
        self.body_color = BLUE
        self.eye_color = BLACK
        self.fs = 15 # font size
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.fs)
        self.text = str(drone_id)
        self.label = self.font.render(self.text, True, BLACK)

        # Misc.
        self.eye_size = 0.4

    def setup(self, sx = 25, sy = 25):
        # Set up drone's surface
        self.sx = sx
        self.sy = sy
        self.surface = pygame.Surface((self.sx, self.sy), pygame.SRCALPHA)
        self.surface = self.surface.convert_alpha()

class guiCameraView():
    def __init__(self, ci = (0, 0), si = 20, vx = 64, vy = 64, view_id = 0):
        # Take initial dimensions of view screen and target position on camera view
        self.center = ci
        self.size = si
        self.vx = vx
        self.vy = vy
        self.view_id = view_id
        self.name = "view" + str(view_id)

        # Label the camera view
        self.fs = 20 # font size
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.fs)
        self.text = "Drone " + str(view_id)
        self.label = self.font.render(self.text, True, BLACK)

    def setup(self, sx = 128, sy = 128):
        # Set up camera view's surface
        self.sx = sx
        self.sy = sy
        self.border_thickness = 5
        self.border_color = (0, 0, 0, 128)
        self.surface = pygame.Surface((self.sx, self.sy), pygame.SRCALPHA)
        self.surface = self.surface.convert_alpha()
