import cv2
import mediapipe as mp
import numpy as np
import pygame

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5
)

# Initialize Pygame
pygame.init()
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Gesture-Based Game")

# Player setup
player_width = 50
player_height = 50
player_x = window_width // 2 - player_width // 2
player_y = window_height - player_height - 10
player_speed = 7   # slightly smoother

# Obstacle setup
obstacle_width = 50
obstacle_height = 50
obstacle_x = np.random.randint(0, window_width - obstacle_width)
obstacle_y = 0
obstacle_speed = 5

# Game over
game_over = False
font_big = pygame.font.Font(None, 64)
font_small = pygame.font.Font(None, 36)

# Restart button
restart_button_rect = pygame.Rect(window_width//2 - 80, window_height//2 + 40, 160, 50)

# Camera
cap = cv2.VideoCapture(0)

running = True
clock = pygame.time.Clock()

while running:

    # 🔹 Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
                # Restart game
                game_over = False
                player_x = window_width // 2 - player_width // 2
                obstacle_x = np.random.randint(0, window_width - obstacle_width)
                obstacle_y = 0

    # 🔹 Camera frame
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    # 🔹 Detect hand
    results = hands.process(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Index finger tip
            tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(tip.x * frame.shape[1])
            y = int(tip.y * frame.shape[0])

            # Gesture logic (LEFT / RIGHT)
            if x < frame.shape[1] // 3:
                gesture = "Left"
                player_x -= player_speed

            elif x > frame.shape[1] * 2 // 3:
                gesture = "Right"
                player_x += player_speed

            else:
                gesture = "Center"

            # Draw on camera
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
            cv2.putText(frame, gesture, (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 🔹 GAME LOGIC
    if not game_over:

        # Player boundaries
        player_x = max(0, min(player_x, window_width - player_width))

        # Move obstacle
        obstacle_y += obstacle_speed

        # Collision detection
        if (player_x < obstacle_x + obstacle_width and
            player_x + player_width > obstacle_x and
            player_y < obstacle_y + obstacle_height and
            player_y + player_height > obstacle_y):

            game_over = True

        # Reset obstacle
        if obstacle_y > window_height:
            obstacle_y = 0
            obstacle_x = np.random.randint(0, window_width - obstacle_width)

    # 🔹 DRAW GAME
    window.fill((0, 0, 0))

    pygame.draw.rect(window, (255, 255, 255),
                     (player_x, player_y, player_width, player_height))

    pygame.draw.rect(window, (255, 0, 0),
                     (obstacle_x, obstacle_y, obstacle_width, obstacle_height))

    # 🔹 Game Over UI
    if game_over:
        text = font_big.render("Game Over", True, (255, 255, 255))
        window.blit(text, (window_width//2 - text.get_width()//2,
                           window_height//2 - 60))

        pygame.draw.rect(window, (0, 0, 255), restart_button_rect)
        restart_text = font_small.render("Restart", True, (255, 255, 255))
        window.blit(restart_text,
                    (restart_button_rect.x + 30, restart_button_rect.y + 10))

    pygame.display.update()
    clock.tick(60)

# Cleanup
cap.release()
cv2.destroyAllWindows()
pygame.quit()