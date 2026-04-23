"""
🎮 GESTURE-BASED GAME CONTROL SYSTEM
=====================================
Control multiple real-time games using hand gestures via webcam.

SUPPORTED GAMES:
1. TEMPLE RUN - Avoid obstacles by swiping LEFT/RIGHT/UP
2. SUBWAY SURFERS - Dodge trains on tracks (LEFT/RIGHT/UP/DOWN)
3. CAR RACING - Avoid traffic by steering (LEFT/RIGHT)
4. FLAPPY BIRD - Flap by raising hand (UP gesture)
5. DINOSAUR RUN - Jump over obstacles (UP gesture)

GESTURE CONTROLS:
- LEFT SWIPE (or hand on LEFT): Move left / Steer left
- RIGHT SWIPE (or hand on RIGHT): Move right / Steer right  
- UP SWIPE (or hand raised UP): Jump / Flap / Climb
- DOWN SWIPE (or hand DOWN): Slide / Crouch / Dive
- FIST: Pause / Unpause game
- OPEN HAND: Reset / Start game

INSTRUCTIONS:
1. Select a game from the menu
2. Sit in front of camera ~60cm away
3. Use clear hand gestures to control
4. Avoid obstacles to score points
5. Pause with FIST gesture
6. Press 'Q' to return to menu
"""

import cv2
import mediapipe as mp
import numpy as np
import pygame
import random
import sys
import os

# Add parent directory to path for gesture_mouse import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6
)

# Initialize Pygame
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("🎮 Gesture-Based Games")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    sys.exit(1)

# Game mode difficulty settings
DIFFICULTY_SETTINGS = {
    "easy": {
        "spawn_rate_multiplier": 1.5,  # Slower spawn
        "speed_multiplier": 0.7,        # Slower obstacles
        "score_multiplier": 2.0         # More points per obstacle
    },
    "medium": {
        "spawn_rate_multiplier": 1.0,
        "speed_multiplier": 1.0,
        "score_multiplier": 1.0
    },
    "hard": {
        "spawn_rate_multiplier": 0.7,   # Faster spawn
        "speed_multiplier": 1.4,         # Faster obstacles
        "score_multiplier": 1.5          # More points
    }
}

# Get game mode from command line
game_mode = "medium"
if len(sys.argv) > 1:
    game_mode = sys.argv[1].lower()
    if game_mode not in DIFFICULTY_SETTINGS:
        game_mode = "medium"

difficulty = DIFFICULTY_SETTINGS[game_mode]

# ==================== GAME STATE ====================
class GameState:
    def __init__(self):
        self.game_running = True
        self.current_game = None
        self.paused = False
        self.score = 0
        self.game_over = False


# ==================== TEMPLE RUN GAME ====================
class TempleRunGame(GameState):
    def __init__(self):
        super().__init__()
        self.player_x = WINDOW_WIDTH // 2
        self.player_y = WINDOW_HEIGHT - 80
        self.player_width = 40
        self.player_height = 60
        self.player_speed = 5
        
        self.obstacles = []
        self.base_spawn_rate = int(30 * difficulty["spawn_rate_multiplier"])
        self.frame_count = 0
        self.score = 0
        
    def handle_gesture(self, gesture):
        """Handle gesture input"""
        if gesture == "LEFT":
            self.player_x = max(0, self.player_x - self.player_speed * 3)
        elif gesture == "RIGHT":
            self.player_x = min(WINDOW_WIDTH - self.player_width, 
                              self.player_x + self.player_speed * 3)
        elif gesture == "UP":
            # Jump effect
            if self.player_y == WINDOW_HEIGHT - 80:
                self.player_y -= 100
                
    def update(self):
        """Update game state"""
        self.frame_count += 1
        
        # Spawn obstacles
        if self.frame_count % self.base_spawn_rate == 0:
            obs_x = random.randint(0, WINDOW_WIDTH - 40)
            self.obstacles.append({
                'x': obs_x, 'y': -40, 'width': 40, 'height': 40,
                'speed': (5 + self.score // 100) * difficulty["speed_multiplier"]
            })
        
        # Move obstacles
        for obs in self.obstacles[:]:
            obs['y'] += obs['speed']
            
            # Collision detection
            if (self.player_x < obs['x'] + obs['width'] and
                self.player_x + self.player_width > obs['x'] and
                self.player_y < obs['y'] + obs['height'] and
                self.player_y + self.player_height > obs['y']):
                self.game_over = True
            
            # Remove off-screen obstacles
            if obs['y'] > WINDOW_HEIGHT:
                self.obstacles.remove(obs)
                self.score += int(10 * difficulty["score_multiplier"])
        
        # Gravity (simple jump mechanic)
        if self.player_y < WINDOW_HEIGHT - 80:
            self.player_y += 5
        else:
            self.player_y = WINDOW_HEIGHT - 80
    
    def draw(self, surface):
        """Draw game on surface"""
        surface.fill(BLACK)
        
        # Draw player
        pygame.draw.rect(surface, BLUE, 
                        (self.player_x, self.player_y, 
                         self.player_width, self.player_height))
        
        # Draw obstacles
        for obs in self.obstacles:
            pygame.draw.rect(surface, RED, 
                            (obs['x'], obs['y'], 
                             obs['width'], obs['height']))
        
        # Draw UI
        score_text = font_medium.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        mode_text = font_small.render(f"Mode: {game_mode.upper()}", True, YELLOW)
        surface.blit(mode_text, (10, 50))
        
        if self.game_over:
            game_over_text = font_large.render("GAME OVER!", True, RED)
            surface.blit(game_over_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 50))
            restart_text = font_small.render("Press R to restart or Q to quit", True, YELLOW)
            surface.blit(restart_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 50))


# ==================== SUBWAY SURFERS GAME ====================
class SubwaySurfersGame(GameState):
    def __init__(self):
        super().__init__()
        self.lanes = [0, 1, 2]  # Left, Center, Right
        self.current_lane = 1
        self.player_x = WINDOW_WIDTH // 2
        self.player_y = WINDOW_HEIGHT - 100
        self.player_width = 50
        self.player_height = 50
        
        self.trains = []
        self.base_spawn_rate = int(40 * difficulty["spawn_rate_multiplier"])
        self.frame_count = 0
        self.score = 0
        
    def handle_gesture(self, gesture):
        """Handle gesture input"""
        if gesture == "LEFT" and self.current_lane > 0:
            self.current_lane -= 1
            self.player_x = 150 + self.current_lane * 250
        elif gesture == "RIGHT" and self.current_lane < 2:
            self.current_lane += 1
            self.player_x = 150 + self.current_lane * 250
        elif gesture == "UP":
            self.player_y -= 50  # Jump
            
    def update(self):
        """Update game state"""
        self.frame_count += 1
        
        # Spawn trains
        if self.frame_count % self.base_spawn_rate == 0:
            lane = random.randint(0, 2)
            train_x = 100 + lane * 250
            self.trains.append({
                'x': train_x, 'y': -50, 'width': 80, 'height': 40,
                'speed': (7 + self.score // 100) * difficulty["speed_multiplier"]
            })
        
        # Move trains
        for train in self.trains[:]:
            train['y'] += train['speed']
            
            # Collision detection
            if (self.player_x < train['x'] + train['width'] and
                self.player_x + self.player_width > train['x'] and
                self.player_y < train['y'] + train['height'] and
                self.player_y + self.player_height > train['y']):
                self.game_over = True
            
            if train['y'] > WINDOW_HEIGHT:
                self.trains.remove(train)
                self.score += int(15 * difficulty["score_multiplier"])
        
        # Gravity
        if self.player_y < WINDOW_HEIGHT - 100:
            self.player_y += 6
        else:
            self.player_y = WINDOW_HEIGHT - 100
    
    def draw(self, surface):
        """Draw game on surface"""
        surface.fill(BLACK)
        
        # Draw lanes
        for i in range(1, 3):
            pygame.draw.line(surface, (50, 50, 50), 
                            (100 + i * 250, 0), 
                            (100 + i * 250, WINDOW_HEIGHT), 2)
        
        # Draw player
        pygame.draw.circle(surface, GREEN, 
                          (int(self.player_x), int(self.player_y)), 
                          self.player_width // 2)
        
        # Draw trains
        for train in self.trains:
            pygame.draw.rect(surface, RED, 
                            (train['x'], train['y'], 
                             train['width'], train['height']))
        
        # Draw UI
        score_text = font_medium.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        mode_text = font_small.render(f"Mode: {game_mode.upper()}", True, YELLOW)
        surface.blit(mode_text, (10, 50))
        
        if self.game_over:
            game_over_text = font_large.render("CRASHED!", True, RED)
            surface.blit(game_over_text, (WINDOW_WIDTH//2 - 120, WINDOW_HEIGHT//2 - 50))


# ==================== CAR RACING GAME ====================
class CarRacingGame(GameState):
    def __init__(self):
        super().__init__()
        self.player_x = WINDOW_WIDTH // 2
        self.player_y = WINDOW_HEIGHT - 80
        self.player_width = 40
        self.player_height = 60
        self.player_speed = 6
        
        self.traffic = []
        self.base_spawn_rate = int(35 * difficulty["spawn_rate_multiplier"])
        self.frame_count = 0
        self.score = 0
        
    def handle_gesture(self, gesture):
        """Handle gesture input"""
        if gesture == "LEFT":
            self.player_x = max(20, self.player_x - self.player_speed * 4)
        elif gesture == "RIGHT":
            self.player_x = min(WINDOW_WIDTH - 60, self.player_x + self.player_speed * 4)
            
    def update(self):
        """Update game state"""
        self.frame_count += 1
        
        if self.frame_count % self.base_spawn_rate == 0:
            traffic_x = random.choice([100, 350, 600])
            self.traffic.append({
                'x': traffic_x, 'y': -60, 'width': 50, 'height': 60,
                'speed': (6 + self.score // 150) * difficulty["speed_multiplier"]
            })
        
        for car in self.traffic[:]:
            car['y'] += car['speed']
            
            if (self.player_x < car['x'] + car['width'] and
                self.player_x + self.player_width > car['x'] and
                self.player_y < car['y'] + car['height'] and
                self.player_y + self.player_height > car['y']):
                self.game_over = True
            
            if car['y'] > WINDOW_HEIGHT:
                self.traffic.remove(car)
                self.score += int(20 * difficulty["score_multiplier"])
    
    def draw(self, surface):
        """Draw game on surface"""
        surface.fill((34, 139, 34))  # Green road
        
        # Draw road lanes
        for i in range(0, WINDOW_HEIGHT, 30):
            pygame.draw.line(surface, YELLOW, 
                            (WINDOW_WIDTH // 2, i), 
                            (WINDOW_WIDTH // 2, i + 15), 3)
        
        # Draw player car
        pygame.draw.rect(surface, BLUE, 
                        (self.player_x, self.player_y, 
                         self.player_width, self.player_height))
        
        # Draw traffic
        for car in self.traffic:
            pygame.draw.rect(surface, RED, 
                            (car['x'], car['y'], 
                             car['width'], car['height']))
        
        score_text = font_medium.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        mode_text = font_small.render(f"Mode: {game_mode.upper()}", True, YELLOW)
        surface.blit(mode_text, (10, 50))
        
        if self.game_over:
            game_over_text = font_large.render("COLLISION!", True, RED)
            surface.blit(game_over_text, (WINDOW_WIDTH//2 - 140, WINDOW_HEIGHT//2 - 50))


# ==================== FLAPPY BIRD GAME ====================
class FlappyBirdGame(GameState):
    def __init__(self):
        super().__init__()
        self.player_y = WINDOW_HEIGHT // 2
        self.player_x = WINDOW_WIDTH // 4
        self.player_size = 30
        self.velocity = 0
        
        self.pipes = []
        self.base_spawn_rate = int(80 * difficulty["spawn_rate_multiplier"])
        self.frame_count = 0
        self.score = 0
        
    def handle_gesture(self, gesture):
        """Handle gesture input"""
        if gesture == "UP":
            self.velocity = -8  # Jump
            
    def update(self):
        """Update game state"""
        self.frame_count += 1
        
        # Gravity
        self.velocity += 0.3
        self.player_y += self.velocity
        
        # Spawn pipes
        if self.frame_count % self.base_spawn_rate == 0:
            gap = 100
            gap_y = random.randint(50, WINDOW_HEIGHT - gap - 50)
            self.pipes.append({
                'x': WINDOW_WIDTH,
                'gap_y': gap_y,
                'gap': gap,
                'width': 50,
                'speed': (5 + self.score // 100) * difficulty["speed_multiplier"]
            })
        
        # Move pipes
        for pipe in self.pipes[:]:
            pipe['x'] -= pipe['speed']
            
            # Collision detection
            if (self.player_x < pipe['x'] + pipe['width'] and
                self.player_x + self.player_size > pipe['x']):
                if (self.player_y < pipe['gap_y'] or 
                    self.player_y + self.player_size > pipe['gap_y'] + pipe['gap']):
                    self.game_over = True
            
            if pipe['x'] < -50:
                self.pipes.remove(pipe)
                self.score += int(25 * difficulty["score_multiplier"])
        
        # Check bounds
        if self.player_y < 0 or self.player_y > WINDOW_HEIGHT:
            self.game_over = True
    
    def draw(self, surface):
        """Draw game on surface"""
        surface.fill((135, 206, 235))  # Sky blue
        
        # Draw player
        pygame.draw.circle(surface, YELLOW, 
                          (int(self.player_x), int(self.player_y)), 
                          self.player_size)
        
        # Draw pipes
        for pipe in self.pipes:
            # Top pipe
            pygame.draw.rect(surface, GREEN, 
                            (pipe['x'], 0, pipe['width'], pipe['gap_y']))
            # Bottom pipe
            pygame.draw.rect(surface, GREEN, 
                            (pipe['x'], pipe['gap_y'] + pipe['gap'], 
                             pipe['width'], WINDOW_HEIGHT - pipe['gap_y'] - pipe['gap']))
        
        score_text = font_medium.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 10))
        mode_text = font_small.render(f"Mode: {game_mode.upper()}", True, YELLOW)
        surface.blit(mode_text, (10, 50))
        
        if self.game_over:
            game_over_text = font_large.render("GAME OVER!", True, RED)
            surface.blit(game_over_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 50))


# ==================== DINOSAUR RUN GAME ====================
class DinosaurRunGame(GameState):
    def __init__(self):
        super().__init__()
        self.player_y = WINDOW_HEIGHT - 80
        self.player_x = WINDOW_WIDTH // 4
        self.player_width = 40
        self.player_height = 50
        self.velocity = 0
        
        self.obstacles = []
        self.base_spawn_rate = int(50 * difficulty["spawn_rate_multiplier"])
        self.frame_count = 0
        self.score = 0
        
    def handle_gesture(self, gesture):
        """Handle gesture input"""
        if gesture == "UP" and self.player_y == WINDOW_HEIGHT - 80:
            self.velocity = -12  # Jump
            
    def update(self):
        """Update game state"""
        self.frame_count += 1
        
        # Gravity
        self.velocity += 0.4
        self.player_y += self.velocity
        
        # Ground collision
        if self.player_y > WINDOW_HEIGHT - 80:
            self.player_y = WINDOW_HEIGHT - 80
            self.velocity = 0
        
        # Spawn obstacles
        if self.frame_count % self.base_spawn_rate == 0:
            self.obstacles.append({
                'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT - 60,
                'width': 30, 'height': 50,
                'speed': (7 + self.score // 120) * difficulty["speed_multiplier"]
            })
        
        # Move obstacles
        for obs in self.obstacles[:]:
            obs['x'] -= obs['speed']
            
            # Collision detection
            if (self.player_x < obs['x'] + obs['width'] and
                self.player_x + self.player_width > obs['x'] and
                self.player_y < obs['y'] + obs['height'] and
                self.player_y + self.player_height > obs['y']):
                self.game_over = True
            
            if obs['x'] < -50:
                self.obstacles.remove(obs)
                self.score += int(10 * difficulty["score_multiplier"])
    
    def draw(self, surface):
        """Draw game on surface"""
        surface.fill((200, 200, 200))
        
        # Draw ground
        pygame.draw.line(surface, BLACK, 
                        (0, WINDOW_HEIGHT - 30),
                        (WINDOW_WIDTH, WINDOW_HEIGHT - 30), 3)
        
        # Draw player (dinosaur)
        pygame.draw.rect(surface, GREEN, 
                        (self.player_x, self.player_y,
                         self.player_width, self.player_height))
        
        # Draw obstacles
        for obs in self.obstacles:
            pygame.draw.rect(surface, RED,
                            (obs['x'], obs['y'],
                             obs['width'], obs['height']))
        
        # Draw UI
        score_text = font_medium.render(f"Score: {self.score}", True, BLACK)
        surface.blit(score_text, (10, 10))
        mode_text = font_small.render(f"Mode: {game_mode.upper()}", True, BLACK)
        surface.blit(mode_text, (10, 50))
        
        if self.game_over:
            game_over_text = font_large.render("GAME OVER!", True, RED)
            surface.blit(game_over_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 50))


# ==================== MENU ====================
def draw_menu(surface):
    """Draw game selection menu"""
    surface.fill(BLACK)
    
    title = font_large.render("🎮 Gesture Games", True, YELLOW)
    surface.blit(title, (WINDOW_WIDTH//2 - 200, 50))
    
    games = [
        "1: Temple Run",
        "2: Subway Surfers",
        "3: Car Racing",
        "4: Flappy Bird",
        "5: Dinosaur Run",
        "Q: Quit"
    ]
    
    for i, game in enumerate(games):
        text = font_medium.render(game, True, GREEN)
        surface.blit(text, (100, 150 + i * 70))


# ==================== MAIN GAME LOOP ====================
def run_game():
    """Main game loop"""
    current_game = None
    game_running = True
    show_menu = True
    
    clock = pygame.time.Clock()
    
    # Track last gesture time to prevent rapid repeated gestures
    last_gesture_time = 0
    gesture_cooldown = 0.2
    
    while game_running:
        # Keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    show_menu = True
                    current_game = None
                if event.key == pygame.K_r and current_game and current_game.game_over:
                    show_menu = True
                    current_game = None
        
        # Game selection
        if show_menu:
            draw_menu(window)
            pygame.display.flip()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                current_game = TempleRunGame()
                show_menu = False
            elif keys[pygame.K_2]:
                current_game = SubwaySurfersGame()
                show_menu = False
            elif keys[pygame.K_3]:
                current_game = CarRacingGame()
                show_menu = False
            elif keys[pygame.K_4]:
                current_game = FlappyBirdGame()
                show_menu = False
            elif keys[pygame.K_5]:
                current_game = DinosaurRunGame()
                show_menu = False
            
            clock.tick(30)
            continue
        
        # Camera frame
        success, frame = cap.read()
        if not success:
            print("Warning: Failed to read camera frame")
            break
        
        frame = cv2.flip(frame, 1)
        
        # Hand detection
        results = hands.process(frame)
        gesture = "NONE"
        current_time = pygame.time.get_ticks() / 1000.0
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x = int(tip.x * frame.shape[1])
                y = int(tip.y * frame.shape[0])
                
                # Simple gesture detection based on hand position
                if x < frame.shape[1] // 3:
                    gesture = "LEFT"
                elif x > frame.shape[1] * 2 // 3:
                    gesture = "RIGHT"
                
                if y < frame.shape[0] // 4:
                    gesture = "UP"
                elif y > frame.shape[0] * 3 // 4:
                    gesture = "DOWN"
        
        # Update game with gesture (with cooldown to prevent rapid inputs)
        if current_game and not current_game.game_over:
            if gesture != "NONE" and (current_time - last_gesture_time) > gesture_cooldown:
                current_game.handle_gesture(gesture)
                last_gesture_time = current_time
            current_game.update()
        
        # Draw game
        if current_game:
            current_game.draw(window)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Check for quit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
    print(f"✅ Game closed. Final score: {current_game.score if current_game else 0}")


if __name__ == "__main__":
    try:
        run_game()
    except KeyboardInterrupt:
        print("\n🛑 Game interrupted by user")
        cap.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        cap.release()
        cv2.destroyAllWindows()
        pygame.quit()
        sys.exit(1)