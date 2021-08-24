import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Point:
    x: float
    z: float

    def __hash__(self):
        return hash(f"{self.x}-{self.z}")


@dataclass
class Color:
    r: float
    g: float
    b: float

    def to_rgb(self) -> Tuple[float, float, float]:
        return self.r, self.g, self.b


@dataclass
class BufferGeometry:
    @staticmethod
    def from_json(js: str) -> "BufferGeometry":
        try:
            js = json.loads(js)
        except json.JSONDecodeError:
            return BufferGeometry({})
        instance: BufferGeometry = BufferGeometry({})
        if "data" not in js:
            return BufferGeometry({})
        position_array: List[float] = js["data"]["attributes"]["position"]["array"]
        color_array: List[float] = js["data"]["attributes"]["color"]["array"]

        assert len(position_array) == len(color_array)

        for i in range(0, len(position_array), 3):
            instance.colors[Point(position_array[i], position_array[i + 2])] = \
                Color(*color_array[i:i + 3])

        min_x = None
        max_x = None
        min_z = None
        max_z = None

        for point in instance.colors.keys():
            if min_x is None or point.x < min_x:
                min_x = point.x
            if max_x is None or point.x > max_x:
                max_x = point.x
            if min_z is None or point.z < min_z:
                min_z = point.z
            if max_z is None or point.x > max_z:
                max_z = point.z

        return instance

    colors: Dict[Point, Color]
