import pygame as pg
#from pygame import gfxdraw as gfxd
from pygame.locals import QUIT
import random as r
import matplotlib.pyplot as plt
import time

pg.init()
pg.mixer.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_DEPTH = 100
TOTAL_INIT = 0
FPS = 144
NUM_OBJ = 10
FONT = pg.font.SysFont("JetBrains Mono", 20)
SOUNDS = (pg.mixer.Sound("pop1.mp3"),
          pg.mixer.Sound("pop2.mp3"))


class Obj:
    def __init__(self, x, y, radius, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.color = color

    def __str__(self):
        return "Coordinates: " + str((self.x, self.y, self.z)) + " displacement: " + str((self.dx, self.dy, self.dz))


def distance(obj1, obj2):
    return ((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)**0.5


def norm(vector):   
    return (vector[0]**2 + vector[1]**2)**0.5


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = FONT.render(fps, 1, 0)
    return fps_text, fps


def create_objects(NUM_OBJ, default_radius=25, radius_shift=5, speed_width=[-4, 4]):
    objects = []
    for _ in range(NUM_OBJ):

        radius = r.randint(25 - radius_shift, 25 + radius_shift)
        x = r.randint(radius, WINDOW_WIDTH - radius)
        y = r.randint(radius, WINDOW_HEIGHT - radius)

        dx = r.uniform(speed_width[0], speed_width[1])
        dy = r.uniform(speed_width[0], speed_width[1])

        color = [r.randint(0, 255) for _ in range(3)]

        objects.append(Obj(x, y, radius, dx, dy, color))
    return objects


beginning = time.time()                                        # Starting time
clock = pg.time.Clock()                                        # Clock for handling FPS
running = True                                                 # Game boolean
last_sound = time.time()

screen = pg.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])    # Creating window
screen.fill((240, 240, 240))                                   # Filling window w/ backroung color

objects = create_objects(NUM_OBJ, speed_width=[-8, 8], radius_shift=15)         # Creating list of objects
movement = []
fps_hist = []

for obj in objects:                                            # Getting the normal amount of movement
    TOTAL_INIT += abs(obj.dx)
    TOTAL_INIT += abs(obj.dy)


while running:

    for event in pg.event.get():                               # Checking exit button
        if event.type == QUIT:
            running = False
            break

    else:
        total = 0
        for obj in objects:                                    # Moving each object
            obj.x += obj.dx
            obj.y += obj.dy
            total += abs(obj.dx)
            total += abs(obj.dy)

        if total > TOTAL_INIT:                                 # If too much movement, normalizing
            for obj in objects:
                obj.dx /= (total / TOTAL_INIT)
                obj.dy /= (total / TOTAL_INIT)

        # Collisions
        collided = []
        for obj1 in objects:                                   # Checking collisions below
            for obj2 in objects:
                if obj1 is obj2: continue

                dist = distance(obj1, obj2)
                if (dist < (obj1.radius + obj2.radius)):
                   
                    vBA = (obj1.x - obj2.x, obj1.y - obj2.y)   # A is center of obj1 and B is center of obj2

                    vBA_norm = norm(vBA)


                    intersection = (vBA[0]/(vBA_norm/(obj1.radius + obj2.radius - dist)),
                                    vBA[1]/(vBA_norm/(obj1.radius + obj2.radius - dist)))

                    
                    obj1.dx += intersection[0] / (obj1.radius/obj2.radius)  # noqa: E226
                    obj1.dy += intersection[1] / (obj1.radius/obj2.radius)  # noqa: E226

                    if time.time() - last_sound > 0.05:
                        r.choice(SOUNDS).play()
                        last_sound = time.time()

            if (obj1.x > WINDOW_WIDTH - obj1.radius) or (obj1.x < obj1.radius):  # Hit a vertical wall
                obj1.dx = -obj1.dx
            if (obj1.y > WINDOW_HEIGHT - obj1.radius) or (obj1.y < obj1.radius):  # Hit a horizontal wall
                obj1.dy = -obj1.dy


        screen.fill((240, 240, 240))
        for obj in objects:
            pg.draw.circle(screen, obj.color, (obj.x, obj.y), obj.radius)

        fps_surface, actual_fps = update_fps()
        screen.blit(fps_surface, (10, 0))
        pg.display.flip()
        clock.tick(FPS)

        fps_hist.append(actual_fps)
        movement.append(total)


pg.quit()

plt.plot(range(len(movement)), movement)
plt.plot(range(len(fps_hist)), fps_hist)
plt.show()
