import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Signal Simulation")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (0,0,0)
WHITE = (255, 255, 255)
ROAD_COLOR = (20, 20, 20)  # Dark grey for roads

# Clock and timing
clock = pygame.time.Clock()

# Vehicle properties
VEHICLE_RADIUS = 5
VEHICLE_SPEED = 10

# Queue area size
QUEUE_WIDTH = 60
QUEUE_HEIGHT = 151

# Define intersection bounds
INTERSECTION_TOP = HEIGHT // 2 - 50
INTERSECTION_BOTTOM = HEIGHT // 2 + 50
INTERSECTION_LEFT = WIDTH // 2 - 50
INTERSECTION_RIGHT = WIDTH // 2 + 50

# Updated queue areas with East queue area moved closer to the traffic light
queue_areas = {
    'N': pygame.Rect(WIDTH//2 - 35, 40, 70, 160),  # Adjusted position and size
    'E': pygame.Rect(WIDTH - 305, HEIGHT//2 - 35, 150, 70),  # Moved closer to the traffic light
    'S': pygame.Rect(WIDTH//2 - 35, HEIGHT - 205, 70, 150),  # Adjusted position and size
    'W': pygame.Rect(155, HEIGHT//2 - 35, 150, 70)  # Adjusted position and size
}


# Vehicles data structure
vehicles = {'N': [], 'E': [], 'S': [], 'W': []}

# Traffic light state
current_light = 'N'
green_time = 20
light_timer = 0
yellow_phase = True 
YELLOW_TIME = 3

def calculate_queue_lengths():
    queue_lengths = {'N': 0, 'E': 0, 'S': 0, 'W': 0}
    for direction, vehicle_list in vehicles.items():
        for vehicle in vehicle_list:
            vehicle_rect = pygame.Rect(vehicle[0] - VEHICLE_RADIUS, vehicle[1] - VEHICLE_RADIUS, VEHICLE_RADIUS * 2, VEHICLE_RADIUS * 2)
            if queue_areas[direction].colliderect(vehicle_rect):
                queue_lengths[direction] += 1
    return queue_lengths
# Function to prioritize signals based on queue lengths using LQF-MWM
def prioritize_signals(queue_lengths):
    # Find the direction with the maximum queue length
    max_queue_direction = max(queue_lengths, key=queue_lengths.get)
    return max_queue_direction


MIN_GREEN_TIME = 2.5  # Minimum green time in seconds
MAX_GREEN_TIME = 7.5  # Maximum green time in seconds

# Define the time duration each direction stays green
green_light_duration = MIN_GREEN_TIME  # Initial green light duration
#Dynamic traffic light timing based on queue lengths and passing rate
def adjust_signal_timing(queue_lengths):
    # Get the direction to prioritize
    prioritized_direction = prioritize_signals(queue_lengths)

    # Calculate the new green time based on the queue length
    queue_pass_rate = 1  # Adjust this value to tune the rate at which the timing is adapted
    base_time = MIN_GREEN_TIME
    additional_time = (queue_lengths[prioritized_direction] * queue_pass_rate)

    # Calculate the new green time with a cap on the maximum allowed green time
    new_green_time = min(base_time + additional_time, MAX_GREEN_TIME)

    return prioritized_direction, new_green_time

elapsed_green_time = 0


queue_counts = {'N': 0, 'E': 0, 'S': 0, 'W': 0}
light_turned_red = False


    
def update_traffic_lights():
    global current_light, green_light_duration, elapsed_green_time, light_turned_red

    # Calculate the queue lengths for all directions
    queue_lengths = calculate_queue_lengths()

    # Update the elapsed time
    elapsed_green_time += 1 / 30  # Assuming the loop runs at 30 FPS; adjust if needed

    # Check if it's time to change the light
    if elapsed_green_time >= green_light_duration:
        # Reset the elapsed green time
        elapsed_green_time = 0

        # Check if the light has just turned red
        if light_turned_red:
            # Reset queue count for the direction that was red
            queue_counts[current_light] = 0
            light_turned_red = False
        
        # Adjust signal timing and get the new direction and green time
        next_direction, new_green_time = adjust_signal_timing(queue_lengths)
        
        # Set the new direction and ensure the green time is within limits
        current_light = next_direction
        green_light_duration = max(MIN_GREEN_TIME, min(new_green_time, MAX_GREEN_TIME))
        
        # Indicate that the light has just turned green
        light_turned_red = True
    else:
        # Continue with the current light
        pass

total_cars_passed = 0
cars_generated = {'N': 0, 'E': 0, 'S': 0, 'W': 0}


def update_vehicles():
    global total_cars_passed

    # Add new vehicles randomly
    for direction in vehicles:
        if random.random() < 0.02:  # Adjust this rate for more or fewer vehicles
            if direction == 'N':
                vehicles['N'].append([WIDTH // 2 - 25, 0])
                cars_generated['N'] += 1
            elif direction == 'E':
                vehicles['E'].append([WIDTH, HEIGHT // 2 - 25])
                cars_generated['E'] += 1
            elif direction == 'S':
                vehicles['S'].append([WIDTH // 2 + 5, HEIGHT])
                cars_generated['S'] += 1
            elif direction == 'W':
                vehicles['W'].append([0, HEIGHT // 2 + 5])
                cars_generated['W'] += 1

    # Move vehicles and manage queuing and collisions
    for direction, vehicle_list in vehicles.items():
        i = len(vehicle_list) - 1
        while i >= 0:  # Iterate in reverse order to safely pop elements
            vehicle = vehicle_list[i]
            vehicle_rect = pygame.Rect(vehicle[0] - VEHICLE_RADIUS, vehicle[1] - VEHICLE_RADIUS, VEHICLE_RADIUS * 2, VEHICLE_RADIUS * 2)
            collision = False

            # Check for collisions with vehicles from other directions
            for other_direction, other_vehicles in vehicles.items():
                if other_direction != direction:
                    for other_vehicle in other_vehicles:
                        if check_collision(vehicle, other_vehicle):
                            collision = True
                            break
                if collision:
                    break

            if collision:
                # Stop vehicle movement if a collision is detected
                i -= 1
                continue

            # Check if the vehicle has passed the traffic signal
            if has_passed_signal(vehicle, direction):  # Correctly pass vehicle and direction
                # Continue moving vehicles freely once they pass the signal
                if direction == 'N':
                    vehicle[1] += VEHICLE_SPEED
                    if vehicle[1] > HEIGHT:  # Check if it has passed the screen bounds
                        vehicle_list.pop(i)  # Remove the vehicle from the list
                        total_cars_passed += 1  # Increment total cars passed counter
                elif direction == 'E':
                    vehicle[0] -= VEHICLE_SPEED
                    if vehicle[0] < -VEHICLE_RADIUS:  # Check if it has passed the screen bounds
                        vehicle_list.pop(i)  # Remove the vehicle from the list
                        total_cars_passed += 1  # Increment total cars passed counter
                elif direction == 'S':
                    vehicle[1] -= VEHICLE_SPEED
                    if vehicle[1] < -VEHICLE_RADIUS:  # Check if it has passed the screen bounds
                        vehicle_list.pop(i)  # Remove the vehicle from the list
                        total_cars_passed += 1  # Increment total cars passed counter
                elif direction == 'W':
                    vehicle[0] += VEHICLE_SPEED
                    if vehicle[0] > WIDTH + VEHICLE_RADIUS:  # Check if it has passed the screen bounds
                        vehicle_list.pop(i)  # Remove the vehicle from the list
                        total_cars_passed += 1  # Increment total cars passed counter
            else:
                # Manage vehicles still in the queue based on traffic light, including yellow signal
                if direction == 'N':
                    if current_light in ['N', 'N_YELLOW'] or vehicle[1] < HEIGHT // 2 - 110:
                        if i == 0 or (vehicle_list[i - 1][1] - vehicle[1] > VEHICLE_RADIUS * 2):
                            vehicle[1] += VEHICLE_SPEED
                elif direction == 'E':
                    if current_light in ['E', 'E_YELLOW'] or vehicle[0] > WIDTH // 2 + 90:
                        if i == 0 or (vehicle[0] - vehicle_list[i - 1][0] > VEHICLE_RADIUS * 2):
                            vehicle[0] -= VEHICLE_SPEED
                elif direction == 'S':
                    if current_light in ['S', 'S_YELLOW'] or vehicle[1] > HEIGHT // 2 + 90:
                        if i == 0 or (vehicle[1] - vehicle_list[i - 1][1] > VEHICLE_RADIUS * 2):
                            vehicle[1] -= VEHICLE_SPEED
                elif direction == 'W':
                    if current_light in ['W', 'W_YELLOW'] or vehicle[0] < WIDTH // 2 - 110:
                        if i == 0 or (vehicle_list[i - 1][0] - vehicle[0] > VEHICLE_RADIUS * 2):
                            vehicle[0] += VEHICLE_SPEED

            i -= 1  # Move to the previous vehicle

    # Draw vehicles as dots
    for direction, vehicle_list in vehicles.items():
        for vehicle in vehicle_list:
            pygame.draw.circle(screen, WHITE, (int(vehicle[0]), int(vehicle[1])), VEHICLE_RADIUS)

# Function to check if a vehicle has passed the traffic signal
def has_passed_signal(vehicle, direction):
    if direction == 'N':
        return vehicle[1] > HEIGHT // 2 - 110  # Traffic signal position for North direction
    elif direction == 'E':
        return vehicle[0] < WIDTH // 2 + 90  # Traffic signal position for East direction
    elif direction == 'S':
        return vehicle[1] < HEIGHT // 2 + 90  # Traffic signal position for South direction
    elif direction == 'W':
        return vehicle[0] > WIDTH // 2 - 110  # Traffic signal position for West direction

# Function to check for collisions between vehicles
def check_collision(vehicle, other_vehicle):
    vehicle_rect = pygame.Rect(vehicle[0] - VEHICLE_RADIUS, vehicle[1] - VEHICLE_RADIUS, VEHICLE_RADIUS * 2, VEHICLE_RADIUS * 2)
    other_vehicle_rect = pygame.Rect(other_vehicle[0] - VEHICLE_RADIUS, other_vehicle[1] - VEHICLE_RADIUS, VEHICLE_RADIUS * 2, VEHICLE_RADIUS * 2)
    return vehicle_rect.colliderect(other_vehicle_rect)
    

# def update_vehicles():
#     global total_cars_passed
    
#     # Add new vehicles randomly
#     for direction in vehicles:
#         if random.random() < 0.02:  # Adjust this rate for more or fewer vehicles
#             if direction == 'N':
#                 vehicles['N'].append([WIDTH // 2 - 25, 0])
#                 cars_generated['N'] += 1  # Increment the counter for North
#             elif direction == 'E':
#                 vehicles['E'].append([WIDTH, HEIGHT // 2 - 25])
#                 cars_generated['E'] += 1  # Increment the counter for East
#             elif direction == 'S':
#                 vehicles['S'].append([WIDTH // 2 + 5, HEIGHT])
#                 cars_generated['S'] += 1  # Increment the counter for South
#             elif direction == 'W':
#                 vehicles['W'].append([0, HEIGHT // 2 + 5])
#                 cars_generated['W'] += 1  # Increment the counter for West

#     # Move vehicles and manage queuing and collisions
#     for direction, vehicle_list in vehicles.items():
#         colliding_vehicles = []  # Track which vehicles are colliding


#         for i, vehicle in enumerate(vehicle_list):
#             vehicle_rect = pygame.Rect(vehicle[0] - VEHICLE_RADIUS, vehicle[1] - VEHICLE_RADIUS, VEHICLE_RADIUS * 2, VEHICLE_RADIUS * 2)
#             collision = False
#             for other_direction, other_vehicles in vehicles.items():
#                 if other_direction != direction:  # Only check against vehicles from other directions
#                     for other_vehicle in other_vehicles:
#                         # Call check_collision with correct arguments: vehicle, other_vehicle, and direction
#                         if check_collision(vehicle, other_vehicle, direction):
#                             collision = True
#                             break  # Stop checking further if collision is found
#                 if collision:
#                     break  # Stop checking further directions if collision is found

#             if collision:
#                 continue  # Skip moving the vehicle if a collision is detected

#             if has_passed_signal(vehicle, direction): 
#                 # Continue moving vehicles freely once they pass the signal
#                   if direction == 'N':
#                     vehicle[1] += VEHICLE_SPEED
#                     if vehicle[1] > HEIGHT:  # Check if it has passed the screen bounds
#                         vehicle_list.pop(i)  # Remove the vehicle from the list
#                         total_cars_passed += 1  # Increment total cars passed counter
#                   elif direction == 'E':
#                     vehicle[0] -= VEHICLE_SPEED
#                     if vehicle[0] < -VEHICLE_RADIUS:  # Check if it has passed the screen bounds
#                         vehicle_list.pop(i)  # Remove the vehicle from the list
#                         total_cars_passed += 1  # Increment total cars passed counter
#                   elif direction == 'S':
#                     vehicle[1] -= VEHICLE_SPEED
#                     if vehicle[1] < -VEHICLE_RADIUS:  # Check if it has passed the screen bounds
#                         vehicle_list.pop(i)  # Remove the vehicle from the list
#                         total_cars_passed += 1  # Increment total cars passed counter
#                   elif direction == 'W':
#                     vehicle[0] += VEHICLE_SPEED
#                     if vehicle[0] > WIDTH + VEHICLE_RADIUS:  # Check if it has passed the screen bounds
#                         vehicle_list.pop(i)  # Remove the vehicle from the list
#                         total_cars_passed += 1  # Increment total cars passed counter 

#             else:
#                 # Manage vehicles still in the queue based on traffic light, including yellow signal
#                 if direction == 'N':
#                     if current_light == 'N' or vehicle[1] < HEIGHT//2 - 110:
#                         if i == 0 or (vehicle_list[i-1][1] - vehicle[1] > VEHICLE_RADIUS * 2):
#                             vehicle[1] += VEHICLE_SPEED
#                 elif direction == 'E':
#                     if current_light == 'E' or vehicle[0] > WIDTH//2 + 90:
#                         if i == 0 or (vehicle[0] - vehicle_list[i-1][0] > VEHICLE_RADIUS * 2):
#                             vehicle[0] -= VEHICLE_SPEED
#                 elif direction == 'S':
#                     if current_light == 'S' or vehicle[1] > HEIGHT//2 + 90:
#                         if i == 0 or (vehicle[1] - vehicle_list[i-1][1] > VEHICLE_RADIUS * 2):
#                             vehicle[1] -= VEHICLE_SPEED
#                 elif direction == 'W':
#                     if current_light == 'W' or vehicle[0] < WIDTH//2 - 110:
#                         if i == 0 or (vehicle_list[i-1][0] - vehicle[0] > VEHICLE_RADIUS * 2):
#                             vehicle[0] += VEHICLE_SPEED


#     # Draw vehicles as dots
#     for direction, vehicle_list in vehicles.items():
#         for vehicle in vehicle_list:
#             pygame.draw.circle(screen, WHITE, (int(vehicle[0]), int(vehicle[1])), VEHICLE_RADIUS)

# # Define a function to check if the vehicle has passed the traffic signal
# def has_passed_signal(vehicle, direction):
#     if direction == 'N':
#         return vehicle[1] > HEIGHT // 2 - 110  # Traffic signal position for North direction
#     elif direction == 'E':
#         return vehicle[0] < WIDTH // 2 + 90  # Traffic signal position for East direction
#     elif direction == 'S':
#         return vehicle[1] < HEIGHT // 2 + 90  # Traffic signal position for South direction
#     elif direction == 'W':
#         return vehicle[0] > WIDTH // 2 - 110  # Traffic signal position for West direction
        
# # Function to check for collisions between vehicles
# def check_collision(vehicle, other_vehicle, direction):
#     if direction in ['N', 'S']:
#         # Check vertical collision for North and South vehicles
#         return abs(vehicle[0] - other_vehicle[0]) < VEHICLE_RADIUS * 2 and abs(vehicle[1] - other_vehicle[1]) < VEHICLE_RADIUS * 2
#     elif direction in ['E', 'W']:
#         # Check horizontal collision for East and West vehicles
#         return abs(vehicle[0] - other_vehicle[0]) < VEHICLE_RADIUS * 2 and abs(vehicle[1] - other_vehicle[1]) < VEHICLE_RADIUS * 2
#     return False    




# Draw queue areas with a green border
def draw_queue_areas():
    font = pygame.font.SysFont(None, 30)  # Font for displaying text

    for direction, rect in queue_areas.items():
        # Determine the color based on queue length
        queue_length = len(vehicles[direction])
        if queue_length < 5:
            color = (0, 255, 0)  # Green for short queues
        elif queue_length < 10:
            color = (255, 255, 0)  # Yellow for medium queues
        else:
            color = (255, 0, 0)  # Red for long queues

        pygame.draw.rect(screen, color, rect)  # Draw the queue area with color

        # Draw the queue border
        pygame.draw.rect(screen, (0, 255, 0), rect, 1)  # Green border

        # Render and draw the queue length text
        text = font.render(f'{queue_length}', True, (255, 255, 255))
        screen.blit(text, (rect.x + 5, rect.y + 5))  # Adjust position as needed


# Function to draw roads in a cross pattern
def draw_roads():
    # Draw vertical road
    pygame.draw.rect(screen, ROAD_COLOR, (WIDTH//2 - 50, 0, 100, HEIGHT))
    # Draw horizontal road
    pygame.draw.rect(screen, ROAD_COLOR, (0, HEIGHT//2 - 50, WIDTH, 100))
    
    # Draw traffic lights closer to the intersection corners
    pygame.draw.rect(screen, GREEN if current_light == 'N' else RED, (WIDTH//2 - 60, HEIGHT//2 - 110, 20, 20))  # North light
    pygame.draw.rect(screen, GREEN if current_light == 'E' else RED, (WIDTH//2 + 90, HEIGHT//2 - 60, 20, 20))   # East light
    pygame.draw.rect(screen, GREEN if current_light == 'S' else RED, (WIDTH//2 + 40, HEIGHT//2 + 90, 20, 20))  # South light
    pygame.draw.rect(screen, GREEN if current_light == 'W' else RED, (WIDTH//2 - 110, HEIGHT//2 + 40, 20, 20)) # West light
#display_total_cars_passed()
def display_total_cars_passed():
    font = pygame.font.Font(None, 30)  # Choose a font and size
    text = font.render(f"Total Cars Passed: {total_cars_passed}", True, (255, 255, 255))  # White color text
    screen.blit(text, (WIDTH - 300, 20))  # Display at the top-right corner

def display_cars_generated():
    font = pygame.font.Font(None, 30)  # Use default font and size 30
    y_offset = 60  # Starting y position for the first line of text
    for direction, count in cars_generated.items():
        text = font.render(f"Cars from {direction}: {count}", True, (255, 255, 255))  # Render the text in white
        screen.blit(text, (WIDTH - 250, y_offset))  # Position the text near the total count
        y_offset += 30  # Move down for the next line of text


# Main simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((50, 50, 50))  # Clear screen with grey

    draw_roads()            # Draw roads
    draw_queue_areas()      # Draw queue areas with green borders                      
    update_traffic_lights()
    update_vehicles()  # Update vehicle positions and handle collisions
    display_total_cars_passed()
    display_cars_generated()


    pygame.display.flip()
    clock.tick(30)

pygame.quit()

