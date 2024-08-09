import pygame as pg
import math
import time
import noise

pg.init()

t = time.time()
wordl_size = (8, 8, 5)
FOV = 70
camera = [0,0,-20]
c_angle = [0,0,0]
screen = pg.display.set_mode((750, 500), pg.RESIZABLE)

def Getdb(x,y,z,camera):
    return (x-camera[0])*(x-camera[0])+(y-camera[1])*(y-camera[1])+(z-camera[2])*(z-camera[2])


class voxel(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.db = 0
        self.size = 1
        self.render = True
        self.screen = screen
        self.camera = camera
        self.angle = c_angle

        self.points_3d = [
            [self.x,           self.y,           self.z          ],
            [self.x+self.size, self.y,           self.z          ],
            [self.x+self.size, self.y+self.size, self.z          ],
            [self.x,           self.y+self.size, self.z          ],
            [self.x,           self.y,           self.z+self.size],
            [self.x+self.size, self.y,           self.z+self.size],
            [self.x+self.size, self.y+self.size, self.z+self.size],
            [self.x,           self.y+self.size, self.z+self.size]
            ]
        
        self.points_2d = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
        
        self.side = [False, False, False, False, False, False]
        self.vertx = [False for i in range(8)]
    
    def init(self):
        if self.side[0] == False:
            self.vertx[1], self.vertx[2], self.vertx[6], self.vertx[5] = True, True, True, True

        if self.side[1] == False:
            self.vertx[3], self.vertx[7], self.vertx[4], self.vertx[0] = True, True, True, True

        if self.side[2] == False:
            self.vertx[7], self.vertx[6], self.vertx[2], self.vertx[3] = True, True, True, True

        if self.side[3] == False:
            self.vertx[0], self.vertx[1], self.vertx[5], self.vertx[4] = True, True, True, True

        if self.side[4] == False:
            self.vertx[4], self.vertx[5], self.vertx[6], self.vertx[7] = True, True, True, True

        if self.side[5] == False:
            self.vertx[0], self.vertx[1], self.vertx[2], self.vertx[3] = True, True, True, True
        
    def vertex(x_, y_, z_, camera, angle):
        x = x_ - camera[0]
        y = y_ - camera[1]
        z = z_ - camera[2]
        render = True
        
        x1 = x * math.cos(angle[0]) - z  * math.sin(angle[0])
        z1 = x * math.sin(angle[0]) + z  * math.cos(angle[0])
        y1 = y * math.cos(angle[1]) - z1 * math.sin(angle[1])
        z2 = y * math.sin(angle[1]) + z1 * math.cos(angle[1])
        x2 = x1 * math.cos(angle[2]) - y1 * math.sin(angle[2])
        y2 = x1 * math.sin(angle[2]) + y1 * math.cos(angle[2])
        
        scale = 600 / (2 * math.tan(FOV) * z2+0.01)
    
        x = (x2 * scale) + WINDOW_SIZE[0]//2
        y = (y2 * scale) + WINDOW_SIZE[1]//2

        if z2 <= 0:
            render = False
        
        return (x, y), render
    
    def if_render(self, camera, angle):
        x = self.x - camera[0] + 0.5
        y = self.y - camera[1] + 0.5
        z = self.z - camera[2] + 0.5
        
        z1 = x * math.sin(angle[0]) + z  * math.cos(angle[0])
        z2 = y * math.sin(angle[1]) + z1 * math.cos(angle[1])

        if z2 > 0:
            self.render = True
        return self.render
    
    def update2(self, camera, angle):
            if (voxels.if_render(camera, angle)):
                self.db = Getdb(self.x+self.size/2, self.y+self.size/2, self.z+self.size/2, camera)
                i = 0
                for vertx in self.vertx:
                    if vertx == True and self.render == True:
                        self.points_2d[i], self.render = voxel.vertex(self.points_3d[i][0],
                                                                      self.points_3d[i][1],
                                                                      self.points_3d[i][2], camera, angle)
                    if self.render == False:
                        break
                    i += 1
            
        
            
    def draw(self, camera):
        if self.render:
            if camera[0] >= self.x+1 and self.side[0] == False:
                pg.draw.polygon(self.screen, (36,27,40), ((self.points_2d[1]), (self.points_2d[2]), (self.points_2d[6]), (self.points_2d[5])))
            elif camera[0] < self.x and self.side[1] == False:
                pg.draw.polygon(self.screen, (43,73,72), ((self.points_2d[3]), (self.points_2d[7]), (self.points_2d[4]), (self.points_2d[0])))

            if camera[1] > self.y+1 and self.side[2] == False:
                pg.draw.polygon(self.screen, (67,67,67), ((self.points_2d[7]), (self.points_2d[6]), (self.points_2d[2]), (self.points_2d[3])))
            elif camera[1] < self.y and self.side[3] == False:
                pg.draw.polygon(self.screen, (11,11,11), ((self.points_2d[0]), (self.points_2d[1]), (self.points_2d[5]), (self.points_2d[4])))

            if camera[2] >= self.z+1 and self.side[4] == False:
                pg.draw.polygon(self.screen, (26,158,44), ((self.points_2d[4]), (self.points_2d[5]), (self.points_2d[6]), (self.points_2d[7])))
            elif camera[2] < self.z and self.side[5] == False:
                pg.draw.polygon(self.screen, (255,255,255), ((self.points_2d[0]), (self.points_2d[1]), (self.points_2d[2]), (self.points_2d[3])))
        
    def Getpos(self):
        return (self.x, self.y, self.z)


class chunk(object):
    def __init__(self,x ,y, z):
        self.x = x
        self.y = y
        self.z = z


voxel_list = []
for x in range(-wordl_size[0], wordl_size[0]):
    for z in range(-wordl_size[1], wordl_size[1]):

        y = round(noise.pnoise2(x/30, z/30) * wordl_size[2])
        for i in range(y, wordl_size[2]):
            voxels = voxel(x, i, z)
            voxel_list.append(voxels)

for i in voxel_list:
    ipos = i.Getpos()

    for j in voxel_list:
        jpos = j.Getpos()

        if ipos == (jpos[0]-1, jpos[1], jpos[2]):
            i.side[0] = True
        elif ipos == (jpos[0]+1, jpos[1], jpos[2]):
            i.side[1] = True
        elif ipos == (jpos[0], jpos[1]+1, jpos[2]):
            i.side[3] = True
        elif ipos == (jpos[0], jpos[1]-1, jpos[2]):
            i.side[2] = True
        elif ipos == (jpos[0], jpos[1], jpos[2]-1):
            i.side[4] = True
        elif ipos == (jpos[0], jpos[1], jpos[2]+1):
            i.side[5] = True

    i.init()
dt = 0
q2 = 0
player_speed = 15
use_mouse = True
mouse = pg.mouse
run = True
t = time.time()
cn = 0
print(round((time.time()-t)*100)/100)

while run == True:
    WINDOW_SIZE = pg.display.get_window_size()
    dt = time.time()-q2
    q2 = time.time()
    
    if [event for event in pg.event.get() if event.type == pg.QUIT]:
        break
        
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        camera[2] += math.sin(c_angle[0])*dt*player_speed
        camera[0] -= math.cos(c_angle[0])*dt*player_speed
    if keys[pg.K_d]:
        camera[2] -= math.sin(c_angle[0])*dt*player_speed
        camera[0] += math.cos(c_angle[0])*dt*player_speed
    if keys[pg.K_w]:
        camera[2] += math.cos(c_angle[0])*dt*player_speed
        camera[0] += math.sin(c_angle[0])*dt*player_speed
    if keys[pg.K_s]:
        camera[2] -= math.cos(c_angle[0])*dt*player_speed
        camera[0] -= math.sin(c_angle[0])*dt*player_speed
    if keys[pg.K_RIGHT]:
        c_angle[2] -= 0.02
    if keys[pg.K_LEFT]:
        c_angle[2] += 0.02
    if keys[pg.K_LSHIFT]:
        camera[1] += dt*player_speed
    if keys[pg.K_SPACE]:
        camera[1] -= dt*player_speed
    if keys[pg.K_ESCAPE]:
        run = False
    if keys[pg.K_q]:
        if use_mouse == True:
            use_mouse = False
            pg.mouse.set_visible(True)
        else:
            use_mouse = True
        mouse.set_pos(WINDOW_SIZE[0]//2,WINDOW_SIZE[1]//2)
    
    if use_mouse == True:
        pg.mouse.set_visible(False)
        rel = pg.mouse.get_rel()
        c_angle[0] += rel[0]/200
        c_angle[1] += rel[1]/200
        mouse.set_pos(WINDOW_SIZE[0]//2,WINDOW_SIZE[1]//2)
    
    screen.fill((36,121,150))

    voxel_list = sorted(voxel_list, key=lambda voxel: voxel.db, reverse=True)

    for voxels in voxel_list:

        if voxels.side != [True for i in range(6)]:
            voxels.update2(camera, c_angle)
            voxels.draw(camera)
                
    pg.draw.circle(screen, (255,255,255), (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), 5, 2)

    if time.time() - t >= 0.25:   
        pg.display.set_caption(f"FPS: {round(cn/(time.time() - t))}   ms {(time.time() - t ) / cn}")
        cn = 0
        t = time.time()
    cn += 1
    pg.display.flip()
pg.quit()
# 16 x 16 = 1.41 sec to run
# 32 x 32 = 26.39 sec to run
# 32 x 64 = 100.26 sec to run
# 64 x 64 = N/A
