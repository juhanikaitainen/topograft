#!/usr/bin/env python3

from random import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay


def main():
    points = []
    for _ in range(0, 20):
        points.append([random(), random()])

    points = np.array(points)

    tri = Delaunay(points)

    plt.triplot(points[:,0], points[:,1], tri.simplices)

    for i, s in enumerate(tri.simplices):
        print(f'Simplices ({i}): {s}')

        for n in tri.neighbors[i]:
            print(f'  neighbor: {tri.simplices[n]}')

        break

    #plt.show()



    


if __name__ == '__main__':
    main()