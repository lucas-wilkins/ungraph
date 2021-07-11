from state import State


import matplotlib.pyplot as plt


def check(state: State):
    for xy in state.transformed_curve_points():
        plt.plot(xy[:,0], xy[:,1])
    plt.show()