import random
from enum import Enum
from queue import Queue
from typing import List, Optional


class Color(Enum):
    OCEAN = 1
    SHALLOW_WATER = 2
    SAND = 3
    GRASS = 4
    TREE = 5


COLOR_POSSIBILITIES = {
    Color.OCEAN: {
        Color.OCEAN: 5,
        Color.SHALLOW_WATER: 2
    },
    Color.SHALLOW_WATER: {
        Color.SAND: 1,
        Color.SHALLOW_WATER: 3
    },
    Color.SAND: {
        Color.SAND: 3,
        Color.GRASS: 1
    },
    Color.GRASS: {
        Color.GRASS: 3,
        Color.SAND: 0,
    } 
}


class Node():

    # Maps relationships to their inverses
    RELATIONSHIPS = {
        'tl': 'br',
        'tr': 'bl',
        'l': 'r',
        'r': 'l',
        'br': 'tl',
        'bl': 'tr'
    }

    def __init__(self, x: int = 0, y: int = 0):
        self.material = None
        self.tl = self.tr = self.l = self.r = self.bl = self.br = None

        self.x = x
        self.y = y

    @property
    def neighbors(self) -> List:
        output = []
        for r in self.RELATIONSHIPS:
            neighbor = getattr(self, r)
            if neighbor is not None:
                output.append(neighbor)
        return output

    @property
    def is_inset(self) -> bool:
        return self.y % 2 != 0
    
    def neighbor_path(self, path: str):
        """Given a path like "l.tl", breaks it apart and returns the `Node` at
        the end of the path, or `None` if no node exists.
        
        Raises `ValueError` if an entry in the path isn't a valid node
        direction.
        """
        n = self
        for step in path.split('.'):
            if step not in self.RELATIONSHIPS.keys():
                raise ValueError("Invalid step name: %s", step)
            
            n = getattr(n, step)
            if n is None:
                break
                
        return n
    
    def link(self, neighbor, relationship: str):
        """Links this node to the neighbor with the given `relationship`, such
        as "tl", "l", etc. The neighbor is linked with the inverse relationship,
        such as "br", "r", etc.
        """
        if relationship not in self.RELATIONSHIPS:
            raise ValueError("%s is not a valid relationship", relationship)
        
        if neighbor is None:
            return
        
        setattr(self, relationship, neighbor)

        inverse_relationship = self.RELATIONSHIPS.get(relationship)
        setattr(neighbor, inverse_relationship, self)
    
    def set_material(self, value = None) -> bool:
        """Color in a node, either by setting it to `value` or determining the
        color based on the neighboring nodes.
        """
        if self.material is not None:
            return False

        if value is not None:
            self.material = value
            return True

        possibilities = {}
        for rel in self.RELATIONSHIPS.keys():
            neighbor = getattr(self, rel)
            if neighbor is not None and neighbor.color is not None:
                possibilities.update(COLOR_POSSIBILITIES.get(neighbor.color))
        
        if possibilities:
            m = sum(possibilities.values())
            c = random.randint(0, m - 1)

            total = 0
            for color, v in possibilities.items():
                total += v
                if total > c:
                    break
            
            self.material = color
        
        return self.material is not None
