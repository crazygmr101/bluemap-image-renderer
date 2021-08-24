sign = lambda x: "-" if x < 0 else ""


def build_bluemap_tile_url(root: str, x: int, z: int) -> str:
    x_str = f"x{sign(x)}" + "/".join(str(abs(x)))
    z_str = f"z{sign(z)}" + "/".join(str(abs(z)))

    return f"{root}/data/world/lowres/{x_str}/{z_str}.json"
