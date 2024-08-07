import pygame as pg
import math
import time
import noise

pg.init()

WINDOW_SIZE = [750, 500]
screen = pg.display.set_mode(WINDOW_SIZE)

wordl_size = (32,32)
FOV = 70
camera = [0,-1,0]
rot = [0,0]
movd = [True,True]
global v
v = 0

def update(camera:list, pos:list, angle:list, render: bool, size = 1):
    
    render[0] = True
    
    points = [
        [pos[0],pos[1],pos[2]],
        [pos[0]+size,pos[1],pos[2]],
        [pos[0]+size,pos[1]+size,pos[2]],
        [pos[0],pos[1]+size,pos[2]],
        [pos[0],pos[1],pos[2]+size],
        [pos[0]+size,pos[1],pos[2]+size],
        [pos[0]+size,pos[1]+size,pos[2]+size],
        [pos[0],pos[1]+size,pos[2]+size]]
    
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
            render[0] = False

        points[i] = (x,y)
        i += 1
            
    e = 0
    for i in points:
        if not (0 < i[0] or i[0] < WINDOW_SIZE[0]) or not (0 < i[1] or i[0] < WINDOW_SIZE[1]):
            e += 1
        
    if e == 8:
        render[0] = False
    return points, render

def draw_and_collide(pos, camera:list, points:list, side:list):
    pos2 = [False,0,0,0]
    if camera[0] >= pos[0]+1 and side[0] == False:
        e = pg.draw.polygon(screen, (36,27,40), ((points[1]), (points[2]), (points[6]), (points[5])))
        if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
            pos2[0],pos2[1] = True,1
    elif camera[0] < pos[0] and side[1] == False:
        e = pg.draw.polygon(screen, (43,73,72), ((points[3]), (points[7]), (points[4]), (points[0])))
        if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
            pos2[0],pos2[1] = True,-1
        
    if camera[1] > pos[1]+1 and side[2] == False:
        e = pg.draw.polygon(screen, (67,67,67), ((points[7]), (points[6]), (points[2]), (points[3])))
        if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
            pos2[0],pos2[2] = True,1
    elif camera[1] < pos[1] and side[3] == False:
        e = pg.draw.polygon(screen, (11,11,11), ((points[0]), (points[1]), (points[5]), (points[4])))
        if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
           pos2[0],pos2[2] = True,-1
    
    if camera[2] >= pos[2]+1 and side[4] == False:
        e = pg.draw.polygon(screen, (26,158,44), ((points[4]), (points[5]), (points[6]), (points[7])))
        if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
            pos2[0],pos2[3] = True,1
    elif camera[2] < pos[2] and side[5] == False:
        e = pg.draw.polygon(screen, (255,255,255), ((points[0]), (points[1]), (points[2]), (points[3])))
        if e.collidepoint(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2):
            pos2[0],pos2[3] = True,-1
    return pos2

def draw(pos, camera:list, points:list, side:list):
         if camera[0] >= pos[0]+1 and side[0] == False:
             pg.draw.polygon(screen, (36,27,40), ((points[1]), (points[2]), (points[6]), (points[5])))
         elif camera[0] < pos[0] and side[1] == False:
             pg.draw.polygon(screen, (43,73,72), ((points[3]), (points[7]), (points[4]), (points[0])))

         if camera[1] > pos[1]+1 and side[2] == False:
             pg.draw.polygon(screen, (67,67,67), ((points[7]), (points[6]), (points[2]), (points[3])))
         elif camera[1] < pos[1] and side[3] == False:
             pg.draw.polygon(screen, (11,11,11), ((points[0]), (points[1]), (points[5]), (points[4])))

         if camera[2] >= pos[2]+1 and side[4] == False:
             pg.draw.polygon(screen, (26,158,44), ((points[4]), (points[5]), (points[6]), (points[7])))
         elif camera[2] < pos[2] and side[5] == False:
             pg.draw.polygon(screen, (255,255,255), ((points[0]), (points[1]), (points[2]), (points[3])))


blocks = []
for x in range(wordl_size[0]):
    for y in range(wordl_size[1]):
        v = noise.pnoise2(x/15, y/15) * 5
        v = round(v)
        
        for i in range(v, 5):
        
            db = (x+.5-camera[0])*(x+.5-camera[0])+(v+.5-camera[1])*(v+.5-camera[1])+(y+.5-camera[2])*(y+.5-camera[2])
            blocks.append([db,[x//8,i//8,y//8],x,i,y,[],[False, False, False, False, False, False], [True,True], 0])

chunk = []
for x in range(0,wordl_size[0],8):
    for y in range(0,wordl_size[1],8):
        for z in range(-1, 1):
            chunk.append([[x//8,z//8,y//8],True, 0])
            
for i in blocks:
    iii = 0
    for ii in chunk:
        if ii[0] == i[1]:
            i[8] =  iii
        iii += 1
    
    n = noise.pnoise2(i[2]/15, i[4]/15) * 5
    n = round(n)
    if i[3] == 4:
        i[6][2] = False
    else:
        i[6][2] = True
    if n < i[3]:
        i[6][3] = True
    n = noise.pnoise2(i[2]/15, (i[4]/15)-1/15) * 5
    n = round(n)
    if n <= i[3]:
        i[6][5] = True
    n = noise.pnoise2(i[2]/15, (i[4]/15)+1/15) * 5
    n = round(n)
    if n <= i[3]:
        i[6][4] = True
    n = noise.pnoise2((i[2]/15)-1/15, i[4]/15) * 5
    n = round(n)
    if n <= i[3]:
        i[6][1] = True
    n = noise.pnoise2((i[2]/15)+1/15, i[4]/15) * 5
    n = round(n)
    if n <= i[3]:
        i[6][0] = True
    
timer1 = 0
t = time.time()
s = 0
dt=1
q2 = 0
player_speed = 20
run = True
action = []
pg.mouse.set_visible(False)
action.append(0)
v = 0
while run == True:
    if time.time()-t >= 1:
        t = time.time()
        pg.display.set_caption(f"FPS: {s}      {rot}     {camera}")
        s = 0
    s += 1
    dt = time.time()-q2
    q2 = time.time()
    
    timer1 += dt
    
    if [event for event in pg.event.get() if event.type == pg.QUIT]:
        run = False
        
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
    rot[0] += rel[0]/200
    rot[1] += rel[1]/200
    if rel != (0,0):
        movd[1] = True
    
    mouse.set_pos(WINDOW_SIZE[0]//2,WINDOW_SIZE[1]//2)
    screen.fill((36,121,150))
    
    if action != []:
        for i in action:
            if i == 0:
                rot = [0,0]
            action = []
            
    blocks.sort()
    for i in chunk:
        points, sht = update(camera,[i[0][0]*8,i[0][1]*8,i[0][2]*8],rot,[False for _ in range(6)], 8)
        
        i[1] = False
        for point in points:
            if point[0] > 0 and point[0] < WINDOW_SIZE[0] and point[1] > 0 and point[1] < WINDOW_SIZE[1]:
                    i[1] = True
    for i in blocks[::-1]:
        i[7][1] = chunk[i[8]][1]
        
        if i[7][1] == True:
            i[0] = (i[2]+.5-camera[0])*(i[2]+.5-camera[0])+(i[3]+.5-camera[1])*(i[3]+.5-camera[1])+(i[4]+.5-camera[2])*(i[4]+.5-camera[2])
            if movd != [False,False] and i[6] != [True for i in range(6)]:
                i[5], i[7] = update(camera,[i[2],i[3],i[4]],rot,i[7])
                v += 1
            if i[7][0] == True:
                if i[0] < 200:
                    pos = draw_and_collide([i[2],i[3],i[4]], camera, i[5], i[6])
                else:
                    draw([i[2],i[3],i[4]], camera, i[5], i[6])
                
                if mouse.get_pressed()[2] and pos[0] == True and timer1 > .5:
                    timer1 = 0
                    blocks.remove(i)
                if mouse.get_pressed()[0] and pos[0] == True and timer1 > .5:
                    timer1 = 0
                    blocks.append([0,[0,0,0],i[2]+pos[1],i[3]+pos[2],i[4]+pos[3],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[False,False,False,False,False,False],[False,True]])
                 
    pg.draw.circle(screen, (255,255,255), (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), 5)

    v = 0
    movd = [False,False]
    pg.display.update()
pg.quit()
