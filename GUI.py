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
        
        if self.joystick_count > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        
        self.running = True
    
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
            
            # Check for joystick connection changes
            pygame.joystick.quit()
            pygame.joystick.init()
            joystick_count = pygame.joystick.get_count()
            
            if joystick_count != self.joystick_count:
                self.joystick_count = joystick_count
                if joystick_count > 0:
                    self.joystick = pygame.joystick.Joystick(0)
                    self.joystick.init()
                else:
                    self.joystick = None
            
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
                
                # Get joystick values
                num_axes = self.joystick.get_numaxes()
                num_buttons = self.joystick.get_numbuttons()
                num_hats = self.joystick.get_numhats()
                
                # Left joystick (usually axes 0 and 1)
                left_x = self.joystick.get_axis(0) if num_axes > 0 else 0
                left_y = self.joystick.get_axis(1) if num_axes > 1 else 0
                self.draw_joystick(150, 200, left_x, left_y, 50, "Left Stick")
                
                # Right joystick (usually axes 2 and 3, or 3 and 4)
                right_x = self.joystick.get_axis(2) if num_axes > 2 else 0
                right_y = self.joystick.get_axis(3) if num_axes > 3 else 0
                self.draw_joystick(350, 200, right_x, right_y, 50, "Right Stick")
                
                # Triggers (usually axes 4 and 5, or 2 and 5)
                left_trigger = 0
                right_trigger = 0
                if num_axes > 4:
                    left_trigger = (self.joystick.get_axis(4) + 1) / 2  # Convert from -1,1 to 0,1
                if num_axes > 5:
                    right_trigger = (self.joystick.get_axis(5) + 1) / 2
                
                self.draw_trigger(500, 150, 30, 100, left_trigger, "LT")
                self.draw_trigger(550, 150, 30, 100, right_trigger, "RT")
                
                # Face buttons (A, B, X, Y)
                button_labels = ["A", "B", "X", "Y"]
                button_positions = [(650, 220), (680, 190), (620, 190), (650, 160)]
                
                for i, (label, pos) in enumerate(zip(button_labels, button_positions)):
                    pressed = self.joystick.get_button(i) if i < num_buttons else False
                    self.draw_button(pos[0], pos[1], 15, pressed, label)
                
                # Shoulder buttons
                lb_pressed = self.joystick.get_button(4) if num_buttons > 4 else False
                rb_pressed = self.joystick.get_button(5) if num_buttons > 5 else False
                self.draw_button(500, 100, 15, lb_pressed, "LB")
                self.draw_button(550, 100, 15, rb_pressed, "RB")
                
                # D-pad
                if num_hats > 0:
                    hat = self.joystick.get_hat(0)
                    up = hat[1] > 0
                    down = hat[1] < 0
                    left = hat[0] < 0
                    right = hat[0] > 0
                    self.draw_dpad(150, 350, up, down, left, right)
                
                # Additional buttons (Start, Select, etc.)
                start_pressed = self.joystick.get_button(7) if num_buttons > 7 else False
                select_pressed = self.joystick.get_button(6) if num_buttons > 6 else False
                self.draw_button(300, 100, 12, start_pressed, "Start")
                self.draw_button(250, 100, 12, select_pressed, "Select")
                
                # Stick buttons (L3, R3)
                l3_pressed = self.joystick.get_button(8) if num_buttons > 8 else False
                r3_pressed = self.joystick.get_button(9) if num_buttons > 9 else False
                self.draw_button(150, 310, 10, l3_pressed, "L3")
                self.draw_button(350, 310, 10, r3_pressed, "R3")
            
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