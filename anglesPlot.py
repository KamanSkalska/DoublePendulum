import math
import matplotlib.pyplot as plt


def drawing_plots(angle1, angle2, fps):
    t = list(range(0, len(angle1)))
    for i in range(len(angle1)):
        if angle1[i] > 10*math.pi or angle1[i] < -10*math.pi:
            angle1[i] %= 2*math.pi
        if angle2[i] > 10*math.pi or angle2[i] < -10*math.pi:
            angle2[i] %= 2*math.pi
        angle1[i] /= math.pi
        angle2[i] /= math.pi
    t = [i / fps for i in t]
    plt.plot(t, angle1, label="Kąt 1")
    plt.plot(t, angle2, label="Kąt 2")
    plt.xlabel("Czas")
    plt.ylabel("Wartość kąta w radianach")
    plt.legend()
    plt.show()
