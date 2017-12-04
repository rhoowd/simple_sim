# Simple_simulator Canvas
# Wan Ju Kang
# Dec. 1, 2017

# --------------------------------------------------------------
# Purpose of Simple Simulator is to test learning algorithms
# in a very simple environment, before testing them
# in the more complicated Gazebo environments.
# --------------------------------------------------------------

import random
import socket
import threading
import json
import pygame
import ConfigParser

from time import sleep
from math import pi, sin, cos, sqrt, ceil, floor
from guiObjects import guiTarget, guiDrone, guiCameraView

config = ConfigParser.ConfigParser()
config.read("params.cfg")
num_drones = config.getint("CanvasParams", "num_drones")
HOST = config.get("CanvasParams", "host")
PORT = config.getint("CanvasParams", "port")
resolution = (config.getint("CanvasParams", "resolutionx"), config.getint("CanvasParams", "resolutiony"))
#print resolution, type(resolution[0]), type(resolution[1])

GREY = (25, 25, 25, 128)
WHITE = (255, 255, 255, 0)
ORANGE = (255, 100, 0, 128)
RED = (255, 0, 0)
GREEN = (0, 153, 76, 128)

class Canvas():
    def __init__(self, wx = 2560, wy = 1440, num_drones = 3):
        # Take resolution and number of trackers as argument

        # --- Some PyGame-related initialization ---
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((wx, wy))
        pygame.display.set_caption("Sim Sim")
        #self.movable_surface = self.display_surface.copy()
        self.movable_surface = pygame.Surface((wx*2, wy*2))
        self.mx = self.movable_surface.get_width()
        self.my = self.movable_surface.get_height()
        self.done = False

        # --- Diplay screen resolution ---
        # Frame is fixed
        self.framex = wx
        self.framey = wy

        # Movable surface is variable
        self.wx = self.mx
        self.wy = self.my
        self.zoom_sensitivity = 1.02 # Change this to zoom faster
        self.pan_sensitivity = 5 # Change this to move screen faster
        self.sx = 0
        self.sy = 0

        # --- Testing for scroll ---
        self.tx = 0
        self.ty = 0
        
        self.center_mark_size_px = 10
        self.center_mark_thickness_px = 1
        self.button_size_px = 50
        
        # List for keeping guiObjects
        self.num_drones = num_drones
        self.guiObjectsList = []

        # Socket parameters
        self.update_freq = 0.02

        # Camera view parameters
        # vx, vy: resolution
        # vmargin: view-to-view margin
        self.vx = 128
        self.vy = 128
        self.vmargin = 5

        # Correctors for intuitive viewing
        self.angle_corrector = 90
        self.x_corrector = self.mx/2
        self.y_corrector = self.my/2
        self.cam_view_scaler = 2
        
    def setup(self):
        
        # --- Socket setup ---
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))
        self.send({"src": "Canvas"})  # by kdw
        # sleep(1)
        # threading._start_new_thread(self.update_requester, ())

        threading._start_new_thread(self.recv_update, ())

        # --- JSON setup ---
        self.decoder = json.JSONDecoder()

        # --- guiObjects setup ---
        # Randomly positioned for now... get real values later
        self.target_cnt = 1 # Allow only one target
        self.target_size_px = 20 # The size of the target in pixels

        self.btn_pause_surface = pygame.Surface((self.button_size_px, self.button_size_px), pygame.SRCALPHA)
        self.btn_pause_surface = self.btn_pause_surface.convert_alpha()
        self.btn_pause_surface.fill(WHITE)

        self.btn_play_surface = pygame.Surface((self.button_size_px, self.button_size_px), pygame.SRCALPHA)
        self.btn_play_surface = self.btn_play_surface.convert_alpha()
        self.btn_play_surface.fill(WHITE)

        self.btn_ff_surface = pygame.Surface((self.button_size_px, self.button_size_px), pygame.SRCALPHA)
        self.btn_ff_surface = self.btn_ff_surface.convert_alpha()
        self.btn_ff_surface.fill(WHITE)
        
        self.button_press_reactor = {"pause":0, "play":0, "ff":0}

        try:
            data = self.conn.recv(8192)
            if data:
                while data:
                    try:
                        j_msg, idx = self.decoder.raw_decode(data)
                        #print(j_msg)
                    except ValueError:
                        print("JSON Error")
                        
                    if j_msg:
                        # --- update positions with socket-received data ---
                        update = j_msg["payload"]["data"]

                        for key in update:
                            if (key == "target"):
                                if self.target_cnt > 0:
                                    self.target = guiTarget(update[key]["x"] + self.x_corrector, self.y_corrector - update[key]["y"], update[key]["z"])
                                    self.target.setup()
                                    self.guiObjectsList.insert(0, self.target)
                                     # Make the target always the first element in the guiObjectsList
                                    self.target_cnt -= 1

                            if ("drone" in key):
                                self.drone = guiDrone(update[key]["x"] + self.x_corrector, self.y_corrector - update[key]["y"], update[key]["z"], self.angle_corrector - update[key]["a"], int(key.lstrip("drone")))
                                self.drone.setup()
                                self.guiObjectsList.append(self.drone)

                        for key in update:
                            if ("drone" in key):
                                self.camera_view = guiCameraView(ci = update[key]["center"], si = int(sqrt(update[key]["size"])), view_id = int(key.lstrip("drone")))
                                self.camera_view.setup()
                                self.guiObjectsList.append(self.camera_view)
                                    
                    data = data[idx:].lstrip()
            else:
                pass
        except (KeyboardInterrupt, SystemExit):
            raise

    def recv_update(self):
        while not self.done:
            try:
                data = self.conn.recv(8192)
                if data:
                    while data:
                        #print data, len(data)
                        try:
                            j_msg, idx = self.decoder.raw_decode(data)
                            #print (j_msg)
                        except ValueError:
                            print("JSON Error")

                        if j_msg:
                            # --- update positions with socket-received data ---
                            update = j_msg["payload"]["data"]
                            for obj in self.guiObjectsList:
                                if ((obj.name == "target") or ("drone" in obj.name)):
                                    # --- Remotely generated test data ---
                                    obj.x = self.target_size_px*(update[str(obj.name)]["x"]) + self.x_corrector
                                    obj.y = self.y_corrector - self.target_size_px*(update[str(obj.name)]["y"])
                                    obj.z = update[str(obj.name)]["z"]
                                    obj.a = self.angle_corrector - update[str(obj.name)]["a"]
                                if ("view" in obj.name):
                                    obj.center[0] = int(update["drone"+str(obj.name[-1])]["center"][0]*self.cam_view_scaler)
                                    obj.center[1] = int(update["drone"+str(obj.name[-1])]["center"][1]*self.cam_view_scaler)
                                    obj.size = update["drone"+str(obj.name[-1])]["size"]
                            
                        data = data[idx:].lstrip()
                else:
                    pass
            except (KeyboardInterrupt, SystemExit):
                raise
        
        
    def button(self, text, bx, by, bw, bh, ac, ic, surface):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if bx + bw > mouse[0] > bx and by + bh > mouse[1] > by:
            pygame.draw.rect(surface, ac, (bx, by, self.button_size_px, self.button_size_px))
            if click[0] == 1:
                pygame.draw.rect(surface, (255, 255, 0, 128), (bx, by, self.button_size_px, self.button_size_px))
        else:
            pygame.draw.rect(surface, ic, (bx, by, self.button_size_px, self.button_size_px))

        button_font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        button_label = button_font.render(text, True, (0, 0, 0))
        surface.blit(button_label, (self.button_size_px/2 - button_font.size(text)[0]/2, self.button_size_px/2 - button_font.size(text)[1]/2))
        self.display_surface.blit(surface, (bx, by))
            
    def send(self, data, dst="TestServer"):

        j_msg = dict()
        j_msg["payload"] = data

        j_msg["src"] = "Canvas"
        j_msg["dst"] = ""

        j_packet = json.dumps(j_msg)

        self.conn.sendall(str(j_packet))

    def make_border(self, obj):

        pygame.draw.rect(obj.surface, obj.border_color, [0, 0, obj.sy, obj.border_thickness])
        pygame.draw.rect(obj.surface, obj.border_color, [0, obj.sy - obj.border_thickness, obj.sy, obj.border_thickness])
        pygame.draw.rect(obj.surface, obj.border_color, [0, 0, obj.border_thickness, obj.sy])
        pygame.draw.rect(obj.surface, obj.border_color, [obj.sx - obj.border_thickness, 0, obj.border_thickness, obj.sy])
                    
    def run(self):
        while not self.done:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if ((event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_q))):
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # --- Buttons ---
                    if self.framey - self.button_size_px - self.vmargin < mouse_pos[1] < self.framey - self.vmargin:
                        # Pause button
                        if self.vmargin < mouse_pos[0] < self.vmargin + self.button_size_px:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self.button_press_reactor["pause"] = min(255, self.button_press_reactor["pause"] + 200)
                                sent = self.conn.send("pause")
                                print(sent)

                        # Play button
                        if 2*self.vmargin + self.button_size_px < mouse_pos[0] < 2*self.vmargin + 2*self.button_size_px:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self.button_press_reactor["play"] = min(255, self.button_press_reactor["play"] + 200)
                                sent = self.conn.send("play")
                                print(sent)

                        # Fast-forward button
                        if 3*self.vmargin + 2*self.button_size_px < mouse_pos[0] < 3*self.vmargin + 3*self.button_size_px:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self.button_press_reactor["ff"] = min(255, self.button_press_reactor["ff"] + 200)
                                sent = self.conn.send("ff")
                                print(sent)
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.wx *= self.zoom_sensitivity
                        self.wy *= self.zoom_sensitivity
                    if event.button == 5:
                        self.wx /= self.zoom_sensitivity
                        self.wy /= self.zoom_sensitivity

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]: self.sy += self.pan_sensitivity
            if pressed[pygame.K_s]: self.sy -= self.pan_sensitivity
            if pressed[pygame.K_a]: self.sx += self.pan_sensitivity
            if pressed[pygame.K_d]: self.sx -= self.pan_sensitivity
        
            # if pressed[pygame.K_w]: self.ty += self.pan_sensitivity
            # if pressed[pygame.K_s]: self.ty -= self.pan_sensitivity
            # if pressed[pygame.K_a]: self.tx += self.pan_sensitivity
            # if pressed[pygame.K_d]: self.tx -= self.pan_sensitivity
            
            # --- Fill background ---
            self.display_surface.fill(GREY)
            self.movable_surface.fill((255, 255, 255, 0))
            #self.button_surface.fill(GREEN)
            #self.button_surface.fill((0+self.button_press_reactor, 153, 76, 128))
            self.btn_pause_surface.fill((0+self.button_press_reactor["pause"], 153, 76, 128))
            self.btn_play_surface.fill((0+self.button_press_reactor["play"], 153, 76, 128))
            self.btn_ff_surface.fill((0+self.button_press_reactor["ff"], 153, 76, 128))

            for button in self.button_press_reactor:
                self.button_press_reactor[button] = max(0, self.button_press_reactor[button]-1)



            # --- Position update ----------------------------------------------
            # Call some get_pos() function here by asking the Environment
            # Then, update the guiObjects' positions accordingly

            # RECV_UPDATE() function runs on its own thread now.
            # This is to accept asynchronous inputs from
            # (i) remote server and (ii) local keyboard input for zooming/panning.
            
            for obj in self.guiObjectsList:
                # Fill the surface of target and drone objects
                if ((obj.name == "target") or ("drone" in obj.name)):
                    obj.surface.fill(WHITE)
                # Fill the surface of camera_view objects
                if ("view" in obj.name):
                    obj.surface.fill((255, 255, 255, 128))

            # --- guiObject update ---

            # Re-draw target circle
            pygame.draw.circle(self.target.surface, self.target.color, (int(self.target.sx/2), int(self.target.sy/2)), int(self.target.tr), 0)
            # Re-draw drone objects
            for obj in self.guiObjectsList:
                if "drone" in obj.name:
                    # Re-scale each surface so that each guiObject can fit in it
                    obj.surface = pygame.transform.scale(obj.surface, (int((2*(1+obj.eye_size))*obj.z), int((2*(1+obj.eye_size))*obj.z)))

                    # Re-draw objects according to z-coordinate (their size will vary)
                    pygame.draw.circle(obj.surface, obj.body_color, (int((1+obj.eye_size)*obj.z), int((1+obj.eye_size)*obj.z)), int(obj.z), 0)
                    pygame.draw.circle(obj.surface, obj.eye_color, (int((1+obj.eye_size)*obj.z + obj.z*cos(obj.a*pi/180)), int((1+obj.eye_size)*obj.z - obj.z*sin(obj.a*pi/180))), int(obj.eye_size*obj.z), 0)

            # Re-draw camera_view objects
            for obj in self.guiObjectsList:
                if "view" in obj.name:
                    pygame.draw.circle(obj.surface, RED, obj.center, int(sqrt(obj.size)), 0)
                    self.make_border(obj)

            # Re-draw center mark
            pygame.draw.line(self.movable_surface, GREEN, (self.mx/2 - self.center_mark_size_px, self.my/2), (self.mx/2 + self.center_mark_size_px, self.my/2), self.center_mark_thickness_px)
            pygame.draw.line(self.movable_surface, GREEN, (self.mx/2, self.my/2 - self.center_mark_size_px), (self.mx/2, self.my/2 + self.center_mark_size_px), self.center_mark_thickness_px)

            # --- Canvas update ---
            # Re-drawing is called "blitting"!

            # Blit hierarchy follows this order:
            # [BOTTOM LEVEL] <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< [TOP LEVEL]
            # guiObject.label <<< guiObject.surface <<< movable_surface <<< display_surface

            # guiObject.surface.blit(guiObject.label, [position]) : write label on object's surface
            # movable_surface.blit(guiObject.surface, [position]) : draw object's surface onto movable surface
            # display_surface.blit(movable_surface, [position])   : draw movable surface onto a position-fixed display surface

            # Bottom-level blit
            for guiObject in self.guiObjectsList:
                # Target
                if guiObject.name == "target":
                    guiObject.surface.blit(guiObject.label, (int(guiObject.sx/2 - guiObject.font.size(guiObject.text)[0]/2), int(guiObject.sy/2 - guiObject.font.size(guiObject.text)[1]/2)))

                # Drones
                elif "drone" in guiObject.name:
                    guiObject.surface.blit(guiObject.label, (int((1+guiObject.eye_size)*guiObject.z - guiObject.font.size(guiObject.text)[0]/2), int((1+guiObject.eye_size)*guiObject.z - guiObject.font.size(guiObject.text)[1]/2)))

                # Camera Views
                elif "view" in guiObject.name:
                    guiObject.surface.blit(guiObject.label, (guiObject.border_thickness, guiObject.border_thickness))

            # Mid-level blit
            for obj in self.guiObjectsList:
                # Target and Drones
                if ((obj.name == "target") or ("drone" in obj.name)):
                    self.movable_surface.blit(obj.surface, (int(obj.x - obj.z), int(obj.y - obj.z)))
                if (obj.name == "center"):
                    self.movable_surface.blit(obj.surface, (int(self.framex/2 - obj.sx/2), int(self.framey/2 - obj.sy/2)))
            
            # Top-level blit
            self.display_surface.blit(pygame.transform.scale(self.movable_surface, (int(self.wx), int(self.wy))), (int((self.framex - self.wx)/2 + self.sx), int((self.framey - self.wy)/2 + self.sy)))
            
            # Re-draw buttons
            self.button("PAUSE", self.vmargin, self.framey - self.vmargin - self.button_size_px, self.button_size_px, self.button_size_px, (0, 255, 0, 128), GREEN, self.btn_pause_surface)
            self.button("PLAY", 2*self.vmargin + self.button_size_px, self.framey - self.vmargin - self.button_size_px, self.button_size_px, self.button_size_px, (0, 255, 0, 128), GREEN, self.btn_play_surface)
            self.button("FF", 3*self.vmargin + 2*self.button_size_px, self.framey - self.vmargin - self.button_size_px, self.button_size_px, self.button_size_px, (0, 255, 0, 128), GREEN, self.btn_ff_surface)

            
            for guiObject in self.guiObjectsList:
                # Camera Views
                if "view" in guiObject.name:
                    grid_y = floor(self.framey/(guiObject.sy + self.vmargin))
                    grid_x = int(ceil(self.num_drones/grid_y))
                    #self.display_surface.blit(guiObject.surface, (self.framex - guiObject.sx - self.vmargin, (guiObject.view_id+1)*self.vmargin + guiObject.view_id*guiObject.sy))
                    self.display_surface.blit(guiObject.surface, (int(self.framex - (guiObject.sx + self.vmargin)*(grid_x - floor(guiObject.view_id/grid_y))), int((guiObject.view_id%int(grid_y))*guiObject.sy + ((guiObject.view_id%int(grid_y))+1)*self.vmargin)))


            pygame.display.update()
            
        
if __name__ == "__main__":
    canvas = Canvas(int(resolution[0]), int(resolution[1]), num_drones)
    canvas.setup()
    canvas.run()
        
