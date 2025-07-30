import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Signal Simulation")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)

# Vehicle properties
# vehicles = {'N': [], 'E': [], 'S': [], 'W': []}
VEHICLE_SIZE = (20, 40)
# VEHICLE_SPEED = 2
# Vehicle properties
vehicles = {'N': [], 'E': [], 'S': [], 'W': []}
VEHICLE_RADIUS = 5  # Radius of the vehicle dots
VEHICLE_SPEED = 10

# Signal timing
# signal_time = 20000  # 20 seconds for each signal
# last_switch = pygame.time.get_ticks()  # Initialize the switch time
# current_light = 'N'  # Starting with North
last_switch = pygame.time.get_ticks()  # Initialize the switch time
current_light = 'N'  # Starting with North
# Function to draw the roads and traffic lights
def draw_roads():
    screen.fill(GRAY)

    # Draw the four roads
    pygame.draw.rect(screen, BLACK, (WIDTH//2 - 50, 0, 100, HEIGHT))  # Vertical road
    pygame.draw.rect(screen, BLACK, (0, HEIGHT//2 - 50, WIDTH, 100))  # Horizontal road

    # Draw traffic lights
    pygame.draw.rect(screen, GREEN if current_light == 'N' else RED, (WIDTH//2 - 60, HEIGHT//2 - 110, 20, 20))  # North light
    pygame.draw.rect(screen, GREEN if current_light == 'E' else RED, (WIDTH//2 + 90, HEIGHT//2 - 60, 20, 20))   # East light
    pygame.draw.rect(screen, GREEN if current_light == 'S' else RED, (WIDTH//2 + 40, HEIGHT//2 + 90, 20, 20))  # South light
    pygame.draw.rect(screen, GREEN if current_light == 'W' else RED, (WIDTH//2 - 110, HEIGHT//2 + 40, 20, 20)) # West light

# Function to update and draw vehicles
def update_vehicles():
    # Add new vehicles randomly
    for direction in vehicles:
        if random.random() < 0.02:  # Adjust this rate for more or fewer vehicles
            if direction == 'N':
                vehicles['N'].append([WIDTH//2 - 25, 0])
            elif direction == 'E':
                vehicles['E'].append([WIDTH, HEIGHT//2 - 25])
            elif direction == 'S':
                vehicles['S'].append([WIDTH//2 + 5, HEIGHT])
            elif direction == 'W':
                vehicles['W'].append([0, HEIGHT//2 + 5])

    # Move vehicles and manage queuing
    for direction, vehicle_list in vehicles.items():
        for i, vehicle in enumerate(vehicle_list):
            if direction == 'N':
                # Stop if the light is red and the car is near the intersection, or if there is a car ahead
                if current_light == 'N' or vehicle[1] < HEIGHT//2 - 110:
                    if i == 0 or (vehicle_list[i-1][1] - vehicle[1] > VEHICLE_RADIUS * 2):  # Maintain spacing in queue
                        vehicle[1] += VEHICLE_SPEED
            elif direction == 'E':
                if current_light == 'E' or vehicle[0] > WIDTH//2 + 90:
                    if i == 0 or (vehicle[0] - vehicle_list[i-1][0] > VEHICLE_RADIUS * 2):
                        vehicle[0] -= VEHICLE_SPEED
            elif direction == 'S':
                if current_light == 'S' or vehicle[1] > HEIGHT//2 + 90:
                    if i == 0 or (vehicle[1] - vehicle_list[i-1][1] > VEHICLE_RADIUS * 2):
                        vehicle[1] -= VEHICLE_SPEED
            elif direction == 'W':
                if current_light == 'W' or vehicle[0] < WIDTH//2 - 110:
                    if i == 0 or (vehicle_list[i-1][0] - vehicle[0] > VEHICLE_RADIUS * 2):
                        vehicle[0] += VEHICLE_SPEED
    # Draw vehicles as dots
    for direction, vehicle_list in vehicles.items():
        for vehicle in vehicle_list:
            pygame.draw.circle(screen, LIGHT_BLUE, vehicle, VEHICLE_RADIUS)



# Function to switch traffic lights
# def switch_lights():
#     global current_light, last_switch
#     now = pygame.time.get_ticks()
#     if now - last_switch >= signal_time:
#         last_switch = now
#         # Rotate traffic lights
#         if current_light == 'N':
#             current_light = 'E'
#         elif current_light == 'E':
#             current_light = 'S'
#         elif current_light == 'S':
#             current_light = 'W'
#         elif current_light == 'W':
#             current_light = 'N'
# def switch_lights():
#     global current_light, last_switch, signal_time
#     now = pygame.time.get_ticks()
#     if now - last_switch >= signal_time:
#         last_switch = now

#         # Calculate queue lengths
#         queue_lengths = {direction: len(vehicle_list) for direction, vehicle_list in vehicles.items()}

#         # Find the direction with the longest queue
#         max_queue_direction = max(queue_lengths, key=queue_lengths.get)

#         # Set the current light to the direction with the longest queue
#         current_light = max_queue_direction

#         # Adjust signal time based on queue length
#         signal_time = 20000 if queue_lengths[max_queue_direction] < 10 else 30000
def switch_lights():
    global current_light, last_switch
    now = pygame.time.get_ticks()
    queue_lengths = {direction: len(vehicle_list) for direction, vehicle_list in vehicles.items()}

    # Find the direction with the longest queue
    max_queue_direction = max(queue_lengths, key=queue_lengths.get)
    queue_length = queue_lengths[max_queue_direction]

    # Calculate the time required for the queue to pass through
    passing_time = (queue_length * VEHICLE_SIZE[1]) / VEHICLE_SPEED * 1000  # in milliseconds

    if now - last_switch >= passing_time:
        last_switch = now
        current_light = max_queue_direction# Reset to default after serving the long queue

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update signals and vehicles
    switch_lights()
    draw_roads()
    update_vehicles()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
