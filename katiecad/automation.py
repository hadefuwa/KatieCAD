"""Local automation bridge: lets an external process (e.g. the MCP server in
mcp_server/) draw in the running KatieCAD window.

Opt-in: only started with `python main.py --bridge` or KATIECAD_BRIDGE=1.
Listens on 127.0.0.1 only (default port 8765, KATIECAD_BRIDGE_PORT to change).
Protocol: one JSON object per line, {"cmd": "...", ...args}; the reply is one
JSON line {"ok": true, ...} or {"ok": false, "error": "..."}.
All model changes run on the Tk main thread (via root.after polling).
"""
import base64
import io
import json
import os
import queue
import socketserver
import threading

from katiecad.electrical.logic import anschlusspunkte
from katiecad.model.blocks import block_laden
from katiecad.model.core import (BlockReferenz, Bogen, E_LINES, Kreis, Leitung,
                                 Linie, Polylinie, Rechteck, Text)

SYMBOL_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "symbols")

PORT = 8765


class _Bruecke:
    def __init__(self, app):
        self.app = app
        self.q = queue.Queue()
        self.befehle = {
            "ping": self.ping,
            "info": self.info,
            "draw_line": self.draw_line,
            "draw_circle": self.draw_circle,
            "draw_rectangle": self.draw_rectangle,
            "draw_arc": self.draw_arc,
            "draw_polyline": self.draw_polyline,
            "draw_text": self.draw_text,
            "list_symbols": self.list_symbols,
            "place_symbol": self.place_symbol,
            "get_pins": self.get_pins,
            "draw_wire": self.draw_wire,
            "list_elements": self.list_elements,
            "delete_elements": self.delete_elements,
            "undo": self.undo,
            "zoom_extents": self.zoom_extents,
            "screenshot": self.screenshot,
        }

    # ---- main-thread pump -------------------------------------------
    def pumpe(self):
        try:
            while True:
                req, antwort = self.q.get_nowait()
                try:
                    fn = self.befehle.get(req.get("cmd"))
                    if fn is None:
                        raise ValueError(f"unknown cmd {req.get('cmd')!r}")
                    res = fn(req)
                    antwort.put({"ok": True, **(res or {})})
                except Exception as e:
                    antwort.put({"ok": False, "error": f"{type(e).__name__}: {e}"})
        except queue.Empty:
            pass
        self.app.root.after(30, self.pumpe)

    def aufrufen(self, req, timeout=30):
        antwort = queue.Queue()
        self.q.put((req, antwort))
        try:
            return antwort.get(timeout=timeout)
        except queue.Empty:
            return {"ok": False, "error": "timeout waiting for the UI thread"}

    # ---- helpers -----------------------------------------------------
    def _add(self, el):
        self.app._snapshot()
        self.app._ziel_liste().append(el)
        self.app.redraw()
        return {"index": len(self.app._ziel_liste()) - 1}

    def _kw(self, r):
        kw = self.app._layer_daten()
        if r.get("layer"):
            if r["layer"] not in self.app.layers:
                raise ValueError(f"layer {r['layer']!r} does not exist")
            kw["layer"] = r["layer"]
            if not kw.get("eig_farbe"):
                kw["farbe"] = self.app.layers[r["layer"]].farbe
        if r.get("color"):
            kw["farbe"] = r["color"]
            kw["eig_farbe"] = True
        return kw

    # ---- commands ----------------------------------------------------
    def ping(self, r):
        return {"pong": True}

    def info(self, r):
        a = self.app
        return {"elements": len(a._ziel_liste()),
                "layers": list(a.layers.keys()),
                "active_layer": a.aktiver_layer.get(),
                "unit": a.einheit.get()}

    def draw_line(self, r):
        return self._add(Linie(r["x1"], r["y1"], r["x2"], r["y2"], **self._kw(r)))

    def draw_circle(self, r):
        return self._add(Kreis(r["cx"], r["cy"], r["r"], **self._kw(r)))

    def draw_rectangle(self, r):
        return self._add(Rechteck(r["x1"], r["y1"], r["x2"], r["y2"], **self._kw(r)))

    def draw_arc(self, r):
        return self._add(Bogen(r["cx"], r["cy"], r["r"], r["start"], r["end"],
                               **self._kw(r)))

    def draw_polyline(self, r):
        pts = [tuple(p) for p in r["points"]]
        if len(pts) < 2:
            raise ValueError("need at least 2 points")
        return self._add(Polylinie(pts, bool(r.get("closed", False)), **self._kw(r)))

    def draw_text(self, r):
        return self._add(Text(r["x"], r["y"], r["text"],
                              hoehe=r.get("height", 3.5),
                              winkel=r.get("angle", 0.0), **self._kw(r)))

    def _symbol_pfad(self, name):
        """'Category/Name' or just 'Name' (case-insensitive) -> file path."""
        name = name.replace("\\", "/").lower()
        if name.endswith(".katieblock"):
            name = name[:-len(".katieblock")]
        treffer = []
        for kat in sorted(os.listdir(SYMBOL_DIR)):
            kdir = os.path.join(SYMBOL_DIR, kat)
            if not os.path.isdir(kdir):
                continue
            for f in sorted(os.listdir(kdir)):
                if not f.endswith(".katieblock"):
                    continue
                stem = f[:-len(".katieblock")]
                if name in (stem.lower(), f"{kat}/{stem}".lower()):
                    treffer.append(os.path.join(kdir, f))
        if not treffer:
            raise ValueError(f"symbol {name!r} not found (see list_symbols)")
        if len(treffer) > 1:
            raise ValueError(f"symbol name {name!r} is ambiguous; use 'Category/Name'")
        return treffer[0]

    def list_symbols(self, r):
        out = []
        flt = (r.get("category") or "").lower()
        for kat in sorted(os.listdir(SYMBOL_DIR)):
            kdir = os.path.join(SYMBOL_DIR, kat)
            if not os.path.isdir(kdir) or (flt and flt not in kat.lower()):
                continue
            names = [f[:-len(".katieblock")] for f in sorted(os.listdir(kdir))
                     if f.endswith(".katieblock")]
            out.append({"category": kat, "symbols": names})
        return {"categories": out}

    def _pins(self, ref):
        return [{"name": a.name, "x": round(a.x, 3), "y": round(a.y, 3)}
                for a in anschlusspunkte([ref])]

    def place_symbol(self, r):
        a = self.app
        d = block_laden(self._symbol_pfad(r["name"]), a._dict_zu_element)
        a.block_bibliothek.setze(d, persistieren=False)
        a._snapshot()
        ref = BlockReferenz(r["x"], r["y"], d.name, d.elemente,
                            skalierung=r.get("scale", 1.0),
                            winkel=r.get("rotation", 0.0),
                            gespiegelt=bool(r.get("mirrored", False)),
                            layer=a._block_layer(d.elemente),
                            farbe=a.zeichenfarbe,
                            linientyp=a.linientyp.get(),
                            eig_farbe=a.eigene_farbe.get(),
                            staerke=a._staerke_neu())
        werte = r.get("values") or {}
        m = ref.geraet_maske()
        if m is not None:
            for k, v in werte.items():
                if k in m.werte:
                    m.werte[k] = str(v)
        ref.setze_attribute(werte)
        a._ziel_liste().append(ref)
        a.redraw()
        return {"index": len(a._ziel_liste()) - 1, "name": d.name,
                "pins": self._pins(ref)}

    def get_pins(self, r):
        liste = self.app._ziel_liste()
        el = liste[int(r["index"])]
        if not isinstance(el, BlockReferenz):
            raise ValueError("element is not a placed symbol")
        return {"pins": self._pins(el)}

    def draw_wire(self, r):
        pts = [tuple(p) for p in r["points"]]
        if len(pts) < 2:
            raise ValueError("need at least 2 points")
        a = self.app
        a._snapshot()
        layer = a._elektro_layer(E_LINES)
        liste = a._ziel_liste()
        for p, q in zip(pts, pts[1:]):
            liste.append(Leitung(p[0], p[1], q[0], q[1], layer=layer))
        a.redraw()
        return {"segments": len(pts) - 1}

    def list_elements(self, r):
        out = []
        for i, el in enumerate(self.app._ziel_liste()):
            d = {"index": i, "type": el.typ, "layer": el.layer}
            if isinstance(el, BlockReferenz):
                d["name"] = el.block_name
            try:
                d["bbox"] = [round(v, 3) for v in el.bbox()]
            except Exception:
                pass
            out.append(d)
        return {"elements": out}

    def delete_elements(self, r):
        liste = self.app._ziel_liste()
        idx = sorted(set(int(i) for i in r["indices"]), reverse=True)
        if any(i < 0 or i >= len(liste) for i in idx):
            raise ValueError("index out of range")
        self.app._snapshot()
        for i in idx:
            del liste[i]
        self.app.redraw()
        return {"deleted": len(idx)}

    def undo(self, r):
        self.app.undo()
        return {}

    def zoom_extents(self, r):
        self.app.zoom_grenzen()
        return {}

    def screenshot(self, r):
        from PIL import ImageGrab
        c = self.app.canvas
        root = self.app.root
        root.deiconify()
        root.lift()
        root.attributes("-topmost", True)      # screen grab needs it on top
        root.update()
        try:
            x, y = c.winfo_rootx(), c.winfo_rooty()
            img = ImageGrab.grab(bbox=(x, y, x + c.winfo_width(),
                                       y + c.winfo_height()))
        finally:
            root.attributes("-topmost", False)
        buf = io.BytesIO()
        img.save(buf, "PNG")
        return {"png_base64": base64.b64encode(buf.getvalue()).decode()}


def starten(app, port=PORT):
    bruecke = _Bruecke(app)

    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            for zeile in self.rfile:
                zeile = zeile.strip()
                if not zeile:
                    continue
                try:
                    req = json.loads(zeile)
                    res = bruecke.aufrufen(req)
                except Exception as e:
                    res = {"ok": False, "error": f"bad request: {e}"}
                self.wfile.write((json.dumps(res) + "\n").encode())

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    srv = Server(("127.0.0.1", port), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    app.root.after(30, bruecke.pumpe)
    print(f"[KatieCAD] automation bridge on 127.0.0.1:{port}")
    return srv
