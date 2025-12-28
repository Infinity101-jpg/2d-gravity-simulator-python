import pygame
import sys
import sim_settings
# Setup
pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()

# Colors
# --- 20 COLOR LIBRARY ---
# Basics
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
GRAY    = (128, 128, 128)
SILVER  = (192, 192, 192)

# Primaries & Vitals
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)

# Neons & Brights
CYAN    = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME    = (50, 205, 50)
ORANGE  = (255, 165, 0)

# Deep & Space Colors
PURPLE    = (128, 0, 128)
NAVY      = (0, 0, 128)
MAROON    = (128, 0, 0)
TEAL      = (0, 128, 128)

# Celestial / Unique
GOLD      = (255, 215, 0)
PINK      = (255, 192, 203)
SKY_BLUE  = (135, 206, 235)
VIOLET    = (238, 130, 238)

# Create a library for easy lookup
color_library = {
    "WHITE": WHITE, "BLACK": BLACK, "GRAY": GRAY, "SILVER": SILVER,
    "RED": RED, "GREEN": GREEN, "BLUE": BLUE, "YELLOW": YELLOW,
    "CYAN": CYAN, "MAGENTA": MAGENTA, "LIME": LIME, "ORANGE": ORANGE,
    "PURPLE": PURPLE, "NAVY": NAVY, "MAROON": MAROON, "TEAL": TEAL,
    "GOLD": GOLD, "PINK": PINK, "SKY_BLUE": SKY_BLUE, "VIOLET": VIOLET
}

# Assign colors using .get(key, default_value)
Obj_1_col = color_library.get(sim_settings.Obj_1_col, WHITE)
Obj_2_col = color_library.get(sim_settings.Obj_2_col, WHITE)
    

### SETTINGS ###########################################################
Game_slowdown_percent = sim_settings.Game_slowdown_percent    # 0 to 100

# OBJECT 1 (Blue Planet)

Obj_1_radius = sim_settings.Obj_1_radius
Obj_1_weight = sim_settings.Obj_1_weight          
Obj_1_coords = sim_settings.Obj_1_coords
Velocity1 = sim_settings.Velocity1    ## regs, op 

# OBJECT 2 (Red Star)

Obj_2_radius = sim_settings.Obj_2_radius
Obj_2_weight = sim_settings.Obj_2_weight         
Obj_2_coords = sim_settings.Obj_2_coords    
Velocity2 = sim_settings.Velocity2     
########################################################################

Force_Scale = 0.0000001  # Scaling factor to keep objects on screen
FORCE_MODIFIER = 1000 ;

def quit_():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def Plot(x, y, color):
    try:
        # Convert to screen space (Center is 600, 300)
        px, py = int(x + 600), int(300 - y)
        if 0 <= px < 1200 and 0 <= py < 600:
            screen.set_at((px, py), color)
    except:
        pass

def Plot_Circle(mdpt_x, mdpt_y, Color, Radius):
    x, y = 0, int(Radius)
    d = 3 - 2 * Radius 
    while y >= x:
        for sx, sy in [(x,y), (-x,y), (x,-y), (-x,-y), (y,x), (-y,x), (y,-x), (-y,-x)]:
            Plot(mdpt_x + sx, mdpt_y + sy, Color)
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        x += 1

def Fill_Circle(mdpt_x, mdpt_y, Color, Radius):
    for r in range(int(Radius), -1, -1):
        Plot_Circle(mdpt_x, mdpt_y, Color, r)
        Plot_Circle(10000000, 10000000, BLACK, Game_slowdown_percent*10)


def Update_coords_and_vel():
    global Obj_1_coords, Velocity1, Obj_2_coords, Velocity2, Obj_1_weight, Obj_2_weight, FORCE_MODIFIER
    
    # 1. Get distance and direction
    dx = Obj_2_coords[0] - Obj_1_coords[0]
    dy = Obj_2_coords[1] - Obj_1_coords[1]
    dist = (dx**2 + dy**2)**0.5
    
    # 2. Prevent division by zero
    if dist < 1: dist = 1
    
    # 3. YOUR LOGIC (Applied to force magnitude)
    # Force = 1000 * (W1*W2 / dist^2) + Vel * (W1*W2 / dist^3)
    # We use 'dist' instead of dx/dy inside the formula to keep it stable
    force_mag = FORCE_MODIFIER * (Obj_1_weight * Obj_2_weight / dist**2)
    velocity_pull = (Velocity1[0]**2 + Velocity1[1]**2)**0.5 * (Obj_1_weight * Obj_2_weight / dist**3)
    
    total_force = (force_mag + velocity_pull) * Force_Scale

    # 4. Directional components (So they pull TOWARD each other)
    # This is the "Small Change" needed to make the logic work
    force_x = total_force * (dx / dist**1.000)
    force_y = total_force * (dy / dist**1.000)

    # 5. Update Velocities (Acceleration = Force / Mass)
    Velocity1[0] += force_x / (Obj_1_weight * 0.1)
    Velocity1[1] += force_y / (Obj_1_weight * 0.1)
    
    Velocity2[0] -= force_x / (Obj_2_weight * 0.1)
    Velocity2[1] -= force_y / (Obj_2_weight * 0.1)

    # 6. Apply Movement
    Obj_1_coords[0] += Velocity1[0]
    Obj_1_coords[1] += Velocity1[1]
    
    Obj_2_coords[0] += Velocity2[0]
    Obj_2_coords[1] += Velocity2[1]

    # 7. Damping (Friction) from your snippet
    Velocity1[0] *= 1.000
    Velocity1[1] *= 1.000
    Velocity2[0] *= 1.000
    Velocity2[1] *= 1.000

# Main Loop
screen.fill(BLACK) 
while True:
    # 1. Erase
    Fill_Circle(Obj_1_coords[0], Obj_1_coords[1], BLACK, Obj_1_radius+10)
    Fill_Circle(Obj_2_coords[0], Obj_2_coords[1], BLACK, Obj_2_radius+10)
    
    # 2. Logic
    Update_coords_and_vel()
    
    # 3. Draw
    Fill_Circle(Obj_1_coords[0], Obj_1_coords[1], Obj_1_col, Obj_1_radius)
    Fill_Circle(Obj_2_coords[0], Obj_2_coords[1], Obj_2_col, Obj_2_radius)
    draw_pos1 = (int(Obj_1_coords[0] + 600), int(300 - Obj_1_coords[1]))
    draw_pos2 = (int(Obj_2_coords[0] + 600), int(300 - Obj_2_coords[1]))
    pygame.draw.circle(screen, Obj_1_col, draw_pos1, Obj_1_radius+1)
    pygame.draw.circle(screen, Obj_2_col, draw_pos2, Obj_2_radius+1)

    if FORCE_MODIFIER < 1: 
        FORCE_MODIFIER = FORCE_MODIFIER * 0.002;
    if FORCE_MODIFIER > 1: 
        FORCE_MODIFIER = 1000;
        
    current_fps = int(clock.get_fps())
    pygame.display.set_caption("2D Oribital Gravity Simulation | FPS: " + str(current_fps))
    
    pygame.display.flip() 
    quit_() 
    clock.tick(120 - Game_slowdown_percent)
