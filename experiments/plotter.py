import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import time
import re

def get_radius(filename):
    return float(re.search(r'radius_(.*?)_trial', filename).group(1))

def load_points(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(float, line.strip().split())
            points.append((x, y))
    return points


def plot_static(filename):
    # extract radius, load points
    radius = get_radius(filename)
    points = load_points(filename)
    
    # plot the circle
    circle = plt.Circle((0, 0), radius, color='r', fill=False)
    fig, ax = plt.subplots()
    ax.add_artist(circle)

    # plot the points
    xs, ys = zip(*points)  # this separates the x and y coordinates
    plt.scatter(xs, ys, color='b', s=1)

    # set the aspect of the plot to be equal
    ax.set_aspect('equal')
    ax.set_xlim(-radius-1, radius+1)
    ax.set_ylim(-radius-1, radius+1)

    plt.show()

def plot_dynamic(filename):
     # extract radius, load points
    radius = get_radius(filename)
    points = load_points(filename)

    plt.rcParams['figure.facecolor'] = 'black'

    # plot the circle
    fig, ax = plt.subplots()
    circle = plt.Circle((0, 0), radius, color='r', fill=False)
    ax.add_artist(circle)

    # prepare for scatter plot
    scatter = ax.scatter([], [], color='cyan', s=1)

    # set the aspect of the plot to be equal
    ax.set_aspect('equal')
    ax.set_facecolor('black')
    ax.set_xlim(-radius-1, radius+1)
    ax.set_ylim(-radius-1, radius+1)

    def update(num, points, scatter):
        if num == 1:
            plt.pause(5)
        scatter.set_offsets(points[:num+1])
        return scatter,

    ani = animation.FuncAnimation(fig, update, frames=len(points), fargs=[points, scatter],
                                  interval=10, blit=True, repeat=False)

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot points on a circle.')
    parser.add_argument('filename', type=str, help='Input file name')
    args = parser.parse_args()

    print("Preparing animation...")

    # Change from static to dynamic or vice versa as desired
    plot_dynamic(args.filename)

if __name__ == '__main__':
    main()
