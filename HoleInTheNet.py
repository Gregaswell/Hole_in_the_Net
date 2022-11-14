from tkinter import *
from tkinter import messagebox
from os import chdir,getcwd
from math import sin,cos,radians,sqrt
from random import choice,uniform

def time_starts():
    #starts counting down the time
    global t,time_unit,quit_happened
    if t>=0:
        minute,second=divmod(t,60)
        if second>9:
            time_line.config(text='0'+str(minute)+':'+str(second))
        else:
            time_line.config(text='0'+str(minute)+':0'+str(second))
        t=t-1
        if quit_happened==False:
            game_page.after(time_unit,time_starts)

def velocity_settings():
    #sets the moving velocity of the gnats for each level
    global multiplier,gnat_radius,max_moving,moving_scale
    if gnat_radius>8:
        multiplier=multiplier-0.25
        if multiplier==1.25:
            multiplier=2.0
            gnat_radius=gnat_radius-1
    else:
        multiplier=multiplier-0.25
        if multiplier==1.25:
            multiplier=2.0
        if max_moving<0:
            max_moving=max_moving*2
        elif max_moving>0:
            max_moving=max_moving*2
        if abs(max_moving)>32*abs(moving_scale):
            max_moving=moving_scale
            gnat_radius=gnat_radius-1

def next_level():
    #turns off the sensors and cleans the board at the end of the actual level
    #redefines a part of the global variables
    #opens the congratulations-window after last level ends
    global max_t,gnat_radius,time_unit,net_touched,moving_scale,\
           clicking,drugged_band,player_score,life_points
    game_board.tag_unbind('pitch','<Leave>')
    game_board.unbind('<Button-1>')
    game_board.tag_unbind('bad_boy','<Enter>')
    game_board.tag_unbind('gnat','<Button-1>')
    game_board.delete('bad_boy')
    game_board.delete('gnat')
    if max_t>30:
        max_t=int(max_t-1.5)
    velocity_settings()
    time_unit=1000
    net_touched=False
    moving_scale=int(gnat_radius)
    clicking=0
    drugged_band=[]
    if gnat_radius==1:
        player_score=player_score*life_points
        score_line.config(text='Score: '+str(player_score))
        messagebox.showinfo(title='YOU GOT RID OF GNATS',\
                            message='Congratulations! \n'+\
                            'Your score is multiplied by your lives!')
        decision()
    else:
        next_level_window()

def next_level_window():
    #opens a window to decide wheter going on or ending the play
    global player_score,star_rising
    star_rising=Toplevel(window,bg='SkyBlue1', bd=5,\
                    relief=RAISED)
    star_rising.title('Prevail over the dirty lot')
    star_rising.geometry('270x100')
    Label(star_rising,text='Your score is: '+str(player_score),\
          fg='brown',bg='SkyBlue1',font=('Times','16'))\
          .grid(columnspan=2,row=0)
    Label(star_rising,text='You can pass to the '+str(level)+'. level',\
          fg='brown',bg='SkyBlue1',font=('Times','16'))\
          .grid(columnspan=2,row=1)
    Button(star_rising,text='Calm down ',fg='black',bg='red',\
           command=decision).grid(row=2,column=0)
    Button(star_rising,text='NEXT LEVEL',fg='khaki2',bg='black',\
           command=new_level_starts).grid(row=2,column=1)

def new_level_starts():
    #closes the end-level-window and makes appearing start_button
    global star_rising,player_score
    star_rising.destroy()
    start_button.grid(row=1,column=2)
    score_line.config(text='Score: '+str(player_score))
    
def game_starts():
    #launches the game-starting algorithms
    #draws as much gnats as the actual level needs (more and more)
    global trunk_coords,lwing_coords,rwing_coords,max_t,gnat_radius,dimension,\
           t,level,gnat_trunk,left_wing,right_wing,player_score,x_gnat,y_gnat
    start_button.grid_remove()
    t=max_t
    time_starts()
    i=0
    while i<level:
        i=i+1
        new_drugged()
    if level>46:
        while i>0:
            i=i-1
            new_drugged()
    if level>50:
        while i<level:
            i=i+1
            new_drugged()
    level=level+1
    x_gnat=round(uniform(dimension,w-dimension),1)
    y_gnat=round(uniform(dimension,h-dimension),1)
    trunk_coords=[[x_gnat-gnat_radius,y_gnat-gnat_radius],\
                    [x_gnat+gnat_radius,y_gnat+gnat_radius]]
    lwing_coords=[[x_gnat,y_gnat],\
                    [x_gnat-5*gnat_radius,y_gnat-4*gnat_radius],\
                    [x_gnat-3*gnat_radius,y_gnat-gnat_radius]]
    rwing_coords=[[x_gnat,y_gnat],\
                    [x_gnat+5*gnat_radius,y_gnat-4*gnat_radius],\
                    [x_gnat+3*gnat_radius,y_gnat-gnat_radius]]
    gnat_trunk=game_board.create_oval(trunk_coords,outline='saddle brown',\
                         width=3,tags='gnat',fill='saddle brown')
    left_wing=game_board.create_polygon(lwing_coords,\
                              tags='gnat',fill='grey45',\
                                  outline='grey45')
    right_wing=game_board.create_polygon(rwing_coords,\
                              tags='gnat',fill='grey45',\
                                  outline='grey45')
    game_board.tag_bind('pitch','<Leave>',touching_the_net)
    game_board.bind('<Button-1>',target_missed)
    game_board.tag_bind('bad_boy','<Enter>',drugged_one_thouched)
    game_board.tag_bind('gnat','<Button-1>',catching)
    new_target()
    flying()
    flapping()
    drugged_ones_move()

def touching_the_net(event):
    #touching the net the countdown timer gets faster as well as score-decreasing
    global time_unit,net_touched,life_points,player_score,\
           t,max_t
    if t<0.95*max_t:
        player_score=player_score-t
        net_touched=True
        time_unit=int(time_unit/2)
    score_line.config(text='Score: '+str(player_score))
    if net_touched==True:
        score_reduction()

def score_reduction():
    #starts decreasing the score if the pointer touches the net
    global time_unit,player_score,t,level,quit_happened
    player_score=player_score-100
    score_line.config(text='Score: '+str(player_score))
    if t>0 and quit_happened==False:
        game_page.after(time_unit,score_reduction)
    
def target_missed(event):
    #makes a lot of drugged gnats according to the actual level
    global level,x_clicking,y_clicking
    i=0
    x_clicking,y_clicking=event.x,event.y
    if level<20:
        while i<int(0.5*level):
            new_drugged()
            i=i+1
    elif 19<level<26:
        while i<int(0.25*level):
            new_drugged()
            i=i+1
    elif level>25:
        new_drugged()

def drugged_one_thouched(event):
    #touching a drugged gnat with the pointer, life points decrease
    #marking the gnat as well
    global life_points,t
    game_board.itemconfig(CURRENT,fill='red')
    life_points=life_points-1
    life_line.config(text='Lives: '+str(life_points))
    if life_points==0:
        game_board.tag_unbind('bad_boy','<Enter>')
        t=-1

def catching(event):
    #catching the gnat the player gets a lot of points
    global t,player_score,clicking
    player_score=player_score+clicking*t+150
    score_line.config(text='Score: '+str(player_score))
    t=-2
    
########################################## F L Y I N G
def flying():
    #makes the gnat flying and controls the playing events
    global x_gnat,y_gnat,gnat_radius,f,x_coord,y_coord,quit_happened,\
           inclination,moving_scale,life_points,t,player_score,max_t,clicking,multiplier
    if player_score<-15000:
        #insufficient score the go on, game ends
        quit_happened=True
        stop_sensors()
    elif life_points>0 and t>-1:
        #game is happening
        if (inclination==True and abs(x_gnat-x_coord)<=abs(moving_scale))\
           or (inclination==False and abs(y_gnat-y_coord)<=abs(moving_scale)):
                new_target()
        else:
            move_the_gnat()
        life_line.config(text='Lives: '+str(life_points))
        score_line.config(text='Score: '+str(player_score))
        game_board.scale('gnat',(x_gnat),(y_gnat),1,1)
        if quit_happened==False:
            window.after(int(gnat_radius**multiplier),flying)
    elif life_points>0 and t==-1:
        #time is over and the gnat has not been cought, next level starts
        if clicking>0 and net_touched==False:
            player_score=player_score+max_t
        next_level()
    elif life_points>0 and t==-2:
        #player has slapped the gnat
        if net_touched==False:
            player_score=player_score+max_t
        next_level()
    elif life_points==0:
        #life points have been lost, game is over
        quit_happened=True
        game_board.tag_unbind('pitch','<Leave>')
        game_board.unbind('<Button-1>')
        game_board.tag_unbind('bad_boy','<Enter>')
        game_board.tag_unbind('gnat','<Button-1>')
        game_board.delete('bad_boy')
        game_board.delete('gnat')
        decision()                
        
def move_the_gnat():
    global x_gnat,y_gnat,inclination,moving_scale,f
    #is generating the function result for moving the gnat
    #choices the right function according to the inclination of the path
    if inclination==True:
        x_gnat=round(x_gnat+moving_scale,1)
        y_gnat=round(f(x_gnat),1)
    else:
        y_gnat=round(y_gnat+moving_scale,1)
        x_gnat=round(f(y_gnat),1)
    
def f_straight(x):
    global a_straight,b_straight
    #returns the function result from the equation of a line
    #f(x)=a*x+b
    return round(a_straight*x+b_straight,1)

def f_arc(x):
    global Cx,Cy,r_square,inclination,moving_scale,which_side,f
    #returns the function result from the equation of a circle
    #f(x)=v(+/-)sqrt(r**2-(x-u)**2)
    try:
        if inclination==True:
              if moving_scale<0:
                  if which_side=='right':
                      #if x decreases, y must decrease too at first
                      return round(Cy-sqrt(r_square-(x-Cx)**2),1)
                  else:
                      #if x decreases, y must increase at first
                      return round(Cy+sqrt(r_square-(x-Cx)**2),1)
              else:
                  if which_side=='left':
                      #if x increases, y must decrease at first
                      return round(Cy-sqrt(r_square-(x-Cx)**2),1)
                  else:
                      #if x increases, y must increase too at first
                      return round(Cy+sqrt(r_square-(x-Cx)**2),1)
        elif inclination==False:
            if moving_scale<0:
                if which_side=='left':
                    #if y decreases, x must decrease too at first
                      return round(Cx-sqrt(r_square-(x-Cy)**2),1)
                else:
                    #if y decreases, x must increase at first
                      return round(Cx+sqrt(r_square-(x-Cy)**2),1)
            else:
                if which_side=='right':
                    #if y increases, x must decrease at first
                      return round(Cx-sqrt(r_square-(x-Cy)**2),1)
                else:
                    #if y increases, x must increases too at first
                      return round(Cx+sqrt(r_square-(x-Cy)**2),1)
    except ValueError:
        #in case of sqrt(negative value) error
        will_be_straight()
        f=f_straight
        return round(f(x),1)
    
########################################## F L A P P I N G
def flapping():
    #makes moving the wings; x1_l,y1_l,x1_r,y1_r:original coordinates
    #x_c,y_c:center vertex coordinates which we turn the other vertices around of
    #rotation angle: wing_angle;
    #new_x=x_c+(x*cos(angle)-y*sin(angle))
    #new_y=y_c+(x*sin(angle)+y*cos(angle))
    global wing_angle,trunk_coords,lwing_coords,rwing_coords,\
           x_gnat,y_gnat,gnat_radius,inclination,gnat_trunk,left_wing,right_wing,\
           life_points,t,quit_happened
    if life_points>0 and t>-1:
        i=1
        x_c,y_c=x_gnat,y_gnat
        if inclination==True:
            left_angle=radians(wing_angle)
            right_angle=radians(-wing_angle)
        elif inclination==False:
            left_angle=radians(-wing_angle)
            right_angle=radians(wing_angle)
        lsin,lcos=sin(left_angle),cos(left_angle)
        rsin,rcos=sin(right_angle),cos(right_angle)
        lwing_coords[0][0]=x_gnat
        lwing_coords[0][1]=y_gnat
        rwing_coords[0][0]=x_gnat
        rwing_coords[0][1]=y_gnat
        while i<3:
            x1_l,y1_l=lwing_coords[i][0],lwing_coords[i][1]
            x1_r,y1_r=rwing_coords[i][0],rwing_coords[i][1]
            x_l,y_l,x_r,y_r=x1_l-x_c,y1_l-y_c,x1_r-x_c,y1_r-y_c
            lwing_coords[i][0]=x_c+(x_l*lcos)-(y_l*lsin)
            lwing_coords[i][1]=y_c+(x_l*lsin)+(y_l*lcos)
            rwing_coords[i][0]=x_c+(x_r*rcos)-(y_r*rsin)
            rwing_coords[i][1]=y_c+(x_r*rsin)+(y_r*rcos)
            i=i+1
        game_board.coords(gnat_trunk,x_gnat-gnat_radius,y_gnat-gnat_radius,\
                x_gnat+gnat_radius,y_gnat+gnat_radius)
        game_board.coords(left_wing,lwing_coords[0][0],\
                      lwing_coords[0][1],\
                      lwing_coords[1][0],\
                      lwing_coords[1][1],\
                      lwing_coords[2][0],\
                      lwing_coords[2][1])
        game_board.coords(right_wing,rwing_coords[0][0],\
                      rwing_coords[0][1],\
                      rwing_coords[1][0],\
                      rwing_coords[1][1],\
                      rwing_coords[2][0],\
                      rwing_coords[2][1])
        if quit_happened==False:
            window.after(int(gnat_radius*1.5),flapping)


######################################## N E W   T A R G E T
def new_target():
    global x_coord,y_coord,gnat_radius,w,h,x_gnat,y_gnat,\
           moving_scale,f
    #generates a new target for the gnat
    gnat_redraw()
    x_coord=choice([round(uniform(3*abs(moving_scale),\
                                 x_gnat-(2*abs(moving_scale))),1),\
                  round(uniform(x_gnat+2*abs(moving_scale),\
                                w-(3*abs(moving_scale))),1)])
    y_coord=choice([round(uniform(3*abs(moving_scale),\
                                 y_gnat-(2*abs(moving_scale))),1),\
                  round(uniform(y_gnat+2*abs(moving_scale),\
                                h-(6*abs(moving_scale))),1)])
    #afterwards choices a function and makes that preparing
    f=choice([f_straight,f_arc])
    if f==f_straight:
        will_be_straight()
    else:
        will_be_curved()

def gnat_redraw():
    #the difference of several iteration updates' rates causes a phase shift
    #therefore this function redefines the original position of the gnat's vertices
    global trunk_coords,lwing_coords,rwing_coords,\
           x_gnat,y_gnat,gnat_radius
    trunk_coords=[[x_gnat-gnat_radius,y_gnat-gnat_radius],\
                    [x_gnat+gnat_radius,y_gnat+gnat_radius]]
    lwing_coords=[[x_gnat,y_gnat],\
                    [x_gnat-5*gnat_radius,y_gnat-4*gnat_radius],\
                    [x_gnat-3*gnat_radius,y_gnat-gnat_radius]]
    rwing_coords=[[x_gnat,y_gnat],\
                    [x_gnat+5*gnat_radius,y_gnat-4*gnat_radius],\
                    [x_gnat+3*gnat_radius,y_gnat-gnat_radius]]

def will_be_straight():
    #prepares the function from the equation of a line
    global x_coord,y_coord,gnat_radius,w,h,x_gnat,y_gnat,\
           a_straight,b_straight,moving_scale,inclination,f
    normal_vector_A=round(x_gnat-x_coord,1)
    normal_vector_B=round(y_gnat-y_coord,1)
    #defines the inclination of the line to know which coordinate must be increased
    #also defines the direction changing the sing of the moving_scale
    if abs(normal_vector_A)>=abs(normal_vector_B):
        inclination=True
        if x_gnat>x_coord:
            moving_scale=0-abs(moving_scale)
        else:
            moving_scale=abs(moving_scale)
        a_straight=round((y_coord-y_gnat)/(x_coord-x_gnat),1)
        b_straight=round((-x_gnat*(y_coord-y_gnat))/\
             (x_coord-x_gnat)+y_gnat,1)
    else:
        inclination=False
        if y_gnat>y_coord:
            moving_scale=0-abs(moving_scale)
        else:
            moving_scale=abs(moving_scale)
        a_straight=round((x_coord-x_gnat)/(y_coord-y_gnat),1)
        b_straight=round((-y_gnat*(x_coord-x_gnat))/\
                   (y_coord-y_gnat)+x_gnat,1)

def will_be_curved():
    global x_coord,y_coord,gnat_radius,w,h,x_gnat,y_gnat,r_square,\
           a_straight,b_straight,moving_scale,inclination,Cx,Cy,which_side
    #prepares the function from the equation of a circle
    #defines the inclination of the beeline
    #then it knows which coordinate will be increased to avoid unexpected jump and velocity
    normal_vector_A=round(x_gnat-x_coord,1)
    normal_vector_B=round(y_gnat-y_coord,1)
    #choices the side of the arc's dilation
    which_side=choice(['right','left'])
    #the basic principle is the figure of a circumscribed triangle
    #center_x,center_y will be the coordinates of the central vertex between the arrival and departure vertices
    center_x=round((x_coord+x_gnat)/2,1)
    center_y=round((y_coord+y_gnat)/2,1)
    #max_distance meaning the maximum dilation can only be the distance between the central vertex and a bounding point
    max_distance=round(sqrt((x_gnat-center_x)**2+\
                        (y_gnat-center_y)**2),1)
    min_distance=round(max_distance/gnat_radius,1)
    #according to the inclination max_distance can become smaller
    #therefore the distance between the line segment and the device-screen's edges must be measured
    if abs(normal_vector_A)>=abs(normal_vector_B):
        inclination=True
        if x_gnat>x_coord:
            moving_scale=0-abs(moving_scale)
            if which_side=='right':
                if center_y<max_distance:
                    max_distance=center_y
            else:
                if max_distance>h-center_y:
                    max_distance=round(h-center_y,1)
        else:
            moving_scale=abs(moving_scale)
            if which_side=='left':
                if center_y<max_distance:
                    max_distance=center_y
            else:
                if max_distance>h-center_y:
                    max_distance=round(h-center_y,1)
    else:
        inclination=False
        if y_gnat>y_coord:
            moving_scale=0-abs(moving_scale)
            if which_side=='left':
                if center_x<max_distance:
                    max_distance=center_x
            else:
                if max_distance>w-center_x:
                    max_distance=round(w-center_x,1)
        else:
            moving_scale=abs(moving_scale)
            if which_side=='right':
                if center_x<max_distance:
                    max_distance=center_x
            else:
                if max_distance>w-center_x:
                    max_distance=round(w-center_x,1)
    #finally the middle_distance gets a value in the above defined range
    middle_distance=round(uniform(min_distance,max_distance),1)
    #the equation of the circle's chord can be determined reversing the method based on distance from a point to a line
    #(y2-y1)x+(x1-x2)y+y1(x2-x1)-x1(y2-y1)=0, l and b relating to line and bisector
    lA=round(y_coord-y_gnat,1)
    lB=round(x_gnat-x_coord,1)
    lC=round(y_gnat*(x_coord-x_gnat)-\
                    x_gnat*(y_coord-y_gnat),1)
    #a perpendicular bisector must go through the segment midpoint: A*x+B*y=A*x0+B*y0,
    #from here the equation of the bisector can be determined: Ax+By-Ax0-By0=0
    bD=round(normal_vector_A,1)
    bE=round(normal_vector_B,1)
    bF=round(-normal_vector_A*center_x-\
                    normal_vector_B*center_y,1)
    bG=round(middle_distance*sqrt((lA**2)+(lB**2)))
    #based on the solving of the equations system the third vertex of the triangle can be defined
    #there will be two solutions from which the proper one can be selected knowing the inclination and direction
    third_vertex_x1=round(((bE)*((lC)+(bG))-(lB)*(bF))/(((bD)*(lB))-((bE)*(lA))),1)
    third_vertex_y1=round(((bD)*((lC)+(bG))-(lA)*(bF))/(((bE)*(lA))-((bD)*(lB))),1)
    third_vertex_x2=round(((bE)*((lC)-(bG))-(bF)*(lB))/(((bD)*(lB))-((bE)*(lA))),1)
    third_vertex_y2=round(((bF)*(lA)+(bD)*((bG)-(lC)))/(((bD)*(lB))-((bE)*(lA))),1)
    if inclination==True:
        if moving_scale<0:
            if which_side=='right':
                #from right to the left on the top
                if third_vertex_y1<third_vertex_y2:
                    third_vertex_y=third_vertex_y1
                    third_vertex_x=third_vertex_x1
                else:
                    third_vertex_y=third_vertex_y2
                    third_vertex_x=third_vertex_x2
            else:
                #from right to the left on the bottom
                if third_vertex_y1>third_vertex_y2:
                    third_vertex_y=third_vertex_y1
                    third_vertex_x=third_vertex_x1
                else:
                    third_vertex_y=third_vertex_y2
                    third_vertex_x=third_vertex_x2
        else:
            if which_side=='right':
                #from left to the right on the bottom
                if third_vertex_y1>third_vertex_y2:
                    third_vertex_y=third_vertex_y1
                    third_vertex_x=third_vertex_x1
                else:
                    third_vertex_y=third_vertex_y2
                    third_vertex_x=third_vertex_x2
            else:
                #from left to the right on the top
                if third_vertex_y1<third_vertex_y2:
                    third_vertex_y=third_vertex_y1
                    third_vertex_x=third_vertex_x1
                else:
                    third_vertex_y=third_vertex_y2
                    third_vertex_x=third_vertex_x2
    elif inclination==False:
        if moving_scale<0:
            if which_side=='left':
                #from bottom to the top on the left
                if third_vertex_x1<third_vertex_x2:
                    third_vertex_y=third_vertex_y1
                    third_vertex_x=third_vertex_x1
                else:
                    third_vertex_y=third_vertex_y2
                    third_vertex_x=third_vertex_x2
            else:
                #from bottom to the top on the right
                if third_vertex_x1>third_vertex_x2:
                    third_vertex_y=third_vertex_y1
                    third_vertex_x=third_vertex_x1
                else:
                    third_vertex_y=third_vertex_y2
                    third_vertex_x=third_vertex_x2
        else:
            if which_side=='left':
                #from top to the bottom on the left
                if third_vertex_x1>third_vertex_x2:
                    third_vertex_y=third_vertex_y1
                    third_vertex_x=third_vertex_x1
                else:
                    third_vertex_y=third_vertex_y2
                    third_vertex_x=third_vertex_x2
            else:
                #from top to the bottom on the right
                if third_vertex_x1<third_vertex_x2:
                    third_vertex_y=third_vertex_y1
                    third_vertex_x=third_vertex_x1
                else:
                    third_vertex_y=third_vertex_y2
                    third_vertex_x=third_vertex_x2
    #having the triangle an other perpendicular bisector most be determined
    center_x=round((x_coord+third_vertex_x)/2,1)
    center_y=round((y_coord+third_vertex_y)/2,1)    
    normal_vector_A=round(third_vertex_x-x_coord,1)
    normal_vector_B=round(third_vertex_y-y_coord,1)
    bA=round(normal_vector_A,1)
    bB=round(normal_vector_B,1)
    bC=round(-normal_vector_A*center_x-\
                    normal_vector_B*center_y,1)
    #the solution of the equation-system defines the intersection of the lines, the center of the circle
    Cy=round((bC*bD-bA*bF)/(bA*bE-bB*bD),1)
    Cx=round((bB*bF-bC*bE)/(bA*bE-bB*bD),1)
    #the square of radius can be determined now
    r_square=round((x_gnat-Cx)**2+(y_gnat-Cy)**2,1)
    
######################################## D R U G G E D
def drugged_ones_move():
    #moves the drugged gnats
    global drugged_band,clicking,gnat_radius,life_points,t,multiplier,level,quit_happened
    if life_points>0 and t>-1:
        drugged_direction()
        i=0
        while i<clicking:
            game_board.move(drugged_band[i][0],drugged_band[i][3],\
                        drugged_band[i][4])
            drugged_band[i][1]+=drugged_band[i][3]
            drugged_band[i][2]+=drugged_band[i][4]
            i=i+1
        if quit_happened==False:    
            if level>28:
                window.after(int(gnat_radius**(multiplier+0.5)),drugged_ones_move)
            else:
                window.after(int(gnat_radius**(multiplier+0.25)),drugged_ones_move)
        
def drugged_direction():
    #perceives when the gnats arrive to an edge of the device-screen
    global w,h,drugged_band,clicking,gnat_radius
    i=0
    while i<clicking:
        if (drugged_band[i][1]-(3*gnat_radius))<0:
            drugged_on_the_left(i)
        elif (drugged_band[i][2]-(3*gnat_radius))<0:
            drugged_on_the_top(i)
        elif (drugged_band[i][1]+(3*gnat_radius))>w:
            drugged_on_the_right(i)
        elif (drugged_band[i][2]+(3*gnat_radius))>h:
            drugged_on_the_bottom(i)
        i=i+1
        
def drugged_on_the_bottom(which_one):
    #changes the direction of the drugged gnats' moving
    global drugged_band,gnat_radius
    drugged_band[which_one][4]=-abs(drugged_band[which_one][4])
    drugged_band[which_one][3]=choice([0,choice([gnat_radius,-gnat_radius])])
def drugged_on_the_top(which_one):
    #changes the direction of the drugged gnats' moving
    global drugged_band,gnat_radius
    drugged_band[which_one][4]=abs(drugged_band[which_one][4])
    drugged_band[which_one][3]=choice([0,choice([gnat_radius,-gnat_radius])])
def drugged_on_the_left(which_one):
    #changes the direction of the drugged gnats' moving
    global drugged_band,gnat_radius
    drugged_band[which_one][3]=abs(drugged_band[which_one][3])
    drugged_band[which_one][4]=choice([0,choice([gnat_radius,-gnat_radius])])
def drugged_on_the_right(which_one):
    #changes the direction of the drugged gnats' moving
    global drugged_band,gnat_radius
    drugged_band[which_one][3]=-abs(drugged_band[which_one][3])
    drugged_band[which_one][4]=choice([0,choice([gnat_radius,-gnat_radius])])
        
def new_drugged():
    #draws a new drugged gnat
    global gnat_radius,drugged_band,clicking,x_clicking,y_clicking,w,h
    clicking=clicking+1
    if x_clicking-3*gnat_radius<gnat_radius:
        x_gnat=round(uniform(x_clicking+3*gnat_radius,w-gnat_radius),1)
    elif x_clicking+3*gnat_radius>w-gnat_radius:
        x_gnat=round(uniform(gnat_radius,x_clicking-3*gnat_radius))
    else:
        x_gnat=choice([round(uniform(gnat_radius,x_clicking-3*gnat_radius),1),\
                     round(uniform(x_clicking+3*gnat_radius,w-gnat_radius),1)])
    if y_clicking-3*gnat_radius<gnat_radius:
        y_gnat=round(uniform(y_clicking+3*gnat_radius,h-gnat_radius),1)
    elif y_clicking+3*gnat_radius>h-gnat_radius*10:
        y_gnat=round(uniform(gnat_radius,y_clicking-3*gnat_radius))
    else:
        y_gnat=choice([round(uniform(gnat_radius,y_clicking-3*gnat_radius),1),\
                     round(uniform(y_clicking+3*gnat_radius,h-gnat_radius*10),1)])
    drugged_x=choice([0,choice([-gnat_radius,+gnat_radius])])
    if drugged_x==0:
        drugged_y=choice([-gnat_radius,+gnat_radius])
    else:
        drugged_y=choice([0,choice([-gnat_radius,+gnat_radius])])
    trunk_coords=[[x_gnat-gnat_radius,y_gnat-gnat_radius],\
            [x_gnat+gnat_radius,y_gnat+gnat_radius]]
    lwing_coords=[[x_gnat,y_gnat],\
                [x_gnat-5*gnat_radius,y_gnat-4*gnat_radius],\
                [x_gnat-3*gnat_radius,y_gnat-gnat_radius]]
    rwing_coords=[[x_gnat,y_gnat],\
                [x_gnat+5*gnat_radius,y_gnat-4*gnat_radius],\
                [x_gnat+3*gnat_radius,y_gnat-gnat_radius]]
    its_name='drugged'+str(clicking-1)
    gnat_trunk=game_board.create_oval(trunk_coords,width=3,tags=its_name,\
                                outline='grey10', fill='grey10')
    left_wing=game_board.create_polygon(lwing_coords,tags=its_name,\
                                     outline='grey10',fill='grey10')
    right_wing=game_board.create_polygon(rwing_coords,tags=its_name,\
                                     outline='grey10',fill='grey10')
    drugged_band.append([its_name,x_gnat,y_gnat,drugged_x,drugged_y])
    game_board.addtag_withtag('bad_boy',its_name)

################################################ B E G I N I N G    
def about():
    #describes the game
    messagebox.showinfo('How to play?',\
                        "   You wake with a start hearing that disturbing buzz round your ears. "
                        "You are trying to fall back asleep but that gnat doesn't let you do that. "
                        "Then you get more and more angry, yes, there's a hole in your bug screen.\n"
                        "   Slap the brownish gnat (of course, clicking on it), only that one. "
                        "Be careful, slapping aside you will attract other gnats' attention.\n"
                        "   Avoid contacting the drugged grey blood-suckers, otherwise they can bite you. "
                        "(Touching the net reduces the time and your points as well.) "
                        "The game may go on even if you can't slap that annoying gnat in time.\n"
                        "   :) Let's get a fine score! Trust me, you will rewarded at the final stage. "
                        "(Yes, there is a final stage!")
def start():
    #starts the game
    global w,h,player_score
    player_score=0
    score_line.config(text='Score: '+str(player_score))
    first_page.grid_remove()
    window.attributes('-fullscreen',True)
    #window.geometry(str(w)+'x'+str(h)+'+0+0')
    #window.attributes('-alpha',0.75)
    game_page.grid()
    
def back_at_start():
    #goes back to the starting page and initialize all global variables
    global quit_window,star_rising,hnotes,hscore,hname,quit_happened,\
           x_clicking,y_clicking,life_points,level,time_unit,text,\
           net_touched,gnat_trunk,left_wing,right_wing,dimension,\
           max_t,t,gnat_radius,multiplier,moving_scale,wing_angle,inclination,max_moving,\
           trunk_coords,lwing_coords,rwing_coords,\
           x_gnat,y_gnat,x_coord,y_coord,clicking,drugged_band,\
           f,a_straight,b_straight,Cx,Cy,r_square,which_side
    quit_window.destroy()
    if quit_happened==True:
        quit_happened=False
        out_button.grid(row=1,column=4,sticky=E)
    if type(star_rising)!=int:
        star_rising.destroy()
    game_page.grid_remove()
    window.attributes('-fullscreen',False)
    window.geometry('500x500')
    chdir(getcwd())
    hnotes=open('hs_holeinthenet.py','r')
    hscore=(hnotes.readline()).strip()
    hname=(hnotes.readline()).strip()
    best_ever.config(text='Highest score: '+hscore+' by '+hname)
    if hscore=='':
        hscore=-1
    else:
        hscore=int(hscore)
    hnotes.close()
    star_rising,text,x_clicking,y_clicking=0,0,0,0
    life_points,level=10,0
    time_unit=1000
    net_touched=False
    gnat_trunk,left_wing,right_wing=0,0,0
    max_t=120
    gnat_radius,multiplier=15,2.0
    max_moving=moving_scale
    moving_scale=gnat_radius
    wing_angle,inclination=30,True
    trunk_coords,lwing_coords,rwing_coords=[[0,0],[0,0]],[[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0]]
    x_coord,y_coord=x_gnat,y_gnat
    clicking,drugged_band=0,[]
    f,a_straight,b_straight=0,0,0
    Cx,Cy,r_square=0,0,0
    which_side=''
    start_button.grid(row=1,column=2)
    time_line.config(text='00:00')
    game_board.delete('bad_boy')
    game_board.delete('gnat')
    first_page.grid()
    
def quit_hscore():
    #after playing asks for the player name who made new high score
    global player_score,quit_window,text,quit_happened
    quit_happened=True
    quit_window=Toplevel(window,bg='SkyBlue1', bd=5,relief=RAISED)
    quit_window.title('Thanks for playing')
    quit_window.geometry('300x100')
    Label(quit_window,text='Your score is: '+str(player_score),fg='brown',\
          bg='SkyBlue1',font=('Times','16')).grid(columnspan=3,row=0)
    Label(quit_window,text='Player name:',fg='brown',\
          bg='SkyBlue1',font=('Times','16')).grid(column=0,row=1)
    text=StringVar()
    Entry(quit_window,fg='brown',bg='white',font=('Times','16'),\
                 textvariable=text).grid(column=1,row=1)
    Button(quit_window,text='Submit',fg='white',bg='red',\
           command=note_down).grid(row=2,column=1)

def note_down():
    #writes down the player datas in a file
    global hnotes,quit_window,player_score,text,first_page
    hnotes=open('hs_holeinthenet.py','w')
    hnotes.write(str(player_score)+'\n')
    hnotes.write(text.get()+'\n')
    hnotes.close()
    back_at_start()

def quit_no_hscore():
    #quits without data-saving
    global quit_window,player_score,quit_happened
    quit_happened=True
    quit_window=Toplevel(window,bg='SkyBlue1', bd=5,relief=RAISED)
    quit_window.title('Thanks for playing')
    Label(quit_window,text='Your score is: '+str(player_score),fg='brown',\
          bg='SkyBlue1',font=('Times','16')).grid(column=0,row=0)
    Button(quit_window,text='Bye-bye',fg='black',bg='red',\
           command=back_at_start,font=('Times','14','bold'))\
           .grid(row=0,column=1)
    if player_score<0:
        Label(quit_window,text='(Do not touch the net, you may split it further)',\
              fg='brown',bg='SkyBlue1',font=('Times','12'))\
              .grid(columnspan=2,row=1)

def decision():
    #decides wether there is a new high score or not
    global player_score,hscore,star_rising
    if type(star_rising)!=int:
        star_rising.destroy()
    out_button.grid_remove()
    if player_score>hscore:
        quit_hscore()
    else:
        quit_no_hscore()

def stop_sensors():
    #turns off the sensors
    global net_touched,t,player_score
    if net_touched==True:
        player_score=player_score+t+1
        net_touched=False
    t=-3
    game_board.tag_unbind('pitch','<Leave>')
    game_board.unbind('<Button-1>')
    game_board.tag_unbind('bad_boy','<Enter>')
    game_board.tag_unbind('gnat','<Button-1>')
    game_board.delete('bad_boy')
    game_board.delete('gnat')
    decision()

def stop_sensors_2():
    #turns off the sensors
    global quit_happened
    quit_happened=True
    game_board.tag_unbind('pitch','<Leave>')
    game_board.unbind('<Button-1>')
    game_board.tag_unbind('bad_boy','<Enter>')
    game_board.tag_unbind('gnat','<Button-1>')
    game_board.delete('bad_boy')
    game_board.delete('gnat')
    decision()
    
##################################################### M A I N

#reading data from file
chdir(getcwd())
try:
    hnotes=open('hs_holeinthenet.py','r')
except FileNotFoundError:
    hnotes=open('hs_holeinthenet.py','a')
    hnotes.close()
    hnotes=open('hs_holeinthenet.py','r')
hscore=(hnotes.readline()).strip()
hname=(hnotes.readline()).strip()
if hscore=='':
    hscore=-1
else:
    hscore=int(hscore)
hnotes.close()
player_score=0
    
#main window
window=Tk()
window.title('Hole in the Net')
window.iconbitmap('fat_gnat.ico')
window.geometry('500x500')
w=window.winfo_screenwidth()
h=window.winfo_screenheight()

#variables initializing
quit_window=0
star_rising=0
text=0
x_clicking,y_clicking=0,0

#first_page
first_page=Frame(window,width=500,height=500,\
               bg='sienna4')
first_page.grid()
first_page.grid_propagate(0)

#image on the top
picture=Canvas(first_page,width=500,height=180,\
           bg='dodger blue',\
           highlightthickness=0,\
           cursor='hand2')
picture.pack(side=TOP)
    
picture.create_polygon(0,0,500,0,400,155,100,155,\
                   fill='deep sky blue')

#drawing bug-screen on the first page image
to_end=0
while to_end<1000:
    to_end=to_end+10
    picture.create_line(to_end,0,0,to_end,width=1,\
                          fill='white')
to_end=0
while to_end<180:
    to_end=to_end+10
    picture.create_line(0,to_end,w,to_end,width=1,\
                          fill='white')

#continuing to draw the first page image
picture.create_oval(235,120,265,150,\
                outline='saddle brown', width=5,\
                fill='saddle brown',\
                activefill='red',\
                activeoutline='white',)
picture.create_arc(100,120,235,150,\
               fill='gray45',outline='gray45',\
               start=0, extent=150,\
               activefill='white',\
               activeoutline='white')
picture.create_arc(265,120,400,150,\
               fill='gray45',outline='gray45',\
               start=30, extent=150,\
               activefill='white',\
               activeoutline='white')

#title-text
picture.create_text(130,50,\
                activefill='medium purple',\
                fill='SlateBlue3',\
                font=('Times','45','bold'),\
                text='HOLE')
picture.create_text(270,100,\
                activefill='medium purple',\
                fill='SlateBlue3',\
                font=('Times','35','bold'),\
                text='IN  THE')
picture.create_text(400,50,\
                activefill='medium purple',\
                fill='SlateBlue3',\
                font=('Times','45','bold'),\
                text='NET')

#buttons and lables
if hscore==-1:
    best_ever=Label(first_page,text='Welcome, dear Player!',\
          fg='khaki2',bg='sienna4',\
          font=('Times','20','bold'))
    best_ever.pack(pady=20)
else:
    best_ever=Label(first_page,text='Highest score: '+str(hscore)+\
          ' by '+hname,fg='khaki2',bg='sienna4',\
          font=('Times','20','bold'))
    best_ever.pack(pady=20)
Button(first_page,text='How to play',\
       bg='RoyalBlue4',fg='khaki2',\
       command=about, activebackground='indigo',\
       font=('Times','16')).pack(pady=20)
Button(first_page,text="Get rid of them",\
       bg='RoyalBlue4',fg='khaki2',\
       command=start, activebackground='indigo',\
       font=('Times','16')).pack(pady=20)
Button(first_page,text='Need some rest',\
       bg='grey20',fg='khaki2',\
       command=window.quit,font=('Times','16'),\
       activebackground='indigo').pack(side=BOTTOM,pady=30)

#gamepage
game_page=Frame(window,width=w,height=h,bg='sienna4')
game_page.grid_propagate(0)

#other variables
life_points=10
time_unit=1000
level=0
net_touched=False
quit_happened=False
gnat_trunk,left_wing,right_wing=0,0,0

#time measure variables
max_t=120
t=max_t

#getting screen dimensions for knowing the proportion of the gameboard lable on the bottom
if h>w:
    dimension=int((w/14)*(h/w))
else:
    dimension=int(h/14)

#buttons and labels    
score_line=Label(game_page,text='Score: '+str(player_score),\
      fg='white',bg='sienna4',font=('Times','18','bold'))
score_line.grid(row=1,column=0,sticky=W)
out_button=Button(game_page,text='Let me bug out!',\
    bg='dark goldenrod',fg='indigo',bd=5,relief=RAISED,\
    command=stop_sensors_2,font=('Times','18','bold'),\
    activebackground='white')
out_button.grid(row=1,column=4,sticky=E)
start_button=Button(game_page,text='START',\
    bg='white',fg='indigo',bd=5,relief=RAISED,\
    command=game_starts,font=('Times','18','bold'),\
    activebackground='firebrick')
time_line=Label(game_page,text='00:00',\
      fg='white',bg='sienna4',\
      font=('Times','18','bold'))
time_line.grid(row=1,column=3)
start_button.grid(row=1,column=2)
life_line=Label(game_page,text='Lives: '+str(life_points),\
      fg='white',bg='sienna4',font=('Times','18','bold'))
life_line.grid(row=1,column=1,sticky=W)

#the bright sky
game_board=Canvas(game_page,width=w,\
                 height=h-dimension,\
               bg='light blue', cursor='hand2')
game_board.grid(row=0,columnspan=5)

#window-sash
game_board.create_rectangle(0,0,w,int(dimension),fill='sienna4',outline='sienna4')
game_board.create_rectangle(0,0,int(dimension),h,fill='sienna4',outline='sienna4')
game_board.create_rectangle(w-int(dimension),0,w,h,fill='sienna4',outline='sienna4')

#bug-screen on the window-sash
to_end=0
while to_end<2*w:
    to_end=to_end+10
    game_board.create_line(to_end,0,0,to_end,width=1,\
                          fill='white')
to_end=0
while to_end<h:
    to_end=to_end+10
    game_board.create_line(0,to_end,w,to_end,width=1,\
                          fill='white')

#the net-hole
game_board.create_oval(dimension,dimension,w-dimension,h-dimension,\
                      outline='white',width=4,\
                      fill='light blue')

#hole on the left top
game_board.create_arc(-dimension,-dimension,3*dimension,3*dimension,\
                     start=0,extent=10,fill='sienna4',outline='white',\
                     width=2,style=PIESLICE)
game_board.create_arc(-dimension,-dimension,3*dimension,3*dimension,\
                     start=305,extent=15,fill='light blue',outline='white',\
                     width=1,style=PIESLICE)
game_board.create_arc(-dimension,-dimension,3*dimension,3*dimension,\
                     start=260,extent=10,fill='sienna4',outline='white',\
                     width=2,style=PIESLICE)

#hole on the top
game_board.create_arc(int(w/2)-dimension,-int(dimension/2),int(w/2)+3*dimension,int(dimension/2),\
                     style=PIESLICE, start=180,extent=180,fill='sienna4',\
                     outline='white',width=4)


#hole on the left bottom
#open air part
game_board.create_polygon(dimension,h-int(1.5*dimension),3*dimension,h-dimension,dimension,h-dimension,\
                         fill='light blue',outline='light blue')
game_board.create_line(3*dimension,h-dimension,dimension,h-dimension,fill='white',width=3)
game_board.create_line(dimension,h-int(1.5*dimension),3*dimension,h-dimension,fill='white',width=3)
#window-sash part
game_board.create_polygon(0,h-3*dimension,dimension,h-2*dimension,dimension,h-dimension,\
                         fill='sienna4',outline='sienna4')
game_board.create_line(0,h-3*dimension,dimension,h-2*dimension,fill='white',width=3)
game_board.create_line(0,h-3*dimension,dimension,h-dimension,fill='white',width=3)
game_board.create_line(dimension,h-2*dimension,dimension,h-int(1.5*dimension),fill='white',width=3)

#hole on the right top
#window-sash part
game_board.create_arc(w-int(1.5*dimension),0,w-int(dimension/2),2*dimension,outline='sienna4',\
                     style=PIESLICE, start=-90,extent=90,fill='sienna4')
game_board.create_arc(w-int(1.5*dimension),0,w-int(dimension/2),2*dimension,outline='white',\
                     style=ARC,start=-90,extent=90,width=4)
#open air part
game_board.create_arc(w-int(1.5*dimension),0,w-int(dimension/2),2*dimension, outline='light blue',\
                     style=PIESLICE,start=180,extent=90,fill='light blue')
game_board.create_arc(w-int(1.5*dimension),0,w-int(dimension/2),2*dimension, outline='white',\
                     style=ARC,start=180,extent=90,width=4)
#the upper part of window-sash
game_board.create_arc(w-int(1.5*dimension),int(dimension/2),w-int(dimension/2),int(1.5*dimension),\
                     outline='sienna4',style=PIESLICE,start=0,extent=180,\
                     fill='sienna4')
game_board.create_arc(w-int(1.5*dimension),int(dimension/2),w-int(dimension/2),int(1.5*dimension),\
                     outline='white',style=ARC,start=0,extent=180,\
                     width=4)

#oval pitch, the hole net
game_board.create_oval(dimension,dimension,w-dimension,h-dimension,\
                      outline='white',width=4,\
                      tags='pitch')

#other variables initialization
#gnat_radius will be the gnats dimension and its moving scale's determinant
gnat_radius=15
multiplier=2.0
moving_scale=gnat_radius
max_moving=moving_scale
wing_angle=30
inclination=True

#Initialization of the points belonging to the gnat
trunk_coords,lwing_coords,rwing_coords=[[0,0],[0,0]],[[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0]]

#generating the gnat's position
x_gnat=round(uniform(dimension,w-dimension),1)
y_gnat=round(uniform(dimension,h-dimension),1)

#new target coordinates initializing
x_coord,y_coord=x_gnat,y_gnat

#other variables
clicking=0
drugged_band=[]

#f is the variable for chosing the actual function
#Cx,Cy the central point of the circle
f,a_straight,b_straight=0,0,0
Cx,Cy,r_square=0,0,0
which_side=''

window.mainloop()
