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

from time import sleep
from math import pi, sin, cos
from guiObjects import guiTarget, guiDrone, guiCameraView

# Make Canvas call get_pos() function of the drones
# Use the return values to draw the target and the drones

HOST = "localhost"
PORT = 23456

GREY = (25, 25, 25, 128)
WHITE = (255, 255, 255, 128)
ORANGE = (255, 100, 0, 128)

class Canvas():
    def __init__(self, wx = 2560, wy = 1440, num_drones = 3):
        # Take resolution and number of trackers as argument

        # --- Some PyGame-related initialization ---
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((wx, wy))
        self.movable_surface = self.display_surface.copy()
        self.done = False

        # --- Diplay screen resolution ---
        # Frame is fixed
        self.framex = wx
        self.framey = wy

        # Movable surface is variable
        self.wx = wx
        self.wy = wy
        self.zoom_sensitivity = 1.02 # Change this to zoom faster
        self.pan_sensitivity = 5 # Change this to move screen faster
        self.sx = 0
        self.sy = 0
        
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
        self.vmargin = 15

        # Correctors for intuitive viewing
        self.angle_corrector = 90
        self.x_corrector = self.framex/2
        self.y_corrector = self.framey/2
        
    def setup(self):
        
        # --- Socket setup ---
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((HOST, PORT))
        # self.send({"src": "Canvas"})  # by kdw
        # sleep(1)
        # threading._start_new_thread(self.update_requester, ())

        # --- JSON setup ---
        self.decoder = json.JSONDecoder()

        # --- guiObjects setup ---
        # Randomly positioned for now... get real values later
        self.target = guiTarget(random.randint(0, self.wx), random.randint(0, self.wy), 0, 10)
        self.target.setup()
        self.guiObjectsList.append(self.target)

        for i in range(self.num_drones):
            self.drone = guiDrone(random.randint(0, self.wx), random.randint(0, self.wy), 10, 0, i+1)
            self.drone.setup()
            self.guiObjectsList.append(self.drone)

        for j in range(self.num_drones):
            self.camera_view = guiCameraView(self.vx, self.vy, j+1)
            self.camera_view.setup()
            self.guiObjectsList.append(self.camera_view)
            
    def update_requester(self):
        while not self.done:
            self.send({"topic":"query"})
            sleep(self.update_freq)
            
    def send(self, data, dst="TestServer"):

        j_msg = dict()
        j_msg["payload"] = data

        j_msg["src"] = "Canvas"
        j_msg["dst"] = ""

        j_packet = json.dumps(j_msg)

        self.conn.sendall(str(j_packet))
            
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if ((event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_q))):
                    self.done = True
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

            # --- Fill background ---
            self.display_surface.fill(GREY)
            self.movable_surface.fill(WHITE)

            # --- Position update ----------------------------------------------
            # Call some get_pos() function here by asking the Environment
            # Then, update the guiObjects' positions accordingly

            # TODO: do position update here

            try:
                data = self.conn.recv(1024)
                if data:
                    while data:
                        print data
                        try:
                            j_msg, idx = self.decoder.raw_decode(data)
                            print "!!==!!", j_msg, idx
                        except ValueError:
                            print("JSON Error")

                        if j_msg:
                            #print(j_msg["data"])
                            #print(str(j_msg), type(j_msg))
                            # print str(j_msg["payload"]["data"])
                            print "!!!!", j_msg
                            
                            # --- update positions with socket-received data ---
                            update = j_msg["payload"]["data"]
                            for obj in self.guiObjectsList:
                                if ((obj.name == "target") or ("drone" in obj.name)):
                                    # --- Remotely generated test data ---
                                    obj.x = update[str(obj.name)]["x"] + self.x_corrector
                                    obj.y = self.y_corrector - update[str(obj.name)]["y"]
                                    obj.z = update[str(obj.name)]["z"]
                                    obj.a = self.angle_corrector - update[str(obj.name)]["a"]



                                    # --- Locally generated test data ---
                                    # obj.x = 0 + self.framex/2 # Replace 0 with real-time value
                                    # obj.y = self.framey - 0 - self.framey/2 # Replace 0 with real-time value
                                    # obj.z = 25
                                    # obj.a = 90 - 0 # Replace 0 with real-time value

                                if ("view" in obj.name):
                                    obj.x, obj.y = update["drone"+str(obj.name[-1])]["center"]
                                    obj.size = update["drone"+str(obj.name[-1])]["size"]

                            '''
                            target = self.guiObjectsList[0]
                            target.x = j_msg["payload"]["data"]["target"]["x"]
                            target.y = j_msg["payload"]["data"]["target"]["y"]
                            
                            drone1 = self.guiObjectsList[1]
                            drone1.x = j_msg["payload"]["data"]["drone1"]["x"]
                            drone1.y = j_msg["payload"]["data"]["drone1"]["y"]
                            drone1.z = j_msg["payload"]["data"]["drone1"]["z"]
                            drone1.a = j_msg["payload"]["data"]["drone1"]["a"]
                            '''

                            
                        data = data[idx:].lstrip()
                else:
                    pass
            except (KeyboardInterrupt, SystemExit):
                raise

            # Position update test with random values
            self.target.surface.fill(GREY)

            # Merge the following two for loops later. Fill them all with white background.
            
            # Fill the surface of target and drone objects
            for i in range(self.num_drones):
                self.guiObjectsList[i+1].surface.fill((55, 55, 55, 128))
                # self.guiObjectsList[i+1].x += random.randint(-5, 5)
                # self.guiObjectsList[i+1].y += random.randint(-5, 5)
                # self.guiObjectsList[i+1].z += random.randint(-3, 3)
                # if self.guiObjectsList[i+1].z < 2: self.guiObjectsList[i+1].z = 2
                # self.guiObjectsList[i+1].a += random.randint(-10, 10)
                # self.guiObjectsList[i+1].a = self.guiObjectsList[i+1].a%360
                
            # Fill the surface of camera_view objects
            for j in range(self.num_drones, self.num_drones+self.num_drones):
                self.guiObjectsList[j+1].surface.fill((255, 255, 255))
            # -------------------------------------------------------------------

                
            
            # --- guiObject update ---
            # Re-draw target circle
            pygame.draw.circle(self.target.surface, self.target.color, (int(self.target.sx/2), int(self.target.sy/2)), self.target.tr, 0)
            # Re-draw drone objects
            for i in range(self.num_drones):
                drone = self.guiObjectsList[i+1]

                # Re-scale each surface so that each guiObject can fit in it
                drone.surface = pygame.transform.scale(drone.surface, (int((2*(1+drone.eye_size))*drone.z), int((2*(1+drone.eye_size))*drone.z)))

                # Re-draw objects according to z-coordinate (their size will vary)
                pygame.draw.circle(drone.surface, drone.body_color, (int((1+drone.eye_size)*drone.z), int((1+drone.eye_size)*drone.z)), drone.z, 0)
                pygame.draw.circle(drone.surface, drone.eye_color, (int((1+drone.eye_size)*drone.z + drone.z*cos(drone.a*pi/180)), int((1+drone.eye_size)*drone.z - drone.z*sin(drone.a*pi/180))), int(drone.eye_size*drone.z), 0)

            # Re-draw camera_view objects
            for j in range(self.num_drones, self.num_drones+self.num_drones):
                viewed_obj = self.guiObjectsList[j+1]

                pygame.draw.circle(viewed_obj.surface, ORANGE, (viewed_obj.x, viewed_obj.y), viewed_obj.size, 0)
                
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
                    guiObject.surface.blit(guiObject.label, (0, 0))

            # Mid-level blit
            for guiObject in self.guiObjectsList:
                # Target and Drones
                if not "view" in guiObject.name:
                    self.movable_surface.blit(guiObject.surface, (int(guiObject.x - guiObject.z), int(guiObject.y - guiObject.z)))


            
            # Top-level blit
            for guiObject in self.guiObjectsList:
                # Camera Views
                if "view" in guiObject.name:
                    self.display_surface.blit(guiObject.surface, (self.framex - guiObject.sx - self.vmargin, guiObject.view_id*self.vmargin + (guiObject.view_id+1)*guiObject.sy))
                    
            self.display_surface.blit(pygame.transform.scale(self.movable_surface, (int(self.wx), int(self.wy))), (int((self.framex - self.wx)/2 + self.sx), int((self.framey - self.wy)/2 + self.sy)))

            pygame.display.update()
            
        
if __name__ == "__main__":
    canvas = Canvas(2560, 1440, 3)
    canvas.setup()
    canvas.run()
        
