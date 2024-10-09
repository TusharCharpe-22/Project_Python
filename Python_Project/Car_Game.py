import pygame 
from pygame.locals import *
import random

pygame.init()

# Create the window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# Colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Road and marker sizes
road_width = 300
marker_width = 10
marker_height = 50

# Lane coordinates
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Road and edge markers
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# Player's starting coordinates
player_x = 250
player_y = 400

# Frame settings
clock = pygame.time.Clock()
fps = 60  # Reduced FPS

# Game settings
gameover = False
speed = 2
score = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (45, 90))  # Scale the image
        self.rect = self.image.get_rect(center=(x, y))

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        try:
            image = pygame.image.load('images/car.png')
            super().__init__(image, x, y)
        except pygame.error:
            print("Error loading player vehicle image.")

# Sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# Create the player's car
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# Load vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    try:
        image = pygame.image.load('images/' + image_filename)
        vehicle_images.append(image)
    except pygame.error:
        print(f"Error loading vehicle image: {image_filename}")

# Load the crash image
try:
    crash = pygame.image.load('images/crash.png')
    crash_rect = crash.get_rect()
except pygame.error:
    print("Error loading crash image.")

# Game loop
running = True
while running:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # Move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

    # Check for collisions after moving
    for vehicle in vehicle_group:
        if pygame.sprite.collide_rect(player, vehicle):
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]

    # Draw the grass
    screen.fill(green)
    
    # Draw the road
    pygame.draw.rect(screen, gray, road)
    
    # Draw the edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)
    
    # Draw the lane markers
    lane_marker_move_y = (pygame.time.get_ticks() // 5) % (marker_height * 2)  # Smooth movement
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    # Draw the player's car
    player_group.draw(screen)
    
    # Add a vehicle
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, -50)
            vehicle_group.add(vehicle)
    
    # Make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            if score > 0 and score % 5 == 0:
                speed += 1

    # Draw the vehicles
    vehicle_group.draw(screen)
    
    # Display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect(center=(50, 400))
    screen.blit(text, text_rect)
    
    # Check for head-on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
    
    # Display game over
    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect(center=(width / 2, 100))
        screen.blit(text, text_rect)
    
    pygame.display.flip()

    # Wait for user's input to play again or exit
    while gameover:
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    gameover = False
                    running = False

pygame.quit()
