import math

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def normalize_neg(data):
    return 2 * normalize(data) - 1


def main():
    fig = plt.figure()

    MAX_DISTANCE = 100
    TIMER = 10

    TIME_COEF = 0.01

    X = np.arange(0, MAX_DISTANCE + 1, 1)
    Y = np.arange(0, TIMER + 1, 1)
    X, Y = np.meshgrid(X, Y)

    attacker_reward = MAX_DISTANCE - X
    attacker_reward = normalize(attacker_reward)

    defender_reward = normalize(TIMER - Y)

    plot_attacker(fig, X, Y, attacker_reward)
    plot_defender(fig, X, Y, defender_reward)

    plt.show()


def plot_attacker(fig, X, Y, reward):
    ax = fig.add_subplot(1, 2, 1, projection="3d")

    # Plot the surface.
    surf = ax.plot_surface(
        X, Y, reward, cmap="coolwarm", linewidth=1, edgecolor="black"
    )

    # Customize the z axis.
    ax.set_xlabel("Distance")
    ax.set_ylabel("time left")
    ax.set_zlabel("reward")
    ax.set_title("attacker")

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)


def plot_defender(fig, X, Y, reward):
    ax = fig.add_subplot(1, 2, 2, projection="3d")
    # Plot the surface.
    surf = ax.plot_surface(
        X, Y, reward, cmap="coolwarm", linewidth=1, edgecolor="black"
    )

    ax.set_xlabel("Distance")
    ax.set_ylabel("time left")
    ax.set_zlabel("reward")
    ax.set_title("defender")

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)


def euclidian_distance(x_vector: np.Array, y_vector: np.Array):
    """ Computes the euclidian distance between two points

    Args:
        x_vector (np.Array): array of the 
        y_vector (np.Array): [description]

    Returns:
        [type]: [description]
    """
    distance = math.sqrt(sum([(x - y) ** 2 for x, y in zip(x_vector, y_vector)]))
    return distance


if __name__ == "__main__":
    u = np.array([0, 0])
    v = np.array([])
