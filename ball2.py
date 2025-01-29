import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eight Bouncing Balls in Rotating Square")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0,255,0)

YELLOWDARK = (128, 128, 0)
REDDARK = (128, 0, 0)
BLUEDARK = (0, 0, 128)
GREENDARK = (0,128,0)


BLACK = (0, 0, 0)

# Square properties
SQUARE_SIZE = 450
square_angle = 0
square_rotation_speed = 1

# Ball properties
BALL_RADIUS = 10
INITIAL_SPEED = 4

# Create multiple balls with different positions and directions
balls = [
    {
        'pos': [WIDTH // 2 - 50, HEIGHT // 2],
        'speed': [INITIAL_SPEED, INITIAL_SPEED],
        'color': YELLOW
    },
    {
        'pos': [WIDTH // 2 - 25, HEIGHT // 2],
        'speed': [INITIAL_SPEED, INITIAL_SPEED],
        'color': YELLOWDARK
    },
    {
        'pos': [WIDTH // 2 + 50, HEIGHT // 2],
        'speed': [-INITIAL_SPEED, -INITIAL_SPEED],
        'color': RED
    },
    {
        'pos': [WIDTH // 2 + 25, HEIGHT // 2],
        'speed': [-INITIAL_SPEED, -INITIAL_SPEED],
        'color': REDDARK
    },
    {
        'pos': [WIDTH // 2, HEIGHT // 2 - 50],
        'speed': [INITIAL_SPEED, -INITIAL_SPEED],
        'color': BLUE
    },
    {
        'pos': [WIDTH // 2, HEIGHT // 2 - 25],
        'speed': [INITIAL_SPEED, -INITIAL_SPEED],
        'color': BLUEDARK
    },
    {
        'pos': [WIDTH // 2 - 50, HEIGHT // 2 - 50],
        'speed': [-INITIAL_SPEED, INITIAL_SPEED],
        'color': GREEN
    },
    {
        'pos': [WIDTH // 2 - 25, HEIGHT // 2 - 25],
        'speed': [-INITIAL_SPEED, INITIAL_SPEED],
        'color': GREENDARK
    }
]

def get_rotated_square_vertices(angle):
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    half_size = SQUARE_SIZE // 2
    vertices = []
    for i in range(4):
        base_angle = math.radians(i * 90 + angle)
        x = center_x + half_size * math.cos(base_angle)
        y = center_y + half_size * math.sin(base_angle)
        vertices.append((x, y))
    return vertices

def normalize_vector(vector):
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    if magnitude == 0:
        return [0, 0]
    return [vector[0]/magnitude, vector[1]/magnitude]

def get_closest_point_on_line(point, line_start, line_end):
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end

    dx = x2 - x1
    dy = y2 - y1
    line_length_sq = dx*dx + dy*dy

    if line_length_sq == 0:
        return line_start

    t = max(0, min(1, ((px - x1)*dx + (py - y1)*dy) / line_length_sq))

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    return (closest_x, closest_y)

def distance_between_points(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update square rotation
    square_angle += square_rotation_speed
    vertices = get_rotated_square_vertices(square_angle)

    # Update each ball
    for ball in balls:
        # Check collision with edges
        min_distance = float('inf')
        collision_normal = None
        collision_point = None

        # Check each edge of the square
        for i in range(4):
            j = (i + 1) % 4
            edge_start = vertices[i]
            edge_end = vertices[j]

            closest = get_closest_point_on_line(ball['pos'], edge_start, edge_end)
            distance = distance_between_points(ball['pos'], closest)

            if distance < min_distance:
                min_distance = distance
                collision_point = closest

                if distance > 0:
                    normal = [(ball['pos'][0] - closest[0])/distance,
                             (ball['pos'][1] - closest[1])/distance]
                else:
                    edge_dx = edge_end[0] - edge_start[0]
                    edge_dy = edge_end[1] - edge_start[1]
                    normal = normalize_vector([-edge_dy, edge_dx])

                collision_normal = normal

        # Handle collision
        if min_distance < BALL_RADIUS + 1:
            dot_product = (ball['speed'][0] * collision_normal[0] +
                          ball['speed'][1] * collision_normal[1])

            ball['speed'][0] = ball['speed'][0] - 2 * dot_product * collision_normal[0]
            ball['speed'][1] = ball['speed'][1] - 2 * dot_product * collision_normal[1]

            # Normalize speed
            current_speed = math.sqrt(ball['speed'][0]**2 + ball['speed'][1]**2)
            ball['speed'][0] = ball['speed'][0] * INITIAL_SPEED / current_speed
            ball['speed'][1] = ball['speed'][1] * INITIAL_SPEED / current_speed

            # Push ball out of collision
            overlap = BALL_RADIUS - min_distance
            if overlap > 0:
                ball['pos'][0] += collision_normal[0] * (overlap + 1)
                ball['pos'][1] += collision_normal[1] * (overlap + 1)

        # Update ball position
        ball['pos'][0] += ball['speed'][0]
        ball['pos'][1] += ball['speed'][1]

    # Clear screen
    screen.fill(BLACK)

    # Draw rotating square
    pygame.draw.polygon(screen, WHITE, vertices, 2)

    # Draw all balls
    for ball in balls:
        pygame.draw.circle(screen, ball['color'],
                         (int(ball['pos'][0]), int(ball['pos'][1])),
                         BALL_RADIUS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()