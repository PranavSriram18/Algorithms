import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

if __name__=="__main__":
    # Parameters
    N = 100  # Number of ants
    T = 20000  # Number of timesteps

    # Step 1: Read the data
    data = np.loadtxt('out.txt').reshape(T, N, 2)  # Reshape to (timesteps, ants, xy)

    # Step 2: Set up the plot
    fig, ax = plt.subplots(facecolor='black')
    ax.set_facecolor('black')
    xdata, ydata = data[0, :, 0], data[0, :, 1]  # Initial positions of ants
    scat = ax.scatter(xdata, ydata, color='cyan')

    def init():
        ax.set_xlim(-1.5, 1.5)  # initial positions are in the range [-1, 1]
        ax.set_ylim(-1.5, 1.5)
        return scat,

    # Step 3: Create the animation
    def update(frame):
        xdata, ydata = data[frame, :, 0], data[frame, :, 1]
        scat.set_offsets(np.c_[xdata, ydata])
        return scat,

    ani = FuncAnimation(fig, update, frames=T, init_func=init, blit=True, interval=20)

    plt.show()
