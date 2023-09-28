'''
Author: Yimin Long
Date: 28 Sep 2023
'''


import pygame
import math
import time
from palette import *


def polygon_centroid(coords):
    n = len(coords)
    if n < 3:
        raise ValueError("A polygon must have at least three vertices")

    A = 0  # total area
    Cx = 0
    Cy = 0

    for i in range(n):
        xi, yi = coords[i]
        xnext, ynext = coords[(i + 1) % n]
        ai = xi * ynext - xnext * yi
        A += ai
        Cx += (xi + xnext) * ai
        Cy += (yi + ynext) * ai

    A /= 2.0
    Cx /= (6.0 * A)
    Cy /= (6.0 * A)

    return Cx, Cy

# Initialize Pygame
pygame.init()

# Load image
image_path = "src/zoomedin.png"
background_image = pygame.image.load(image_path)

# Set the window size to the image size
screen_width, screen_height = background_image.get_size()
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window size and title
window_size = (screen_width, screen_height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("City Battery Distribution")

# Define color
white = (255, 255, 255)
green = (0, 255, 0)

# City node location (x and y)
nodes = [(50, 50), (73, 150), (125, 120), (100, 200), (200, 200), (300, 200),
         (100, 300), (200, 300), (300, 300), (100, 400), (200, 400), (300, 400),
         (100, 500), (200, 500)]

# polygons
polygons = [
    [(144, 472), (306, 418), (396, 655), (331, 680), (311, 677), (256, 698), (202, 689), (182, 602), (143, 485)],
    [(308, 416), (351, 534), (473, 490), (427, 372)],
    [(351, 534), (470, 490), (495, 552), (374, 595)],
    [(374, 596), (395, 657), (542, 602), (531, 572), (508, 578), (495, 552)],
    [(427, 373), (550, 328), (594, 449), (473, 492)],
    [(473, 493), (495, 552), (616, 508), (594, 448)],
    [(495, 553), (507, 581), (531, 574), (542, 600), (637, 567), (615, 508)],
    [(550, 329), (610, 305), (654, 428), (592, 450)],
    [(594, 448), (616, 508), (677, 488), (654, 426)],
    [(616, 508), (637, 569), (700, 547), (678, 489)],
    [(784, 246), (609, 306), (654, 426), (837, 359), (830, 336), (837, 260)],
    [(654, 428), (677, 487), (858, 420), (836, 360)],
    [(678, 488), (699, 547), (880, 479), (858, 420)],
    [(418, 193), (402, 302), (427, 369), (612, 305), (575, 214)]
]
# Demand power (simulated data)
node_demands_1 = [50, 10, 50, 50, 40, -50, -500, 50, 50, 15, 50, 50, 32, 500]

# Find centroids
centroids = []
for polygon in polygons:
    centroids.append(polygon_centroid(polygon))

# Define vehicle and battery capacity
vehicles = {
    "火车": {"电池容量": 50, "每节车厢电池数": 15},
    "电车": {"电池容量": 50, "每节车厢电池数": 4},
}

# Define constant
arrive_point = 1
# Battery threshold at normal times
Power_Threshold = 50
# Emergency power threshold
Power_Threshold_Negative = 15
# 非紧急和紧急情况的判断条件，0意味着最低需求量，小于0的时候继续其他bloke调度电量
Lowest_Power_Demand = 0

arrive_flag = False

# Initialize node battery requirements
node_battery_demand = [0] * len(nodes)

# initial calculate distance array
distances_between_points = []

def calculate_distance(node1, node2):
    distance = []
    x1, y1 = node1
    x2, y2 = node2
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance

# Event processing loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Clear screen
    screen.fill(white)

    # Draw nodes
    for i, (x, y) in enumerate(centroids):
        # 归一化数值到[0, 1]区间
        normalized_demand = min(1, max(0, (node_demands_1[i] + 100) / 200))

        # 计算颜色分量
        r = int((1 - normalized_demand) * 255)
        g = int(normalized_demand * 255)

        # 设置颜色
        color = blend_colors(normalized_demand, ZERO_CAPACITY_COLOUR, FULL_CAPACITY_COLOUR)

        # 绘制圆圈和文本
        # pygame.draw.circle(screen, color, (x, y), 10)
        pygame.draw.polygon(screen, color, polygons[i])
        font = pygame.font.Font(None, 36)
        text = font.render(str(node_demands_1[i]), True, WHITE)
        screen.blit(text, (x-10, y-10))

    # Blit the image onto the screen
    screen.blit(background_image, (0, 0))

    # Update node
    # Batteries arrive at shipping point
    if arrive_flag == True:
        if node_demands_1[arrive_point] < Power_Threshold:
            need_demands = Power_Threshold - node_demands_1[arrive_point]
            node_demands_1[arrive_point] = Power_Threshold
        arrive_flag = False

    for index_selected_node in range(len(nodes)):
        # initial calculate distance array
        distances_between_points = []
        selected_node = nodes[index_selected_node]
        if (node_demands_1[index_selected_node] < Power_Threshold) and (node_demands_1[index_selected_node] >= Lowest_Power_Demand):
            selected_node_x = []
            selected_node_y = []
            for node in nodes:
                selected_node_x.append(node[0])
                selected_node_y.append(node[1])

            for index_2, node in enumerate(nodes):
                if node != selected_node:
                    distance = calculate_distance(selected_node, node)
                    distances_between_points.append((index_2, distance))  # Save node index and distance

            # 按照距离从小到大排序
            distances_between_points.sort(key=lambda x: x[1])

            for index_3 in range(len(distances_between_points)):
                # Calculate how much below power_threshold
                less_power = Power_Threshold - node_demands_1[index_selected_node]
                # Calculate whether this block can provide enough power
                average_demand = node_demands_1[distances_between_points[index_3][0]] - less_power

                # if power enough
                if (node_demands_1[index_selected_node] < Power_Threshold) and (average_demand >= Power_Threshold):
                    node_demands_1[index_selected_node] = Power_Threshold
                    node_demands_1[distances_between_points[index_3][0]] = average_demand

                    break
        # For emergencies, power demand increases significantly
        elif node_demands_1[index_selected_node] < Lowest_Power_Demand:
            for index_4, node in enumerate(nodes):
                if node != selected_node:
                    distance = calculate_distance(selected_node, node)
                    distances_between_points.append((index_4, distance))  # Save node index and distance

            # Sort by distance from small to large
            distances_between_points.sort(key=lambda x: x[1])

            for index_6 in range(len(distances_between_points)):
                # The power requirement is negative
                # Calculate how much below power_threshold
                less_power = Power_Threshold_Negative - node_demands_1[index_selected_node]
                # Calculate whether this block can provide enough power
                add_demand = node_demands_1[distances_between_points[index_6][0]] - Power_Threshold_Negative

                # if power enough
                if (node_demands_1[index_selected_node] < Power_Threshold_Negative) and (add_demand > Lowest_Power_Demand):
                    node_demands_1[index_selected_node] = node_demands_1[index_selected_node] + add_demand
                    node_demands_1[distances_between_points[index_6][0]] = node_demands_1[distances_between_points[index_6][0]] - add_demand

                    break

    # Update screen
    pygame.display.flip()

    # delay 1s
    time.sleep(0.5)

# Exit Pygame
pygame.quit()



