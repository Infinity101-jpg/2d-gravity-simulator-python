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
Obj_1_weight = 3                            #### CHAAAAAANGE
Velocity1 = [-5, 7] ## Right, up            #### CHAAAAAANGE
Obj_2_col = RED                             #### CHAAAAAANGE
Obj_2_radius = 30                           #### CHAAAAAANGE
Program_slowdown_percent = 300                #### CHAAAAAANGE
True_velocity1 = [0,0]
### SETTINGS DONE 

Obj_2_coords = [0, 0];
Obj_2_weight = 60
Velocity2 = [0, 0]
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
    global Obj_1_coords, Velocity1, Obj_2_coords, Obj_1_weight, Obj_2_weight
    
    # 1. Calculate the distance between objects for both axes
    dx = Obj_2_coords[0] - Obj_1_coords[0]
    dy = Obj_2_coords[1] - Obj_1_coords[1]
    
    # Distance squared (r^2) - helps prevent division by zero
    dist_sq = dx**2 + dy**2
    if dist_sq < 500: dist_sq = 500 # Safety buffer
    
    # 2. Calculate Force components
    # Using a small multiplier (0.5) to keep speeds manageable
    force_x = (Obj_1_weight * Obj_2_weight * dx) / dist_sq * 0.5
    force_y = (Obj_1_weight * Obj_2_weight * dy) / dist_sq * 0.5
    
    # 3. Update Velocity (Accelerate the planet)
    Velocity1[0] += force_x
    Velocity1[1] += force_y
    
    # 4. Update Coordinates (Move the planet)
    Obj_1_coords[0] += Velocity1[0]
    Obj_1_coords[1] += Velocity1[1]
    

    
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
    Frame_limiter() 
    Update_coords_and_vel()
    Plot_obj_1(Obj_1_coords,Obj_1_col,Obj_1_radius,Obj_1_weight)
    Plot_obj_2(Obj_2_coords,Obj_2_col,Obj_2_radius,Obj_2_weight)
    quit_() 

    
    
    

pygame.quit()