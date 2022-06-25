import math
import matplotlib.pyplot as plt


def drawing_plots(angle1,angle2):
    t=len(angle1)
    plt.plot(angle1,t,label="Kąt 1")
    plt.plot(angle2, t, label="Kąt 2")
    plt.show
