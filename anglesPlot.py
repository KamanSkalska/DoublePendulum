import math
import matplotlib.pyplot as plt


def float_pi_mod(num: float):
    return math.asin(math.sin(num))


def drawing_plots(angle1, angle2, fps):
    t = list(range(0, len(angle1)))
    for i in range(len(angle1)):
        if angle1[i] is float or angle2[i] is float:
            angle1[i] = 0
            angle2[i] = 0
        angle1[i] = float_pi_mod(angle1[i])
        angle2[i] = float_pi_mod(angle2[i])
    t = [i / fps for i in t]
    plt.plot(t, angle1, label="Kąt 1")
    plt.plot(t, angle2, label="Kąt 2")
    plt.xlabel("Czas")
    plt.ylabel("Wartość kąta w radianach")
    plt.legend()
    plt.show()
