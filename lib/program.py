"""
Copyright 2021 crazygmr101

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import asyncio
import itertools
from typing import List, Tuple

import aiohttp
from PIL import ImageDraw, Image

from lib.models import BufferGeometry
from lib.url_build import build_bluemap_tile_url


async def get_json(root: str, x: int, z: int, session: aiohttp.ClientSession):
    url = build_bluemap_tile_url(root, x, z)
    async with session.get(url) as resp:
        content = await resp.read()
        print(f"{x},{z}: downloaded")
        return content


async def main(base_url: str, padding_amount: int, location: Tuple[int, int], output: str):
    x_range = location[0] // 512 - padding_amount, location[0] // 512 + padding_amount
    y_range = location[1] // 512 - padding_amount, location[1] // 512 + padding_amount

    tiles = list(itertools.chain(
        *([(x, y) for x in range(x_range[0], x_range[1] + 1)]
          for y in range(y_range[0], y_range[1] + 1))
    ))

    session = aiohttp.ClientSession()
    jsons = await asyncio.gather(*(get_json(base_url, x, z, session) for x, z in tiles))
    await session.close()

    buffers: List[BufferGeometry] = []

    for i in range(len(tiles)):
        x, z = tiles[i]
        print(f"\rRendering tile {i}/{len(tiles)}", end="")
        buffers.append(BufferGeometry.from_json(jsons[i]))

    print()

    min_x = min(tile[0] for tile in tiles)
    min_z = min(tile[1] for tile in tiles)
    max_x = (max(tile[0] for tile in tiles) - min_x) * 50
    max_z = (max(tile[1] for tile in tiles) - min_z) * 50

    img = Image.new("RGB", (max_x + 50, max_z + 50))
    draw = ImageDraw.Draw(img)

    for i in range(len(tiles)):
        print(f"\rAdding tile {i + 1}/{len(tiles)}", end="")
        x, z = tiles[i]
        correction_x = x * 50
        correction_y = z * 50

        for point, color in buffers[i].colors.items():
            new_x = point.x + correction_x - min_x * 50
            new_z = point.z + correction_y - min_z * 50
            if new_z < 0 or new_x < 0:
                print(new_x, new_z, point.x, point.z, correction_x, correction_y)
            else:
                draw.point((new_x, new_z),
                           fill=tuple(map(lambda x: int(x * 255), color.to_rgb())))
    print()
    with open(output, "xb") as fp:
        img.save(fp, format="PNG")
