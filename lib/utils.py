import json
from dataclasses import dataclass
from typing import List, Dict, Tuple

sign = lambda x: "-" if x < 0 else ""


def build_bluemap_tile_url(root: str, x: int, z: int) -> str:
    x_str = f"x{sign(x)}" + "/".join(str(abs(x)))
    z_str = f"z{sign(z)}" + "/".join(str(abs(z)))

    return f"{root}/data/world/lowres/{x_str}/{z_str}.json"

@dataclass
class Color:
    r: float
    g: float
    b: float

    def to_rgb(self) -> Tuple[float, float, float]:
        return self.r, self.g, self.b


@dataclass
class Point:
    x: float
    z: float

    def __hash__(self):
        return hash(f"{self.x}-{self.z}")

def parse_geo(js: str) -> Dict[Point, Color]:
    try:
        js = json.loads(js)
    except json.JSONDecodeError:
        return {}
    if "data" not in js:
        return {}

    geo_array = {}
    position_array: List[float] = js["data"]["attributes"]["position"]["array"]
    color_array: List[float] = js["data"]["attributes"]["color"]["array"]

    assert len(position_array) == len(color_array)

    for i in range(0, len(position_array), 3):
        geo_array[Point(position_array[i], position_array[i + 2])] = \
            Color(*color_array[i:i + 3])

    min_x = None
    max_x = None
    min_z = None
    max_z = None

    for point in geo_array.keys():
        if min_x is None or point.x < min_x:
            min_x = point.x
        if max_x is None or point.x > max_x:
            max_x = point.x
        if min_z is None or point.z < min_z:
            min_z = point.z
        if max_z is None or point.x > max_z:
            max_z = point.z

    return geo_array


