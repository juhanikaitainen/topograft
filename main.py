#!/usr/bin/env python3
import random
from queue import Queue
from typing import Optional

from draw import draw
from node import Color, Node


def main():
    LIMIT_X = 12
    LIMIT_Y = 12

    # Create starter node
    board = {}

    origin = Node()
    nodes = Queue()
    nodes.put(origin)

    # Generate a node to the right, and a node below
    while not nodes.empty():
        node = nodes.get()

        # Create a link to the tile on the board so we can easily look it up
        # later
        board[(node.x, node.y)] = node

        # Create the right node
        if node.x < LIMIT_X - 1:
            right_node = Node(node.x + 1, node.y)

            # Wire all the connections up (left, top left, top right)
            right_node.link(node, 'l')
            right_node.link(node.neighbor_path('tr'), 'tl')
            right_node.link(node.neighbor_path('tr.r'), 'tr')

            nodes.put(right_node)
        
        # Create the next node below - left if this new row is inset, right if
        # not (only created if we're at the beginning of the row)
        if node.x == 0 and node.y < LIMIT_Y - 1:
            bottom_node = Node(node.x, node.y + 1)

            if bottom_node.is_inset:
                bottom_node.link(node, 'tl')
                bottom_node.link(node.neighbor_path('r'), 'tr')
                bottom_node.link(node.neighbor_path('bl'), 'l')
            else:
                bottom_node.link(node, 'tr')
                bottom_node.link(node.neighbor_path('l'), 'tl')
                bottom_node.link(node.neighbor_path('l.bl'), 'l')

            nodes.put(bottom_node)

    print("Done generating, coloring map")

    nodes = Queue()

    # Color some random points
    for _ in range(0, 10):
        x = random.randint(0, LIMIT_X - 1)
        y = random.randint(0, LIMIT_Y - 1)

        n = board[(x,y)]
        n.color = random.choice([Color.OCEAN]) #, Color.SAND]) #Color.Grass])

        for neighbor in n.neighbors:
            nodes.put(neighbor)

    imgs = [draw(LIMIT_X, LIMIT_Y, board.values())]

    i = 0
    while not nodes.empty():
        node = nodes.get()
       
        if node.material:
            continue

        if node.set_material():
            if i % 5 == 0:
                imgs.append(draw(LIMIT_X, LIMIT_Y, board.values()))
            i += 1

        neighbors = node.neighbors
        random.shuffle(neighbors)

        for neighbor in neighbors:
            nodes.put(neighbor)

    imgs.append(draw(LIMIT_X, LIMIT_Y, board.values()))

    print(f"Writing out {len(imgs)} images")
    imgs[0].save('test.gif', save_all=True, append_images=imgs[1:], duration=20)


if __name__ == '__main__':
    main()