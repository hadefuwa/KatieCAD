"""MCP server for KatieCAD (stdio). Talks to a running KatieCAD started with
`python main.py --bridge` over 127.0.0.1 (KATIECAD_BRIDGE_PORT, default 8765).

Coordinates are in drawing units (mm by default); angles in degrees.
"""
import base64
import json
import os
import socket

from mcp.server.fastmcp import FastMCP, Image

PORT = int(os.environ.get("KATIECAD_BRIDGE_PORT", "8765"))
mcp = FastMCP("katiecad")


def _call(cmd, **args):
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=5) as s:
            s.settimeout(40)
            s.sendall((json.dumps({"cmd": cmd, **args}) + "\n").encode())
            buf = b""
            while not buf.endswith(b"\n"):
                chunk = s.recv(1 << 20)
                if not chunk:
                    break
                buf += chunk
    except OSError as e:
        raise RuntimeError(
            f"Cannot reach KatieCAD on port {PORT} ({e}). Start it with "
            "'python main.py --bridge'.")
    res = json.loads(buf)
    if not res.pop("ok", False):
        raise RuntimeError(res.get("error", "unknown error"))
    return res


def _style(layer, color):
    return {k: v for k, v in (("layer", layer), ("color", color)) if v}


@mcp.tool()
def get_info() -> dict:
    """Element count, layer names, active layer and unit of the open drawing."""
    return _call("info")


@mcp.tool()
def draw_line(x1: float, y1: float, x2: float, y2: float,
              layer: str = "", color: str = "") -> dict:
    """Draw a line. `color` is an optional hex colour like '#ff0000'."""
    return _call("draw_line", x1=x1, y1=y1, x2=x2, y2=y2, **_style(layer, color))


@mcp.tool()
def draw_circle(cx: float, cy: float, r: float,
                layer: str = "", color: str = "") -> dict:
    """Draw a circle from centre and radius."""
    return _call("draw_circle", cx=cx, cy=cy, r=r, **_style(layer, color))


@mcp.tool()
def draw_rectangle(x1: float, y1: float, x2: float, y2: float,
                   layer: str = "", color: str = "") -> dict:
    """Draw an axis-aligned rectangle from two opposite corners."""
    return _call("draw_rectangle", x1=x1, y1=y1, x2=x2, y2=y2, **_style(layer, color))


@mcp.tool()
def draw_arc(cx: float, cy: float, r: float, start: float, end: float,
             layer: str = "", color: str = "") -> dict:
    """Draw an arc from centre, radius and start/end angle in degrees."""
    return _call("draw_arc", cx=cx, cy=cy, r=r, start=start, end=end,
                 **_style(layer, color))


@mcp.tool()
def draw_polyline(points: list[list[float]], closed: bool = False,
                  layer: str = "", color: str = "") -> dict:
    """Draw a polyline through [[x, y], ...] (at least 2 points)."""
    return _call("draw_polyline", points=points, closed=closed, **_style(layer, color))


@mcp.tool()
def draw_text(x: float, y: float, text: str, height: float = 3.5,
              angle: float = 0.0, layer: str = "", color: str = "") -> dict:
    """Place text with its lower-left corner at (x, y)."""
    return _call("draw_text", x=x, y=y, text=text, height=height, angle=angle,
                 **_style(layer, color))


@mcp.tool()
def list_symbols(category: str = "") -> dict:
    """List the electrical symbol library (contactors, relays, fuses, motors,
    switches, ...) by category. `category` filters by substring."""
    return _call("list_symbols", category=category)


@mcp.tool()
def place_symbol(name: str, x: float, y: float, rotation: float = 0.0,
                 scale: float = 1.0, mirrored: bool = False,
                 values: dict[str, str] | None = None) -> dict:
    """Place a library symbol (name from list_symbols, optionally
    'Category/Name'). Symbols are vertical by default with ~5 mm pole pitch.
    `values` fills the device mask, e.g. {"IND": "K1", "TYP": "LC1D09"}.
    Returns the element index and the absolute pin positions; pins that touch
    other pins get wired automatically."""
    return _call("place_symbol", name=name, x=x, y=y, rotation=rotation,
                 scale=scale, mirrored=mirrored, values=values or {})


@mcp.tool()
def get_pins(index: int) -> dict:
    """Absolute pin positions of a placed symbol (index from list_elements)."""
    return _call("get_pins", index=index)


@mcp.tool()
def draw_wire(points: list[list[float]]) -> dict:
    """Draw an electrical wire through [[x, y], ...]; use pin positions from
    place_symbol/get_pins as end points."""
    return _call("draw_wire", points=points)


@mcp.tool()
def list_elements() -> dict:
    """List elements (index, type, layer, bounding box) in the active space."""
    return _call("list_elements")


@mcp.tool()
def delete_elements(indices: list[int]) -> dict:
    """Delete elements by index (see list_elements)."""
    return _call("delete_elements", indices=indices)


@mcp.tool()
def undo() -> dict:
    """Undo the last change."""
    return _call("undo")


@mcp.tool()
def zoom_extents() -> dict:
    """Zoom the view to show the whole drawing."""
    return _call("zoom_extents")


@mcp.tool()
def screenshot() -> Image:
    """Screenshot of the drawing canvas (PNG)."""
    return Image(data=base64.b64decode(_call("screenshot")["png_base64"]),
                 format="png")


if __name__ == "__main__":
    mcp.run()
