# Simple_simulator Canvas
# Wan Ju Kang
# Nov. 30, 2017

# --------------------------------------------------------------
# Purpose of Simple Simulator is to test learning algorithms
# in a very simple environment, before testing them
# in the more complicated Gazebo environments.
# --------------------------------------------------------------


import pygame
import random
from math import pi, sin, cos
from guiObjects import guiTarget, guiDrone

# Make Canvas call get_pos() function of the drones
# Use the return values to draw the target and the drones

GREY = (25, 25, 25, 0)

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
        self.mouseX = self.wx/2
        self.mouseY = self.wy/2
        self.sx = 0
        self.sy = 0
        
        # List for keeping guiObjects
        self.num_drones = num_drones
        self.guiObjectsList = []

    def setup(self):

        # Randomly positioned for now... get real values later
        self.target = guiTarget(random.randint(0, self.wx), random.randint(0, self.wy), 0, 10)
        self.target.setup()
        self.guiObjectsList.append(self.target)

        for i in range(self.num_drones):
            self.drone = guiDrone(random.randint(0, self.wx), random.randint(0, self.wy), 10, 0, i+1)
            self.drone.setup()
            self.guiObjectsList.append(self.drone)
        
    def run(self):
        while not self.done:
            for event in pygame.event.get():
                if ((event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_q))):
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseX, self.mouseY = pygame.mouse.get_pos()
                    if event.button == 4:
                        self.wx *= self.zoom_sensitivity
                        self.wy *= self.zoom_sensitivity
                    if event.button == 5:
                        self.wx /= self.zoom_sensitivity
                        self.wy /= self.zoom_sensitivity

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]: self.sy -= self.pan_sensitivity
            if pressed[pygame.K_s]: self.sy += self.pan_sensitivity
            if pressed[pygame.K_a]: self.sx -= self.pan_sensitivity
            if pressed[pygame.K_d]: self.sx += self.pan_sensitivity

            # --- Fill background ---
            self.display_surface.fill(GREY)
            self.movable_surface.fill((255, 255, 255, 128))

            # --- Position update ---
            # Call some get_pos() function here by asking the Environment
            # Then, update the guiObjects' positions accordingly

            # TODO: do position update here

            # Test
            self.target.surface.fill((55, 55, 55, 128))
            for i in range(self.num_drones):
                self.guiObjectsList[i+1].surface.fill((55, 55, 55, 128))
                self.guiObjectsList[i+1].x += random.randint(-5, 5)
                self.guiObjectsList[i+1].y += random.randint(-5, 5)
                self.guiObjectsList[i+1].z += random.randint(-3, 3)
                if self.guiObjectsList[i+1].z < 2: self.guiObjectsList[i+1].z = 2
                self.guiObjectsList[i+1].a += random.randint(-10, 10)
                self.guiObjectsList[i+1].a = self.guiObjectsList[i+1].a%360

            
            # --- guiObject update ---
            # Re-draw target circle
            pygame.draw.circle(self.target.surface, self.target.color, (int(self.target.sx/2), int(self.target.sy/2)), self.target.tr, 0)
            # Re-draw other guiObjects
            for i in range(self.num_drones):
                drone = self.guiObjectsList[i+1]

                # Re-scale each surface so that each guiObject can fit in it
                drone.surface = pygame.transform.scale(drone.surface, (int((2*(1+drone.eye_size))*drone.z), int((2*(1+drone.eye_size))*drone.z)))

                # Re-draw objects according to z-coordinate (their size will vary)
                pygame.draw.circle(drone.surface, drone.body_color, (int((1+drone.eye_size)*drone.z), int((1+drone.eye_size)*drone.z)), drone.z, 0)
                pygame.draw.circle(drone.surface, drone.eye_color, (int((1+drone.eye_size)*drone.z + drone.z*cos(drone.a*pi/180)), int((1+drone.eye_size)*drone.z - drone.z*sin(drone.a*pi/180))), int(drone.eye_size*drone.z), 0)
            
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
                if guiObject.text == "T":
                    guiObject.surface.blit(guiObject.label, (int(guiObject.sx/2 - guiObject.font.size(guiObject.text)[0]/2), int(guiObject.sy/2 - guiObject.font.size(guiObject.text)[1]/2)))

                # Drones
                else:
                    guiObject.surface.blit(guiObject.label, (int((1+guiObject.eye_size)*guiObject.z - guiObject.font.size(guiObject.text)[0]/2), int((1+guiObject.eye_size)*guiObject.z - guiObject.font.size(guiObject.text)[1]/2)))

            # Mid-level blit
            for guiObject in self.guiObjectsList:
                self.movable_surface.blit(guiObject.surface, (int(guiObject.x - guiObject.z), int(guiObject.y - guiObject.z)))
            
            # Top-level blit
            self.display_surface.blit(pygame.transform.scale(self.movable_surface, (int(self.wx), int(self.wy))), (int((self.framex - self.wx)/2 + self.sx), int((self.framey - self.wy)/2 + self.sy)))

            pygame.display.update()
            
        
if __name__ == "__main__":
    canvas = Canvas(2560, 1440, 3)
    canvas.setup()
    canvas.run()
        
'''
pygame.init()

# --- Display ---
# wx, wy: dispay width, height
wx = 1280*3
wy = 720*3

# --- Target ---
# tx, ty: initial position of Target
# tr: radius of Target
#tx = 640
#ty = 360
tx = wx/2
ty = wy/2
tr = 20




# --- Drones ---
# num_drones: number of trackers
num_drones = 3
drones_attitude = []

# Randomly initialize drone positions
# This will be updated later anyway
for i in range(num_drones):
    drones_attitude.append([random.randint(0, wx), random.randint(0, wy), 10, 0])

print(drones_attitude)
    
# --- Drone1 ---
# d1x, d1y: Initial position of Drone1 square. Updated by drone's x, y coordinates
# d1e: Initial edge length of Drone1 square. Updated by drone's altitude
d1x = 30
d1y = 30
d1e = 60

d2x = 30
d2y = 30
d2e = 60

d3x = 30
d3y = 30
d3e = 60




clock = pygame.time.Clock()
original_screen = pygame.display.set_mode((wx, wy))
screen = original_screen.copy()
done = False
is_blue = True

fs = 20 # font size
font = pygame.font.SysFont(pygame.font.get_default_font(), fs)
target_text = "T"
target_label = font.render(target_text, True, (0, 0, 0))

drone1_text = "D1"
drone1_label = font.render(drone1_text, True, (0, 0, 0))
#print(font.size("D1"))
#print(font.size("D1")[0], font.size("D1")[1])
#print(pygame.font.get_fonts())

rsx = 100
rsy = 100
rect_surface = pygame.Surface((rsx, rsy), pygame.SRCALPHA)
rect_surface = rect_surface.convert_alpha()
mouseX = wx/2
mouseY = wy/2

sx = 0
sy = 0

scale = 1.0
dr = 20
angle = 90
switch = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if event.button == 4: # wheel up
                wx *= 1.02
                wy *= 1.02
            if event.button == 5: # wheel down
                wx /= 1.02
                wy /= 1.02
    # --- Whiten screen ---
    screen.fill((255, 255, 255)) # Use this for actual deployment
    original_screen.fill((25, 25, 25))
    #screen.fill((0, 0, 0))  # Use this for debugging purposes
    rect_surface.fill((255, 255, 255, 0)) # (r,g,b, alpha) alpha=0 means transparent


    # --- Position update ---
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: d1y -= 3
    if pressed[pygame.K_DOWN]: d1y += 3
    if pressed[pygame.K_LEFT]: d1x -= 3
    if pressed[pygame.K_RIGHT]: d1x += 3

    if pressed[pygame.K_p]:
        wx *= 1.02
        wy *= 1.02
        mouseX, mouseY = pygame.mouse.get_pos()
    if pressed[pygame.K_n]:
        wx /= 1.02
        wy /= 1.02
        mouseX, mouseY = pygame.mouse.get_pos()

    if pressed[pygame.K_k]:
        dr += 1
        rsx *= 1.02
        rsy *= 1.02
    if pressed[pygame.K_j]:
        dr -= 1
        rsx /= 1.02
        rsy /= 1.02

    if pressed[pygame.K_w]: sy -= 1
    if pressed[pygame.K_s]: sy += 1
    if pressed[pygame.K_a]: sx -= 1
    if pressed[pygame.K_d]: sx += 1

    if pressed[pygame.K_h]: angle += 1
    if pressed[pygame.K_l]: angle -= 1
        
    cnt = 0
    separator = 100
    for drone in drones_attitude:
        drone[0] = d1x + cnt*separator
        drone[1] = d1y + cnt*separator
        cnt += 1
    
    # --- Boundary safety ---
    # if dr > 100: dr = 100
    # if dr < 5: dr = 5
    # if d1x < 0: d1x = 0
    # if d1y < 0: d1y = 0
    # if d1x + d1e > 1280: d1x = 1280 - d1e
    # if d1y + d1e > 720: d1y = 720 - d1e
    # if rsx < 10: rsx = 10
    # if rsy < 10: rsy = 10
    # if wx > 1600: wx = 1600
    # if wy > 900: wy = 900
    # if wx < 320: wx = 320
    # if wy < 180: wy = 180
    angle = angle%360
    
    # --- The step ---
    if is_blue: color = (0, 128, 255, 128)
    else: color = (255, 100, 0, 128)

    pygame.draw.circle(screen, (255, 128, 0), (tx, ty), tr, 0)



    # --- Test ---


    # d1x += random.randint(-2, 2)
    # d1y += random.randint(-2, 2)
    # angle += random.randint(-1, 1)
    # angle = angle%360

    # ----------------

    
    rad = angle*pi/180
    
    rect1 = pygame.draw.circle(rect_surface, color, (int(rsx/2), int(rsy/2)), dr, 0)

    eye1 = pygame.draw.circle(rect_surface, (0, 0, 0), (int(rsx/2 + dr*cos(rad)), int(rsy/2 - dr*sin(rad))), int(0.4*dr), 0)
    

    rect_surface = pygame.transform.scale(rect_surface, (int(rsx), int(rsy)))




    

    rect_surface.blit(drone1_label, (rsx/2 - font.size(drone1_text)[0]/2 , rsy/2))    

    screen.blit(rect_surface, (d1x, d1y))

    screen.blit(target_label, (tx - font.size(target_text)[0]/2, ty - font.size(target_text)[1]/2))
    #screen.blit(drone1_label, (drones_attitude[0][0] + d1e/2 - font.size(drone1_text)[0]/2, drones_attitude[0][1] + d1e/2 - font.size(drone1_text)[1]/2))


    
    #pygame.draw.polygon(screen, color, ((drones_attitude[0][0], drones_attitude[0][1]), (drones_attitude[0][0] + d1e, drones_attitude[0][1]), (drones_attitude[0][0] + d1e/2, drones_attitude[0][1] - d1e/2)), 0)
    
    #pygame.draw.rect(screen, color, pygame.Rect(drones_attitude[1][0], drones_attitude[1][1], d1e, d1e))
    #pygame.draw.rect(screen, color, pygame.Rect(drones_attitude[2][0], drones_attitude[2][1], d1e, d1e))
    #pygame.draw.rect(screen, color, rect1.inflate(100, 100))

    screen.scroll(sx, sy)
    original_screen.blit(pygame.transform.scale(screen, (int(wx), int(wy))), (int(mouseX - wx/2), int(mouseY - wy/2)))

    # --- Screen update ---    
    pygame.display.update()
    
    #clock.tick(60)



'''
