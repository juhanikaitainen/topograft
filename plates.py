#!/usr/bin/env python3

import random

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d


def main():
    POINT_LIMIT = 50

    points = []
    for i in range(0, POINT_LIMIT):
        points.append([random.randint(0, 100), random.randint(0, 100)])

    points = np.array(points)

    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor, show_points=False, show_vertices=False)

    for ridge in random.choices(vor.ridge_vertices, k=25):
        a, b = ridge

        if a == -1 or b == -1:
            continue
            
        start = (vor.vertices[a][0], vor.vertices[b][0])
        end = (vor.vertices[a][1], vor.vertices[b][1])

        print(start, end)
        plt.plot(start, end, color='r', linestyle='-', linewidth=2)

    for region in random.choices(vor.regions, k=POINT_LIMIT // 3):
        xs = [vor.vertices[v][0] for v in region if v != -1]
        ys = [vor.vertices[v][1] for v in region if v != -1]

        plt.fill(xs, ys, 'b')

        plt.text(sum(xs) / len(xs), sum(ys) / len(ys), 'text')


    plt.show()


if __name__ == '__main__':
    main()