import matplotlib.pyplot as plt
import argparse
import re

def plot_points(filename):
    # extract radius from filename
    radius = float(re.search(r'radius_(.*?)_trial', filename).group(1))
    
    # load the data
    points = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(float, line.strip().split())
            points.append((x, y))

    # plot the circle
    circle = plt.Circle((0, 0), radius, color='r', fill=False)
    fig, ax = plt.subplots()
    ax.add_artist(circle)

    # plot the points
    xs, ys = zip(*points)  # this separates the x and y coordinates
    plt.scatter(xs, ys, color='b', s=1)

    # set the aspect of the plot to be equal, so the circle isn't distorted
    ax.set_aspect('equal')
    ax.set_xlim(-radius-1, radius+1)
    ax.set_ylim(-radius-1, radius+1)

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot points on a circle.')
    parser.add_argument('filename', type=str, help='Input file name')
    args = parser.parse_args()

    plot_points(args.filename)

if __name__ == '__main__':
    main()
