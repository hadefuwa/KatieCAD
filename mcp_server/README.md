# KatieCAD MCP server

Lets an MCP client (Claude) draw in a running KatieCAD window.

1. `pip install -r requirements.txt` (Python 3.10+)
2. Start KatieCAD with the bridge enabled: `python main.py --bridge`
   (or `KATIECAD_BRIDGE=1`). It listens on 127.0.0.1:8765 only
   (`KATIECAD_BRIDGE_PORT` to change). Without the flag nothing is opened.
3. Register the server, e.g. in `.mcp.json`:

```json
{
  "mcpServers": {
    "katiecad": {
      "command": "python",
      "args": ["mcp_server/katiecad_mcp.py"]
    }
  }
}
```

Tools: `get_info`, `draw_line`, `draw_circle`, `draw_rectangle`, `draw_arc`,
`draw_polyline`, `draw_text`, `list_elements`, `delete_elements`, `undo`,
`zoom_extents`, `screenshot`. Units are the drawing unit (mm), angles in degrees.
Every change goes through the normal undo history.
