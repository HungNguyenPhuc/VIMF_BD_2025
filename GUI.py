import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

class GamepadVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gamepad Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Initialize joystick
        pygame.joystick.init()
        self.joystick = None
        self.joystick_count = pygame.joystick.get_count()
        
        self.init_joystick()
        self.running = True
    
    def init_joystick(self):
        """Initialize the first available joystick"""
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            # Don't call init() on newer pygame versions
        else:
            self.joystick = None
    
    def draw_button(self, x, y, radius, pressed, label):
        """Draw a circular button"""
        color = GREEN if pressed else GRAY
        pygame.draw.circle(self.screen, color, (int(x), int(y)), radius)
        pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), radius, 2)
        
        # Draw label
        text = self.small_font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(x, y + radius + 15))
        self.screen.blit(text, text_rect)
    
    def draw_joystick(self, center_x, center_y, x_axis, y_axis, radius, label):
        """Draw joystick with current position"""
        # Draw outer circle
        pygame.draw.circle(self.screen, DARK_GRAY, (int(center_x), int(center_y)), radius)
        pygame.draw.circle(self.screen, WHITE, (int(center_x), int(center_y)), radius, 2)
        
        # Draw crosshairs
        pygame.draw.line(self.screen, GRAY, 
                        (center_x - radius, center_y), 
                        (center_x + radius, center_y), 1)
        pygame.draw.line(self.screen, GRAY, 
                        (center_x, center_y - radius), 
                        (center_x, center_y + radius), 1)
        
        # Draw joystick position
        stick_x = center_x + (x_axis * (radius - 10))
        stick_y = center_y + (y_axis * (radius - 10))
        pygame.draw.circle(self.screen, RED, (int(stick_x), int(stick_y)), 8)
        
        # Draw label
        text = self.font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(center_x, center_y + radius + 25))
        self.screen.blit(text, text_rect)
        
        # Draw axis values
        axis_text = f"X: {x_axis:.2f}, Y: {y_axis:.2f}"
        axis_surface = self.small_font.render(axis_text, True, WHITE)
        axis_rect = axis_surface.get_rect(center=(center_x, center_y + radius + 45))
        self.screen.blit(axis_surface, axis_rect)
    
    def draw_trigger(self, x, y, width, height, value, label):
        """Draw trigger as a progress bar"""
        # Draw background
        pygame.draw.rect(self.screen, DARK_GRAY, (x, y, width, height))
        pygame.draw.rect(self.screen, WHITE, (x, y, width, height), 2)
        
        # Draw fill based on trigger value
        if value > 0:
            fill_height = int(height * value)
            pygame.draw.rect(self.screen, GREEN, 
                           (x, y + height - fill_height, width, fill_height))
        
        # Draw label
        text = self.small_font.render(label, True, WHITE)
        text_rect = text.get_rect(center=(x + width//2, y + height + 15))
        self.screen.blit(text, text_rect)
        
        # Draw value
        value_text = f"{value:.2f}"
        value_surface = self.small_font.render(value_text, True, WHITE)
        value_rect = value_surface.get_rect(center=(x + width//2, y + height + 30))
        self.screen.blit(value_surface, value_rect)
    
    def draw_dpad(self, center_x, center_y, up, down, left, right):
        """Draw D-pad"""
        size = 20
        gap = 5
        
        # Draw up
        color = GREEN if up else GRAY
        pygame.draw.rect(self.screen, color, 
                        (center_x - size//2, center_y - size - gap, size, size))
        pygame.draw.rect(self.screen, WHITE, 
                        (center_x - size//2, center_y - size - gap, size, size), 2)
        
        # Draw down
        color = GREEN if down else GRAY
        pygame.draw.rect(self.screen, color, 
                        (center_x - size//2, center_y + gap, size, size))
        pygame.draw.rect(self.screen, WHITE, 
                        (center_x - size//2, center_y + gap, size, size), 2)
        
        # Draw left
        color = GREEN if left else GRAY
        pygame.draw.rect(self.screen, color, 
                        (center_x - size - gap, center_y - size//2, size, size))
        pygame.draw.rect(self.screen, WHITE, 
                        (center_x - size - gap, center_y - size//2, size, size), 2)
        
        # Draw right
        color = GREEN if right else GRAY
        pygame.draw.rect(self.screen, color, 
                        (center_x + gap, center_y - size//2, size, size))
        pygame.draw.rect(self.screen, WHITE, 
                        (center_x + gap, center_y - size//2, size, size), 2)
        
        # Draw center
        pygame.draw.rect(self.screen, DARK_GRAY, 
                        (center_x - size//2, center_y - size//2, size, size))
        pygame.draw.rect(self.screen, WHITE, 
                        (center_x - size//2, center_y - size//2, size, size), 2)
        
        # Label
        text = self.small_font.render("D-PAD", True, WHITE)
        text_rect = text.get_rect(center=(center_x, center_y + 50))
        self.screen.blit(text, text_rect)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Clear screen
            self.screen.fill(BLACK)
            
            # Check for joystick connection changes (less aggressive approach)
            joystick_count = pygame.joystick.get_count()
            
            if joystick_count != self.joystick_count:
                self.joystick_count = joystick_count
                self.init_joystick()
            
            # Draw title
            title = self.font.render("Gamepad Visualizer", True, WHITE)
            self.screen.blit(title, (10, 10))
            
            if self.joystick is None:
                # No gamepad connected
                no_gamepad_text = self.font.render("No gamepad connected", True, RED)
                text_rect = no_gamepad_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                self.screen.blit(no_gamepad_text, text_rect)
                
                instruction_text = self.small_font.render("Connect a gamepad and it will appear here", True, GRAY)
                instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
                self.screen.blit(instruction_text, instruction_rect)
            else:
                # Display gamepad info
                gamepad_name = self.joystick.get_name()
                name_text = self.small_font.render(f"Controller: {gamepad_name}", True, WHITE)
                self.screen.blit(name_text, (10, 40))
                
                # Get joystick values safely
                num_axes = self.joystick.get_numaxes()
                num_buttons = self.joystick.get_numbuttons()
                num_hats = self.joystick.get_numhats()
                
                # Debug: Print axis mapping (remove this line after testing)
                # if num_axes > 0:
                #     print(f"Axes: {[round(self.joystick.get_axis(i), 3) for i in range(min(num_axes, 6))]}")
                
                try:
                    # Xbox controller mapping:
                    # Axis 0: Left stick X, Axis 1: Left stick Y
                    # Axis 2: Left trigger, Axis 3: Right stick X
                    # Axis 4: Right stick Y, Axis 5: Right trigger
                    
                    left_x = self.joystick.get_axis(0) if num_axes > 0 else 0
                    left_y = self.joystick.get_axis(1) if num_axes > 1 else 0
                    self.draw_joystick(150, 200, left_x, left_y, 50, "Left Stick")
                    
                    # Right stick mapping - fix the axis assignment
                    right_x = self.joystick.get_axis(3) if num_axes > 3 else 0  # Changed from axis 2 to 3
                    right_y = self.joystick.get_axis(4) if num_axes > 4 else 0  # Changed from axis 3 to 4
                    self.draw_joystick(350, 200, right_x, right_y, 50, "Right Stick")
                    
                    # Triggers - correct mapping
                    left_trigger = 0
                    right_trigger = 0
                    if num_axes > 2:
                        left_trigger = max(0, (self.joystick.get_axis(2) + 1) / 2)  # Axis 2 is left trigger
                    if num_axes > 5:
                        right_trigger = max(0, (self.joystick.get_axis(5) + 1) / 2)  # Axis 5 is right trigger
                    
                    self.draw_trigger(100, 100, 30, 80, left_trigger, "LT")
                    self.draw_trigger(450, 100, 30, 80, right_trigger, "RT")
                    
                    # Face buttons - Xbox layout: A=0, B=1, X=2, Y=3
                    # Rearrange to match physical layout
                    face_buttons = [
                        (0, "A", (650, 250)),  # Bottom
                        (1, "B", (680, 220)),  # Right  
                        (2, "X", (620, 220)),  # Left
                        (3, "Y", (650, 190))   # Top
                    ]
                    
                    for btn_id, label, pos in face_buttons:
                        pressed = self.joystick.get_button(btn_id) if btn_id < num_buttons else False
                        self.draw_button(pos[0], pos[1], 15, pressed, label)
                    
                    # Shoulder buttons - proper positioning
                    lb_pressed = self.joystick.get_button(4) if num_buttons > 4 else False
                    rb_pressed = self.joystick.get_button(5) if num_buttons > 5 else False
                    self.draw_button(150, 100, 15, lb_pressed, "LB")
                    self.draw_button(350, 100, 15, rb_pressed, "RB")
                    
                    # D-pad - move to left side to match controller layout
                    if num_hats > 0:
                        hat = self.joystick.get_hat(0)
                        up = hat[1] > 0
                        down = hat[1] < 0
                        left = hat[0] < 0
                        right = hat[0] > 0
                        self.draw_dpad(80, 250, up, down, left, right)
                    
                    # System buttons - center positioned
                    select_pressed = self.joystick.get_button(6) if num_buttons > 6 else False  # Back/Select
                    start_pressed = self.joystick.get_button(7) if num_buttons > 7 else False   # Start/Menu
                    home_pressed = self.joystick.get_button(8) if num_buttons > 8 else False    # Xbox/Home
                    
                    self.draw_button(300, 120, 10, select_pressed, "Back")
                    self.draw_button(400, 120, 10, start_pressed, "Start") 
                    self.draw_button(350, 150, 8, home_pressed, "Home")
                    
                    # Stick buttons (L3, R3) - positioned on the sticks
                    l3_pressed = self.joystick.get_button(9) if num_buttons > 9 else False
                    r3_pressed = self.joystick.get_button(10) if num_buttons > 10 else False
                    self.draw_button(150, 280, 8, l3_pressed, "L3")
                    self.draw_button(350, 280, 8, r3_pressed, "R3")
                    
                except pygame.error as e:
                    # Handle joystick disconnection gracefully
                    error_text = self.font.render(f"Joystick error: {str(e)}", True, RED)
                    text_rect = error_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                    self.screen.blit(error_text, text_rect)
                    self.joystick = None
            
            # Instructions
            instructions = [
                "ESC - Exit",
                "Connect/disconnect gamepads as needed"
            ]
            
            for i, instruction in enumerate(instructions):
                text = self.small_font.render(instruction, True, GRAY)
                self.screen.blit(text, (10, WINDOW_HEIGHT - 40 + i * 20))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    visualizer = GamepadVisualizer()
    visualizer.run()