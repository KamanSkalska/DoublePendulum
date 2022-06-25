import math
import pygame
import Formular
from TextBox import TextBox
from TextInputBox import TextInputBox
from anglesPlot import drawing_plots

# dla ekranów full-HD i większych:
window_scaling = 1

# dla ekranów mniejszych (odkomentować poniższe):
# window_scaling /= 1.5

# initializing pygame values
w, h = 1920 // (1 / window_scaling), 1080 // (1 / window_scaling)
width = int(w)
height = int(h)
SIZE = (width, height)
pygame.init()
pygame.display.set_caption("Wahadło podwójne")
fps = 30
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# initializing initial parameters
init_mass = max(width // 48, 1)
mass1 = init_mass
mass2 = init_mass
length1 = max(int(width // 9.6), 1)
length2 = max(int(width // 9.6), 1)

angle1 = math.pi / 2
angle2 = math.pi / 2
angle_velocity1 = 0
angle_velocity2 = 0
angle_acceleration1 = 0
angle_acceleration2 = 0
Gravity = 8
scatter1 = []
scatter2 = []

angle1_list = []
angle2_list = []

LIST_LIMIT = 100

# COLORS
BACKGROUND = (20, 20, 20)
SCATTER_LINE_1 = (255, 255, 255)
SCATTER_LINE_2 = (255, 255, 0)
FIRST_POINT = (0, 255, 0)
SECOND_POINT = (0, 255, 255)
PENDULUM_ARM = (45, 140, 245)
ARM_STROKE = max(width // 120, 1)

scaling = max(width // 960, 1)

first_point_width = mass1 // scaling
second_point_width = mass2 // scaling

starting_point = (max(width // 2, 1), max(height // 3, 1))

x_offset = starting_point[0]
y_offset = starting_point[1]

# adding text fields
text_box_size = width // 8
dist_from_border = height // 100
font = pygame.font.Font(None, text_box_size // 4)
mass1_changer = TextInputBox(dist_from_border, dist_from_border, text_box_size,
                             font, "Masa 1", str(mass1))
mass2_changer = TextInputBox(dist_from_border + text_box_size, dist_from_border,
                             text_box_size, font, "Masa 2", str(mass2))
angle1_changer = TextInputBox(dist_from_border + 2 * text_box_size, dist_from_border,
                              text_box_size, font, "Kąt 1", str(round(angle1, 6)))
angle2_changer = TextInputBox(dist_from_border + 3 * text_box_size, dist_from_border,
                              text_box_size, font, "Kąt 2", str(round(angle2, 6)))
group = pygame.sprite.Group(mass1_changer,
                            mass2_changer,
                            angle1_changer,
                            angle2_changer)

# instructions
instructions1 = "Kliknij: \'r\' - restart z podanymi parametrami, " \
                "myszką na liczby - edytuj,"
instructions2 = "\'ENTER\' - przestań edytować, " \
                "\'s\' - zastopuj/odstopuj symulację"
instructions_box = TextBox(dist_from_border, height - (text_box_size - dist_from_border),
                           width - 2 * dist_from_border, font, instructions1, instructions2)

group.add(instructions_box)

run = True
stop = False
restart = False

try:
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
                        first_point_width = mass1 // scaling
                        second_point_width = mass2 // scaling
                    except ValueError:
                        mass1 = init_mass
                        mass2 = init_mass
                        angle_velocity1 = 0
                        angle_velocity2 = 0
                    finally:
                        angle_velocity1 = 0
                        angle_velocity2 = 0
                        angle_acceleration1 = 0
                        angle_acceleration2 = 0
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

            angle1_list.append(angle1)
            angle2_list.append(angle2)

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

except ValueError:
    print("Gdzies w kodzie program musial podzielic przez 0 - dlatego program sie wylaczyl")
finally:
    drawing_plots(angle1_list, angle2_list, fps)
