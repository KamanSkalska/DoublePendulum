import math
import random
import pygame
import Formular
from Point import Point
from TextBox import TextBox
from TextInputBox import TextInputBox

# initializing pygame values
width, height = 1920, 1080
SIZE = (width, height)
pygame.init()
pygame.display.set_caption("Double Pendulum")
fps = 30
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# initializing initial parameters
mass1 = 40
mass2 = 40
length1 = 200
length2 = 200

angle1 = math.pi/2
angle2 = math.pi/2
angle_velocity1 = 0
angle_velocity2 = 0
angle_acceleration1 = 0
angle_acceleration2 = 0
Gravity = 8
scatter1 = []
scatter2 = []

LIST_LIMIT = 100

# COLORS
BACKGROUND = (20, 20, 20)
SCATTER_LINE_1 = (255, 255, 255)
SCATTER_LINE_2 = (255, 255, 0)
FIRST_POINT = (0, 255, 0)
SECOND_POINT = (0, 255, 255)
PENDULUM_ARM = (45, 140, 245)
ARM_STROKE = 10

first_point_width = mass1 // 2
second_point_width = mass2 // 2

starting_point = (width//2, height//3)

x_offset = starting_point[0]
y_offset = starting_point[1]

# adding text fields
text_box_size = 220
dist_from_border = 20
font = pygame.font.Font(None, 50)
mass1_changer = TextInputBox(20, dist_from_border, text_box_size,
                             font, "Mass 1", str(mass1))
mass2_changer = TextInputBox(20 + text_box_size, dist_from_border,
                             text_box_size, font, "Mass 2", str(mass2))
angle1_changer = TextInputBox(20 + 2 * text_box_size, dist_from_border,
                              text_box_size, font, "Angle 1", str(round(angle1, 9)))
angle2_changer = TextInputBox(20 + 3 * text_box_size, dist_from_border,
                              text_box_size, font, "Angle 2", str(round(angle2, 9)))
group = pygame.sprite.Group(mass1_changer,
                            mass2_changer,
                            angle1_changer,
                            angle2_changer)

# instructions
instructions1 = "Click: \'r\' - restart and set chosen parameters, " \
                "right-click on box - edit params,"
instructions2 = "\'ENTER\' - stop editing, " \
                "\'s\' - stop the simulation"
instructions_box = TextBox(dist_from_border, 1080 - (text_box_size - dist_from_border),
                           text_box_size, font, instructions1, instructions2)

group.add(instructions_box)

run = True
stop = False
restart = False

while run:
    clock.tick(fps)

    screen.fill(BACKGROUND)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                try:
                    mass1 = float(mass1_changer.get_text())
                    mass2 = float(mass2_changer.get_text())
                    angle1 = float(angle1_changer.get_text())
                    angle2 = float(angle2_changer.get_text())
                except ValueError:
                    mass1 = 40
                    mass2 = 40
                    angle_velocity1 = 0
                    angle_velocity2 = 0
                finally:
                    angle1 = angle1
                    angle2 = angle2
                    angle_velocity1 = angle_velocity1
                    angle_velocity2 = angle_velocity2
                    angle_acceleration1 = angle_acceleration1
                    angle_acceleration2 = angle_acceleration2
                    scatter1 = []
                    scatter2 = []

            if event.key == pygame.K_s:
                stop = not stop

    group.update(event_list)

    x1 = float(length1 * math.sin(angle1) + x_offset)
    y1 = float(length1 * math.cos(angle1) + y_offset)

    x2 = float(x1 + length2 * math.sin(angle2))
    y2 = float(y1 + length2 * math.cos(angle2))

    if not stop:
        # calculate the acceleration
        angle_acceleration1 = Formular.FirstAcceleration(angle1, angle2, mass1, mass2,
                                                         length1, length2, Gravity,
                                                         angle_velocity1, angle_velocity2)
        angle_acceleration2 = Formular.SecondAcceleration(angle1, angle2, mass1, mass2,
                                                          length1, length2, Gravity,
                                                          angle_velocity1, angle_velocity2)

        # change velocities and angles
        angle_velocity1 += angle_acceleration1
        angle_velocity2 += angle_acceleration2
        angle1 += angle_velocity1
        angle2 += angle_velocity2

        # adding scattered points to list
        if len(scatter1) > LIST_LIMIT:
            scatter1.pop()
        if len(scatter2) > LIST_LIMIT:
            scatter2.pop()

    scatter1.insert(0, (x1, y1))
    scatter2.insert(0, (x2, y2))

    pygame.draw.line(screen, PENDULUM_ARM, starting_point, (x1, y1), ARM_STROKE)
    pygame.draw.circle(screen, (105, 90, 105), starting_point, 10)

    if len(scatter1) > 1:
        pygame.draw.lines(screen, SCATTER_LINE_1, False, scatter1, 1)
    if len(scatter2) > 1:
        pygame.draw.lines(screen, SCATTER_LINE_2, False, scatter2, 1)

    pygame.draw.line(screen, PENDULUM_ARM, (x1, y1), (x2, y2), ARM_STROKE)
    pygame.draw.circle(screen, FIRST_POINT, (int(x1), int(y1)), first_point_width)
    pygame.draw.circle(screen, SECOND_POINT, (int(x2), int(y2)), second_point_width)
    group.draw(screen)
    pygame.display.update()

pygame.quit()
