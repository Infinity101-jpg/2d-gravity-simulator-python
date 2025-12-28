import pygame

# Setup
pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
### Setup done 

# Colors (R, G, B)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0);
BLUE = (0, 0, 255)
### Colors Done 

### Settings 
Obj_1_coords = [-200, 0]                    #### CHAAAAAANGE
Obj_1_col = BLUE                            #### CHAAAAAANGE
Obj_1_radius = 5                            #### CHAAAAAANGE
Obj_1_weight = .001                            #### CHAAAAAANGE
Velocity1 = [-3, 6] ## Right, up            #### CHAAAAAANGE
Obj_2_col = RED                             #### CHAAAAAANGE
Obj_2_radius = 30                           #### CHAAAAAANGE
Program_slowdown_percent = 100                #### CHAAAAAANGE
True_velocity1 = [0,0]
### SETTINGS DONE 

Obj_2_coords = [0, 0];                      #### CHAAANGE 
Obj_2_weight = 10000                           #### CHAAAANGE
Velocity2 = [0, 0]                          #### CHAAANGE
dt = 0.7  # Smaller = more accurate, Larger = faster
Frame_lim_significance = Program_slowdown_percent
# Closing the game
def quit_():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
### Closing done 



# 2d Renderer Functions 
def Plot(x, y, color):
    screen.set_at((int(x + 600), int(300 - y)), color)
    ## CANVAS SETUP = 4 QUADRANTS, FROM X = -300 TO 300 , AND Y = -300 TO 300 

def Fill_Circle(mdpt_x, mdpt_y, Color, Radius):
    x = 0
    y = Radius
    d = 3 - 2 * Radius

    def draw_line(x1, x2, y_pos):
        # Draws a horizontal line between two x-coordinates at a specific y
        for i in range(int(x1), int(x2) + 1):
            Plot(i, y_pos, Color)

    while y >= x:
        # Draw horizontal lines between the mirrored points to fill the circle
        draw_line(mdpt_x - x, mdpt_x + x, mdpt_y + y)
        draw_line(mdpt_x - x, mdpt_x + x, mdpt_y - y)
        draw_line(mdpt_x - y, mdpt_x + y, mdpt_y + x)
        draw_line(mdpt_x - y, mdpt_x + y, mdpt_y - x)

        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        x += 1
def Frame_limiter():
    Plot_obj_1([10000, 10000],BLACK,Frame_lim_significance,0)
    
def Plot_obj_1(coords, col, radius, weight):
    mdpt_x, mdpt_y = coords;
    Color = col
    Radius = radius;
    Fill_Circle(mdpt_x, mdpt_y, Color, Radius); 
def Plot_obj_2(coords, col, radius, weight):
    mdpt_x, mdpt_y = coords;
    Color = col
    Radius = radius;
    Fill_Circle(mdpt_x, mdpt_y, Color, Radius); 
def Update_coords_and_vel():
    global Obj_1_coords, Velocity1, Obj_2_coords, Velocity2
    
    # 1. Distance and Direction
    dx = Obj_2_coords[0] - Obj_1_coords[0]
    dy = Obj_2_coords[1] - Obj_1_coords[1]
    dist_sq = dx**2 + dy**2
    
    # Prevent overlapping/division by zero
    if dist_sq < 400: dist_sq = 400 
    distance = dist_sq**0.5

    # 2. Calculate Shared Force
    # F = (m1 * m2) / r^2 (simplified G=1)
    force_mag = (Obj_1_weight * Obj_2_weight) / dist_sq
    
    # 3. Acceleration for Object 1 (a = F / m1)
    accel1_x = (force_mag * (dx / distance)) / Obj_1_weight
    accel1_y = (force_mag * (dy / distance)) / Obj_1_weight
    
    # 4. Acceleration for Object 2 (a = F / m2) 
    # Notice the direction is reversed (-dx, -dy)
    accel2_x = (force_mag * (-dx / distance)) / Obj_2_weight
    accel2_y = (force_mag * (-dy / distance)) / Obj_2_weight
    
    # 5. Update Velocities
    Velocity1[0] += accel1_x
    Velocity1[1] += accel1_y
    Velocity2[0] += accel2_x
    Velocity2[1] += accel2_y
    
    # 6. Update Coordinates
    Obj_1_coords[0] += Velocity1[0]
    Obj_1_coords[1] += Velocity1[1]
    Obj_2_coords[0] += Velocity2[0]
    Obj_2_coords[1] += Velocity2[1]
    

    
# Window Setup
screen.fill(BLACK) # Clear screen with black   
for i in range (-300, 300):     ## Temp function for drawing all of the quadrants
    Plot(i, 0, BLACK)
for i in range (-300, 300):     ## Temp function for drawing all of the quadrants
    Plot (0, i, BLACK)

# Gameloop
while True:
    
    pygame.display.flip() # Update the display
    Plot_obj_1(Obj_1_coords,BLACK,Obj_1_radius,Obj_1_weight)
    Plot_obj_2(Obj_2_coords,BLACK,Obj_2_radius,Obj_2_weight)
    Frame_limiter() 
    Update_coords_and_vel()
    Plot_obj_1(Obj_1_coords,Obj_1_col,Obj_1_radius,Obj_1_weight)
    Plot_obj_2(Obj_2_coords,Obj_2_col,Obj_2_radius,Obj_2_weight)
    quit_() 

    
    
    

pygame.quit()