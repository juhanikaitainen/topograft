import math
from typing import List

from PIL import Image, ImageDraw

from node import Color


COLOR_TO_RGB = {
    Color.OCEAN:         (0x0F, 0x2C, 0xE8),
    Color.SHALLOW_WATER: (0x1D, 0x83, 0xFF),
    Color.SAND:          (0xF2, 0xD5, 0xBB),
    Color.GRASS:         (0x70, 0xA6, 0x1F),
    Color.TREE:          (0x64, 0x73, 0x2F)
}


def draw(x: int, y: int, nodes: List) -> Image:
    HEX_RADIUS = 4.0
    MARGIN = 0
    W = math.sqrt(3) * HEX_RADIUS
    H = 2 * HEX_RADIUS

    WIDTH = int(12 + (W + MARGIN) * (x + 0.5)) 
    HEIGHT = int(12 + (H + MARGIN) * (0.75 * y)) 

    img = Image.new('RGBA', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    for n in nodes:
        inset = 0.5 if n.is_inset else 0
        x = 12 + (W + MARGIN) * (n.x + inset)
        y = 12 + (H + MARGIN) * 0.75 * n.y

        fill = COLOR_TO_RGB.get(n.color, (0xFF, 0xFF, 0xFF))
        draw.regular_polygon((x, y, HEX_RADIUS), 6, rotation=90.0, fill=fill)

    return img