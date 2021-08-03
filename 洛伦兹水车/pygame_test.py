import pygame
from waterwheel import Water_Wheel
import math


outside_speed = 1
clock = pygame.time.Clock()

water_wheel = Water_Wheel()

pygame.init()
white = (255, 255, 255)
black = (0,0,0)
blue = (91,146,255)
slight_gray = (245,245,245)
slight_blue = (254,131,131)
slight_red = (131,131,254)

height = 700
width = 500

water_max_height = 40

display_surface = pygame.display.set_mode((width, height))

# set the pygame window name
pygame.display.set_caption('洛伦兹水车')
icon = pygame.image.load('icon.jpg')
icon = pygame.transform.scale(icon, (20, 20))
pygame.display.set_icon(icon)

deep_blue_bucket = pygame.image.load(r'深蓝水桶.png')
deep_blue_bucket = pygame.transform.scale(deep_blue_bucket, (40, 40))

deep_red_bucket = pygame.image.load(r'深红水桶.png')
deep_red_bucket = pygame.transform.scale(deep_red_bucket, (40, 40))

count = 0
barycenter_list = []

while True:
    count += 1

    bucket_num = water_wheel.bucket_num
    bucket_angles = [i - math.pi/2 for i in water_wheel.bucket_angles]
    bucket_weights = water_wheel.bucket_weight

    display_surface.fill(slight_gray)

    next(water_wheel.water_wheel_generate())

    anchor_points = []
    for angle in bucket_angles:
        anchor_points.append([250 - 200 * math.sin(angle) - 20, 250 - 200 * math.cos(angle)])

    top_anchor_point = min(anchor_points[i][1] for i in range(bucket_num))
    text = pygame.font.SysFont('宋体', 50)

    for i in range(bucket_num):

        text_fmt = text.render(f'{i}', True,(0,0,0))
        display_surface.blit(text_fmt, anchor_points[i])

        water_line = bucket_weights[i]

        water_points = [(2 + anchor_points[i][0], 0 + anchor_points[i][1] + 35 - water_line), (38 + anchor_points[i][0], 0 + anchor_points[i][1] + 35 - water_line),
                        (34 + anchor_points[i][0], 36 + anchor_points[i][1]), (6 + anchor_points[i][0], 36 + anchor_points[i][1])]
        pygame.draw.polygon(display_surface, blue, water_points, 0)

        if anchor_points[i][1] == top_anchor_point:
            display_surface.blit(deep_red_bucket, anchor_points[i])
        else:
            display_surface.blit(deep_blue_bucket, anchor_points[i])

    pygame.draw.circle(display_surface, black, (250, 250), 3, 3)

    barycenter = [water_wheel.water_wheel_barycenter[0] * 3000 + 250, -water_wheel.water_wheel_barycenter[1] * 3000 + 250]
    barycenter_list.append(barycenter)

    if 2000 < count:
        for z in barycenter_list[count-2000:count]:
            pygame.draw.circle(display_surface, blue, z, 1, 1)
    else:
        for z in barycenter_list:
            pygame.draw.circle(display_surface, blue, z, 1, 1)

    mouse = pygame.mouse.get_pos()
    if 50 + 100 > mouse[0] > 50 and 550 + 50 > mouse[1] > 550:
        pygame.draw.rect(display_surface, slight_blue , (50, 550, 100, 50))
    else:
        pygame.draw.rect(display_surface, slight_red , (50, 550, 100, 50))

    if 250 + 100 > mouse[0] > 250 and 550 + 50 > mouse[1] > 550:
        pygame.draw.rect(display_surface, slight_blue , (250, 550, 100, 50))
    else:
        pygame.draw.rect(display_surface, slight_red , (250, 550, 100, 50))

    text_fmt = text.render(f'x1', True, (0, 0, 0))
    display_surface.blit(text_fmt, (75, 555))
    text_fmt = text.render(f'x10', True, (0, 0, 0))
    display_surface.blit(text_fmt, (255, 555))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and 50 < event.pos[0] < 50 + 100 and 550 < event.pos[1] < 550 + 50:
            outside_speed = 1
        if event.type == pygame.MOUSEBUTTONDOWN and 250 < event.pos[0] < 250 + 100 and 550 < event.pos[1] < 550 + 50:
            outside_speed = 10
        if event.type == pygame.QUIT:
            pygame.quit()
            # quit the program.
            quit()

    clock.tick(20 * outside_speed)
    pygame.display.flip()

