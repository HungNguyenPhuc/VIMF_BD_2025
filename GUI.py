import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
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
CONTROLLER_GRAY = (240, 240, 240)
CONTROLLER_OUTLINE = (180, 180, 180)

class GamepadVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Xbox Controller Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 32)
        
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
        else:
            self.joystick = None
    
    def draw_controller_body(self):
        """Draw the Xbox controller outline"""
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50
        
        # Main body (rounded rectangle)
        body_rect = pygame.Rect(center_x - 200, center_y - 80, 400, 160)
        pygame.draw.rect(self.screen, CONTROLLER_GRAY, body_rect, border_radius=30)
        pygame.draw.rect(self.screen, CONTROLLER_OUTLINE, body_rect, 3, border_radius=30)
        
        # Controller grips (handles)
        # Left grip
        left_grip = pygame.Rect(center_x - 250, center_y + 40, 80, 120)
        pygame.draw.rect(self.screen, CONTROLLER_GRAY, left_grip, border_radius=40)
        pygame.draw.rect(self.screen, CONTROLLER_OUTLINE, left_grip, 3, border_radius=40)
        
        # Right grip
        right_grip = pygame.Rect(center_x + 170, center_y + 40, 80, 120)
        pygame.draw.rect(self.screen, CONTROLLER_GRAY, right_grip, border_radius=40)
        pygame.draw.rect(self.screen, CONTROLLER_OUTLINE, right_grip, 3, border_radius=40)
        
        return center_x, center_y
    
    def draw_trigger(self, x, y, width, height, value, label):
        """Draw trigger as shoulder button"""
        # Trigger body (rounded rectangle)
        trigger_rect = pygame.Rect(x - width//2, y - height//2, width, height)
        color = GREEN if value > 0.1 else GRAY
        pygame.draw.rect(self.screen, color, trigger_rect, border_radius=8)
        pygame.draw.rect(self.screen, WHITE, trigger_rect, 2, border_radius=8)
        
        # Label above trigger
        text = self.small_font.render(label, True, BLACK)
        text_rect = text.get_rect(center=(x, y - height//2 - 15))
        self.screen.blit(text, text_rect)
        
        # Value below trigger
        value_text = f"{value:.2f}"
        value_surface = self.small_font.render(value_text, True, BLACK)
        value_rect = value_surface.get_rect(center=(x, y + height//2 + 15))
        self.screen.blit(value_surface, value_rect)
    
    def draw_shoulder_button(self, x, y, width, height, pressed, label):
        """Draw shoulder button (LB/RB)"""
        button_rect = pygame.Rect(x - width//2, y - height//2, width, height)
        color = GREEN if pressed else GRAY
        pygame.draw.rect(self.screen, color, button_rect, border_radius=6)
        pygame.draw.rect(self.screen, WHITE, button_rect, 2, border_radius=6)
        
        # Label
        text = self.small_font.render(label, True, WHITE if pressed else BLACK)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)
    
    def draw_joystick(self, center_x, center_y, x_axis, y_axis, radius, label, pressed=False):
        """Draw joystick with Xbox controller style"""
        # Outer ring
        pygame.draw.circle(self.screen, DARK_GRAY, (int(center_x), int(center_y)), radius + 5)
        pygame.draw.circle(self.screen, WHITE, (int(center_x), int(center_y)), radius + 5, 2)
        
        # Inner area
        pygame.draw.circle(self.screen, WHITE, (int(center_x), int(center_y)), radius)
        pygame.draw.circle(self.screen, GRAY, (int(center_x), int(center_y)), radius, 1)
        
        # Crosshairs
        pygame.draw.line(self.screen, LIGHT_GRAY, 
                        (center_x - radius, center_y), 
                        (center_x + radius, center_y), 1)
        pygame.draw.line(self.screen, LIGHT_GRAY, 
                        (center_x, center_y - radius), 
                        (center_x, center_y + radius), 1)
        
        # Joystick position
        stick_x = center_x + (x_axis * (radius - 8))
        stick_y = center_y + (y_axis * (radius - 8))
        
        # Stick color changes when pressed
        stick_color = RED if pressed else BLACK
        pygame.draw.circle(self.screen, stick_color, (int(stick_x), int(stick_y)), 10)
        pygame.draw.circle(self.screen, WHITE, (int(stick_x), int(stick_y)), 10, 2)
        
        # Label below joystick
        text = self.small_font.render(label, True, BLACK)
        text_rect = text.get_rect(center=(center_x, center_y + radius + 25))
        self.screen.blit(text, text_rect)
    
    def draw_dpad(self, center_x, center_y, up, down, left, right):
        """Draw D-pad with Xbox style"""
        size = 15
        thickness = 25
        
        # Vertical bar
        v_rect = pygame.Rect(center_x - size//2, center_y - thickness, size, thickness * 2)
        pygame.draw.rect(self.screen, DARK_GRAY, v_rect, border_radius=3)
        pygame.draw.rect(self.screen, WHITE, v_rect, 2, border_radius=3)
        
        # Horizontal bar  
        h_rect = pygame.Rect(center_x - thickness, center_y - size//2, thickness * 2, size)
        pygame.draw.rect(self.screen, DARK_GRAY, h_rect, border_radius=3)
        pygame.draw.rect(self.screen, WHITE, h_rect, 2, border_radius=3)
        
        # Highlight pressed directions
        if up:
            up_rect = pygame.Rect(center_x - size//2, center_y - thickness, size, thickness//2)
            pygame.draw.rect(self.screen, GREEN, up_rect, border_radius=3)
        if down:
            down_rect = pygame.Rect(center_x - size//2, center_y + thickness//2, size, thickness//2)
            pygame.draw.rect(self.screen, GREEN, down_rect, border_radius=3)
        if left:
            left_rect = pygame.Rect(center_x - thickness, center_y - size//2, thickness//2, size)
            pygame.draw.rect(self.screen, GREEN, left_rect, border_radius=3)
        if right:
            right_rect = pygame.Rect(center_x + thickness//2, center_y - size//2, thickness//2, size)
            pygame.draw.rect(self.screen, GREEN, right_rect, border_radius=3)
    
    def draw_face_buttons(self, center_x, center_y, buttons):
        """Draw ABXY buttons in Xbox layout"""
        button_radius = 18
        spacing = 35
        
        # Button positions relative to center
        positions = {
            'Y': (center_x, center_y - spacing),      # Top
            'X': (center_x - spacing, center_y),     # Left  
            'B': (center_x + spacing, center_y),     # Right
            'A': (center_x, center_y + spacing)      # Bottom
        }
        
        colors = {
            'Y': (255, 255, 0),   # Yellow
            'X': (0, 150, 255),   # Blue
            'B': (255, 50, 50),   # Red
            'A': (50, 255, 50)    # Green
        }
        
        for i, (button, pos) in enumerate(positions.items()):
            pressed = buttons[i] if i < len(buttons) else False
            color = colors[button] if pressed else GRAY
            
            pygame.draw.circle(self.screen, color, pos, button_radius)
            pygame.draw.circle(self.screen, WHITE, pos, button_radius, 3)
            
            # Button letter
            text_color = WHITE if pressed else BLACK
            text = self.font.render(button, True, text_color)
            text_rect = text.get_rect(center=pos)
            self.screen.blit(text, text_rect)
    
    def draw_center_buttons(self, center_x, center_y, back_pressed, start_pressed, xbox_pressed):
        """Draw center buttons (Back, Xbox, Start)"""
        # Back button (left)
        back_pos = (center_x - 40, center_y - 20)
        color = GREEN if back_pressed else GRAY
        pygame.draw.rect(self.screen, color, (back_pos[0] - 15, back_pos[1] - 8, 30, 16), border_radius=3)
        pygame.draw.rect(self.screen, WHITE, (back_pos[0] - 15, back_pos[1] - 8, 30, 16), 2, border_radius=3)
        text = self.small_font.render("⧉", True, WHITE if back_pressed else BLACK)
        text_rect = text.get_rect(center=back_pos)
        self.screen.blit(text, text_rect)
        
        # Xbox button (center)
        xbox_pos = (center_x, center_y - 20)
        color = GREEN if xbox_pressed else GRAY
        pygame.draw.circle(self.screen, color, xbox_pos, 12)
        pygame.draw.circle(self.screen, WHITE, xbox_pos, 12, 2)
        text = self.small_font.render("⊞", True, WHITE if xbox_pressed else BLACK)
        text_rect = text.get_rect(center=xbox_pos)
        self.screen.blit(text, text_rect)
        
        # Start button (right)  
        start_pos = (center_x + 40, center_y - 20)
        color = GREEN if start_pressed else GRAY
        pygame.draw.rect(self.screen, color, (start_pos[0] - 15, start_pos[1] - 8, 30, 16), border_radius=3)
        pygame.draw.rect(self.screen, WHITE, (start_pos[0] - 15, start_pos[1] - 8, 30, 16), 2, border_radius=3)
        text = self.small_font.render("≡", True, WHITE if start_pressed else BLACK)
        text_rect = text.get_rect(center=start_pos)
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
            self.screen.fill(WHITE)
            
            # Check for joystick connection changes
            joystick_count = pygame.joystick.get_count()
            if joystick_count != self.joystick_count:
                self.joystick_count = joystick_count
                self.init_joystick()
            
            # Draw title
            title = self.large_font.render("Xbox Controller Visualizer", True, BLACK)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 40))
            self.screen.blit(title, title_rect)
            
            if self.joystick is None:
                # No gamepad connected
                no_gamepad_text = self.font.render("No controller connected", True, RED)
                text_rect = no_gamepad_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                self.screen.blit(no_gamepad_text, text_rect)
                
                instruction_text = self.small_font.render("Connect an Xbox controller to see visualization", True, GRAY)
                instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
                self.screen.blit(instruction_text, instruction_rect)
            else:
                # Draw controller body
                center_x, center_y = self.draw_controller_body()
                
                # Display controller name
                gamepad_name = self.joystick.get_name()
                name_text = self.small_font.render(f"Controller: {gamepad_name}", True, BLACK)
                name_rect = name_text.get_rect(center=(WINDOW_WIDTH//2, 80))
                self.screen.blit(name_text, name_rect)
                
                try:
                    num_axes = self.joystick.get_numaxes()
                    num_buttons = self.joystick.get_numbuttons()
                    num_hats = self.joystick.get_numhats()
                    
                    # Get all input values
                    left_x = self.joystick.get_axis(0) if num_axes > 0 else 0
                    left_y = self.joystick.get_axis(1) if num_axes > 1 else 0
                    right_x = self.joystick.get_axis(3) if num_axes > 3 else 0
                    right_y = self.joystick.get_axis(4) if num_axes > 4 else 0
                    
                    left_trigger = max(0, (self.joystick.get_axis(2) + 1) / 2) if num_axes > 2 else 0
                    right_trigger = max(0, (self.joystick.get_axis(5) + 1) / 2) if num_axes > 5 else 0
                    
                    # Triggers (top)
                    self.draw_trigger(center_x - 120, center_y - 120, 40, 20, left_trigger, "LT")
                    self.draw_trigger(center_x + 120, center_y - 120, 40, 20, right_trigger, "RT")
                    
                    # Shoulder buttons
                    lb_pressed = self.joystick.get_button(4) if num_buttons > 4 else False
                    rb_pressed = self.joystick.get_button(5) if num_buttons > 5 else False
                    self.draw_shoulder_button(center_x - 120, center_y - 90, 50, 20, lb_pressed, "LB")
                    self.draw_shoulder_button(center_x + 120, center_y - 90, 50, 20, rb_pressed, "RB")
                    
                    # Left joystick
                    l3_pressed = self.joystick.get_button(9) if num_buttons > 9 else False
                    self.draw_joystick(center_x - 100, center_y + 20, left_x, left_y, 35, "Left Stick", l3_pressed)
                    
                    # Right joystick  
                    r3_pressed = self.joystick.get_button(10) if num_buttons > 10 else False
                    self.draw_joystick(center_x + 100, center_y + 20, right_x, right_y, 35, "Right Stick", r3_pressed)
                    
                    # D-pad (left side)
                    if num_hats > 0:
                        hat = self.joystick.get_hat(0)
                        up = hat[1] > 0
                        down = hat[1] < 0
                        left = hat[0] < 0
                        right = hat[0] > 0
                        self.draw_dpad(center_x - 100, center_y - 25, up, down, left, right)
                    
                    # Face buttons (right side)
                    face_button_states = []
                    for i in range(4):
                        face_button_states.append(self.joystick.get_button(i) if i < num_buttons else False)
                    self.draw_face_buttons(center_x + 100, center_y - 25, face_button_states)
                    
                    # Center buttons
                    back_pressed = self.joystick.get_button(6) if num_buttons > 6 else False
                    start_pressed = self.joystick.get_button(7) if num_buttons > 7 else False
                    xbox_pressed = self.joystick.get_button(8) if num_buttons > 8 else False
                    self.draw_center_buttons(center_x, center_y, back_pressed, start_pressed, xbox_pressed)
                    
                except pygame.error as e:
                    error_text = self.font.render(f"Controller error: {str(e)}", True, RED)
                    text_rect = error_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
                    self.screen.blit(error_text, text_rect)
                    self.joystick = None
            
            # Instructions
            instructions = [
                "ESC - Exit",
                "Connect Xbox controller for real-time visualization"
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