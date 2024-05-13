import pygame as pg
import math
import time
import noise

pg.init()

WINDOW_SIZE = [750, 500]
screen = pg.display.set_mode(WINDOW_SIZE)

FOV = 70
camera = [0,-1,0]
rot = [0,0]
movd = [True,True]

def update(camera:list, pos:list, angle:list, points:list, movd:list, render: bool, side: list[bool]):
    
    if movd[0] == True or movd[1] == True:
        render = False
        points = [
            [pos[0],pos[1],pos[2]],
            [pos[0]+1,pos[1],pos[2]],
            [pos[0]+1,pos[1]+1,pos[2]],
            [pos[0],pos[1]+1,pos[2]],
            [pos[0],pos[1],pos[2]+1],
            [pos[0]+1,pos[1],pos[2]+1],
            [pos[0]+1,pos[1]+1,pos[2]+1],
            [pos[0],pos[1]+1,pos[2]+1]
            ]
        
        i = 0
        for point in points:
            
            x = point[0] - camera[0]
            y = point[1] - camera[1]
            z = point[2] - camera[2]
            
            x1 = x * math.cos(angle[0]) - z * math.sin(angle[0])
            z1 = x * math.sin(angle[0]) + z * math.cos(angle[0])
            y1 = y * math.cos(angle[1]) - z1 * math.sin(angle[1])
            z2 = y * math.sin(angle[1]) + z1 * math.cos(angle[1])
            
            scale = 600 / ((2 * math.tan(FOV / 2) * z2)+.1)
            
            x = (x1 * scale) + WINDOW_SIZE[0]/2
            y = (y1 * scale) + WINDOW_SIZE[1]/2

            if z2 <= 0:
                render = True

            points[i] = (x,y)
            i += 1
    
    if render == False:
        global pos2
        pos2 = False
        
        if (camera[0] < pos[0] or camera[0] > pos[0]+1):
            if camera[0] >= (pos[0]+1) and side[0] == False:
                e = pg.draw.polygon(screen, (36,27,40), ((points[1]), (points[2]), (points[6]), (points[5])))
                if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
                    pos2 = True
            if camera[0] < (pos[0]) and side[1] == False:
                e = pg.draw.polygon(screen, (43,73,72), ((points[3]), (points[7]), (points[4]), (points[0])))
                if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
                    pos2 = True
            
        if (camera[1] < pos[1] or camera[1] > pos[1]+1):
            if camera[1] >= (pos[1]+.5) and side[2] == False:
                e = pg.draw.polygon(screen, (67,67,67), ((points[7]), (points[6]), (points[2]), (points[3])))
                if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
                    pos2 = True
            if camera[1] < (pos[1]+.5) and side[3] == False:
                e = pg.draw.polygon(screen, (11,11,11), ((points[0]), (points[1]), (points[5]), (points[4])))
                if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
                    pos2 = True
        
        if camera[2] >= pos[2]+1 and side[4] == False:
            e = pg.draw.polygon(screen, (26,158,44), ((points[4]), (points[5]), (points[6]), (points[7])))
            if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
                pos2 = True
        if camera[2] < pos[2] and side[5] == False:
            e = pg.draw.polygon(screen, (255,255,255), ((points[0]), (points[1]), (points[2]), (points[3])))
            if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
                pos2 = True
    return points, render, pos2

def faie(pos: list):
    c2 = 0
    for ii in blocks:
        
        if [ii[1]+1,ii[2],ii[3]] == pos:
            blocks[c2][5][0] = False
        if [ii[1]-1,ii[2],ii[3]] == pos:
            blocks[c2][5][1] = False

        if [ii[1],ii[2],ii[3]+1] == pos:
            blocks[c2][5][4] = False 
        if [ii[1],ii[2],ii[3]-1] == pos:
            blocks[c2][5][5] = False 

        if [ii[1],ii[2]+1,ii[3]] == pos:
            blocks[c2][5][2] = False
        if [ii[1],ii[2]-1,ii[3]] == pos:
            blocks[c2][5][3] = False
        c2 += 1

blocks = []
for x in range(40):
    for y in range(40):
        v = noise.pnoise2(x/10, y/10, octaves=1) * 5 - 3
        v = round(v)
        db = (x+.5-camera[0])*(x+.5-camera[0])+(v+.5-camera[1])*(v+.5-camera[1])+(y+.5-camera[2])*(y+.5-camera[2])
        
        blocks.append([db,x,v,y,[],[False, False, False, False, False, False], False])



c1 = 0
for i in blocks:
    pos = [i[1],i[2],i[3]]
    c2 = 0
    for ii in blocks:
        if [ii[1]+1,ii[2],ii[3]] == pos:
            blocks[c1][5][1] = True
            blocks[c2][5][0] = True

        if [ii[1],ii[2],ii[3]+1] == pos:
            blocks[c1][5][5] = True
            blocks[c2][5][4] = True 

        if [ii[1],ii[2]+1,ii[3]] == pos:
            blocks[c1][5][3] = True
            blocks[c2][5][2] = True
        c2 += 1
    c1 += 1


 
t = time.time()
s = 0
FPS = None
dt=1
q2 = 0
player_speed = 10
run = True
action = []
pg.mouse.set_visible(False)
action.append(0)
while run == True:
    if time.time()-t >= 1:
        t = time.time()
        FPS = s
        s = 0
    s += 1

    dt = time.time()-q2
    q2 = time.time()
    
    for event in pg.event.get():
        if event.type == pg.QUIT: run = False
        
    global keys
    keys = pg.key.get_pressed()
    mouse = pg.mouse

    if keys[pg.K_a]:
        movd[0] = True
        camera[2] += math.sin(rot[0])*dt*player_speed
        camera[0] -= math.cos(rot[0])*dt*player_speed
    if keys[pg.K_d]:
        movd[0] = True
        camera[2] -= math.sin(rot[0])*dt*player_speed
        camera[0] += math.cos(rot[0])*dt*player_speed
    if keys[pg.K_w]:
        movd[0] = True
        camera[2] += math.cos(rot[0])*dt*player_speed
        camera[0] += math.sin(rot[0])*dt*player_speed
    if keys[pg.K_s]:
        movd[0] = True
        camera[2] -= math.cos(rot[0])*dt*player_speed
        camera[0] -= math.sin(rot[0])*dt*player_speed
    if keys[pg.K_LSHIFT]:
        movd[0] = True
        camera[1] += dt*player_speed
    if keys[pg.K_SPACE]:
        movd[0] = True
        camera[1] -= dt*player_speed
    if keys[pg.K_ESCAPE]:
        run = False
    
    rel = pg.mouse.get_rel()
    mouse_pos = pg.mouse.get_pos()
    rot[0] += rel[0]/20*dt
    rot[1] += rel[1]/20*dt
    if rel != (0,0):
        movd[1] = True
    
    mouse.set_pos(WINDOW_SIZE[0]//2,WINDOW_SIZE[1]//2)
    screen.fill((36,121,150))
    
    if movd[0] == True:
        
        for i in blocks:
            pos = i
            db = (pos[1]+.5-camera[0])*(pos[1]+.5-camera[0])+(pos[2]+.5-camera[1])*(pos[2]+.5-camera[1])+(pos[3]+.5-camera[2])*(pos[3]+.5-camera[2])
            i[0] = db  
        blocks.sort(reverse=True)
        action = []

    for i in blocks:
        i[4], i[6], pos = update(camera,[i[1],i[2],i[3]],rot,i[4],movd,i[6],i[5])
        if mouse.get_pressed()[2] and pos == True:
            blocks.remove(i)
            faie([i[1],i[2],i[3]])
    
    pg.draw.circle(screen, (255,255,255), (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), 5)

    movd = [False,False]
    pg.display.set_caption(f"FPS {FPS}  frime:{s}        {rot}       {camera}")
    pg.display.update()
pg.quit()



# week 0

#1: 30x30 26 fps
#1: 50x50 7 fps

# week 1

#1: 30x30 35 fps
#1: 50x50 10.5 fps

# week 2

#1: 30x30 28//42 fps
#1: 50x50 12//19 fps

# week 3

#1: 30x30 40//200 fps
#1: 50x50 20//100 fps
