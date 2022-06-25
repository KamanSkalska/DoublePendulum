import math
import matplotlib.pyplot as plt


def drawing_plots(angle1,angle2):
    t=list(range(0,len(angle1)))
    for i in range(0,len(angle1)):
        angle1[i]=angle1[i]/math.pi
        angle2[i] = angle2[i]/ math.pi
    plt.plot(t,angle1,label="Kąt 1")
    plt.plot(t,angle2, label="Kąt 2")
    plt.xlabel("Czas")
    plt.ylabel("Wartość kąta w radianach")
    plt.legend()
    plt.show()
