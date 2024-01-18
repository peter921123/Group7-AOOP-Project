import os

from config import *
from obstacles import box

class MapFactory():

    def __init__(self):
        print('MapFactory init')
        pass

    def create_map(self, map_type):
        map_path = os.path.join(os.path.dirname(__file__), f"..\..\map\map{map_type}.txt")
        with open(map_path, 'r') as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if char == 'b':
                    box.Box(x * grid_size, y * grid_size)