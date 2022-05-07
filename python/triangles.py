#!/usr/bin/env python3

from math import sqrt
import random
from queue import Queue
from typing import Set

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay


class Node:

    def __init__(self, x: float, y: float, height: float = 0.0, neighbors: Set = None):
        self.x = x
        self.y = y
        self.height = height

        self.neighbors = neighbors if neighbors else set()

    def __hash__(self) -> int:
        # TODO: Bad hashing here :)
        return int(self.x * 100000 + self.y)

    def __repr__(self):
        output = [f"Node({self.x:.02},{self.y:.02})"]

        neighbors = [f"Node({n.x:.02},{n.y:.02})" for n in self.neighbors]
        if neighbors:
            output.append(' -> ' + ', '.join(neighbors))
        
        return ''.join(output)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        return False

    def distance(self, other) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def add_neighbors(self, *neighbors):
        for neighbor in neighbors:
            if neighbor == self:
                continue

            self.neighbors.add(neighbor)


def main():
    points = np.asarray([(random.random()*10, random.random()*10) for _ in range(0, 2000)])

    tri = Delaunay(points)

    nodes = [Node(*p) for p in points]

    # Build a graph from the simplices
    for s in tri.simplices:
        for p in s:
            for neighbor in s:
                if neighbor == p:
                    continue 
                nodes[p].add_neighbors(nodes[neighbor])
    
    # Center each node amongst its neighbors
    for n in nodes:
        n.x = sum([neighbor.x for neighbor in n.neighbors]) / len(n.neighbors)
        n.y = sum([neighbor.y for neighbor in n.neighbors]) / len(n.neighbors)
    
    # Could merge nodes that are still too close to each other

    # Add heights by selecting random nodes, randomizing parameters, and working
    # outwards from the chosen origin point(s)
    for origin in random.choices(nodes, k=50):

        max_distance = random.randint(1, 7) 
        ridge_length = random.randint(0, 8)

        origin_height = 0.5 + random.random() * .5
        if random.random() > 0.7:
            origin_height = 0.2

        trough_inversion = 1  #-1 if random.random() > 0.7 else 1

        calculate_height = lambda distance: (trough_inversion - (trough_inversion * distance / max_distance)) * origin_height

        q = Queue()
        q.put(origin)
        distances = {origin: 0}

        # Generate either a peak or a ridge of all the same heights
        node = random.choice(list(origin.neighbors))
        seen = set()
        for _ in range(ridge_length):
            # TODO: Should we restrict this to nodes we haven't seen?
            q.put(node)
            distances[node] = 0
            seen.add(node)

            options = list(node.neighbors - seen)
            if not options:
                break

            node = random.choice(options)

            # Could also look at the angle between the node we come from, this node, and the neighbors,
            # to find the arm with the greatest angle

        while not q.empty():
            n = q.get()

            distance = distances[n]
            if distance > max_distance:
                continue

            n.height = calculate_height(distance)

            # Add the neighbor only if we haven't seen it (added its distance from the origin)
            for neighbor in n.neighbors:
                if neighbor in distances:
                    continue

                distances[neighbor] = distance + 1
                q.put(neighbor)


    for node in nodes:
        for neighbor in node.neighbors:
            if abs(node.height - neighbor.height) <= 0.05 and not (
                   node.height <= 0 and neighbor.height > 0
                   or node.height > 0 and neighbor.height <= 0 
            ):  # Close enough
                color = (1.0 - node.height,) * 3
                if node.height <= 0:
                    color = (-node.height, -node.height, 1.0)
                elif 0 < node.height < 0.20:
                    color = (0.0, 1.0 - node.height, 0.0) 

                plt.plot((neighbor.x, node.x), (neighbor.y, node.y), color=color)

    """
        if node.height == 0.0:
            plt.plot(node.x, node.y, marker=".", markersize=8, color=(0,0,1))
        else:
            plt.plot(node.x, node.y, marker=".", markersize=8, color=((1-node.height),)*3)
    """

    """
    # Choose a random point that isn't on the edge
    # Find the simplices that contain it
    for i in range(0, 3):  # Add lakes
        p = choice(range(0, len(tri.points)))
        s = []
        for simplex in tri.simplices:
            if p in simplex:
                s.append(simplex)
        
        plt.triplot(points[:,0], points[:,1], s, color='red')
    """

    plt.gca().set_aspect("equal")
    plt.show() #savefig("graph.png")


if __name__ == '__main__':
    main()