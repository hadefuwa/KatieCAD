# -*- coding: utf-8 -*-
"""
katiecad/ui/tastenhilfe.py - Window "Keyboard shortcuts and commands" (F1).

The data part (`abschnitte`) needs no Tk. The command list is built from
core.BEFEHLE, so it always matches the program; `BESCHREIBUNG` gives every
command its text (a test checks that none is missing).
"""

import tkinter as tk
from tkinter import ttk

from katiecad.common.i18n import tr, SPRACHE
from katiecad.model.core import BEFEHLE
from katiecad.ui import tastenhilfe_es as ES

# --- Keys: (key, German, English) ------------------------------------------
TASTEN = [
    ("F1", "Diese Übersicht", "This overview"),
    ("F2", "Blatt-Eigenschaften (Name, Einbauort)", "Sheet properties (name, installation location)"),
    ("F3", "Objektfang ein/aus", "Object snap on/off"),
    ("F4", "Seitenleiste ein-/ausblenden", "Show / hide side bar"),
    ("F7", "Raster anzeigen ein/aus", "Show grid on/off"),
    ("F8", "Ortho ein/aus", "Ortho on/off"),
    ("F9", "Rasterfang ein/aus", "Grid snap on/off"),
    ("Esc", "Abbrechen / Auswahl aufheben", "Cancel / clear selection"),
    ("Entf", "Auswahl löschen", "Delete selection"),
    ("Strg+S", "Speichern (im Projekt ohne Nachfrage)", "Save (in a project without prompting)"),
    ("Strg+P", "Drucken", "Print"),
    ("Strg+Z", "Rückgängig", "Undo"),
    ("Strg+Y / Strg+Umschalt+Z", "Wiederholen", "Redo"),
    ("Strg+C", "Kopieren", "Copy"),
    ("Strg+Umschalt+C", "Kopieren mit Basispunkt", "Copy with base point"),
    ("Strg+X", "Ausschneiden", "Cut"),
    ("Strg+V", "Einfügen", "Paste"),
    ("Strg+D", "Duplizieren (mit Versatz)", "Duplicate (with offset)"),
    ("Strg+A", "Alles markieren", "Select all"),
    ("Strg+F", "Suchen und Ersetzen", "Find and replace"),
    ("Strg+B", "Block/Gerät einfügen (Blockauswahl)", "Insert block/device (block selection)"),
    ("Strg+1", "Eigenschaftenpalette", "Properties palette"),
    ("G", "Alles anzeigen (Zoom Grenzen)", "Show everything (zoom extents)"),
    ("Eingabe (leer)", "Werkzeug beenden: Polylinie/Wand/Raum abschließen, Auswahl bestätigen",
     "Finish tool: close polyline/wall/room, confirm selection"),
    ("Tab (Eingabezeile)", "Zwei Leerzeichen einfügen", "Insert two spaces"),
]

MAUS = [
    ("Linksklick", "Auswählen / Punkt setzen", "Select / pick point"),
    ("Linksklick ziehen", "Auswahlrahmen: links→rechts = ganz enthalten, rechts→links = berührt",
     "Selection window: left→right = fully inside, right→left = touching"),
    ("Doppelklick links", "Eigenschaften des Objekts", "Properties of the object"),
    ("Mausrad", "Zoomen (auf den Mauszeiger)", "Zoom (at the pointer)"),
    ("Mitteltaste ziehen", "Ansicht verschieben", "Pan the view"),
    ("Rechtstaste ziehen", "Ansicht verschieben", "Pan the view"),
    ("Rechtsklick", "Kontextmenü; beim Zeichnen: Werkzeug beenden", "Context menu; while drawing: finish tool"),
    ("Doppelklick Mitte/Rechts", "Alles anzeigen (Zoom Grenzen)", "Show everything (zoom extents)"),
]

# --- Commands (input line): function id -> (German, English) ---------------
BESCHREIBUNG = {
    "3d:abrunden": ("3D: Kanten abrunden", "3D: fillet edges"),
    "3d:aufloesen": ("3D: Körper auflösen", "3D: explode solid"),
    "3d:block": ("3D: Block aus Körper", "3D: block from solid"),
    "3d:drehen": ("3D: Körper drehen", "3D: rotate solid"),
    "3d:extrudieren": ("3D: Fläche extrudieren", "3D: extrude"),
    "3d:loch": ("3D: Loch / Bohrung", "3D: hole"),
    "3d:mass": ("3D: Maße", "3D: dimensions"),
    "3d:neu:kegel": ("3D: Kegel", "3D: cone"),
    "3d:neu:kugel": ("3D: Kugel", "3D: sphere"),
    "3d:neu:pyramide": ("3D: Pyramide", "3D: pyramid"),
    "3d:neu:quader": ("3D: Quader", "3D: box"),
    "3d:neu:schrank": ("3D: Schrank", "3D: cabinet"),
    "3d:neu:zylinder": ("3D: Zylinder", "3D: cylinder"),
    "3d:oeffnen": ("3D-Ansicht öffnen", "Open 3D view"),
    "3d:pivot": ("3D: Manipulator versetzen", "3D: move manipulator"),
    "3d:verschmelzen": ("3D: Körper verschmelzen", "3D: union"),
    "abrunden": ("Ecke abrunden", "Fillet"),
    "array": ("Reihe / Anordnung", "Array"),
    "attdef": ("Attributdefinition", "Attribute definition"),
    "attedit": ("Attribute bearbeiten", "Edit attributes"),
    "ausrichten2p": ("Ausrichten (2 Punkte)", "Align (2 points)"),
    "ausrichten:links": ("Objekte links ausrichten", "Align left"),
    "ausrichten:mitte_h": ("Objekte horizontal mittig ausrichten", "Align centres horizontally"),
    "ausrichten:mitte_v": ("Objekte vertikal mittig ausrichten", "Align centres vertically"),
    "ausrichten:oben": ("Objekte oben ausrichten", "Align top"),
    "ausrichten:rechts": ("Objekte rechts ausrichten", "Align right"),
    "ausrichten:unten": ("Objekte unten ausrichten", "Align bottom"),
    "bem:durchmesser": ("Durchmesserbemaßung", "Diameter dimension"),
    "bem:kette": ("Kettenbemaßung", "Continued dimension"),
    "bem:radius": ("Radiusbemaßung", "Radius dimension"),
    "bem:winkel": ("Winkelbemaßung (Bogen)", "Angular dimension (arc)"),
    "bem:winkel_linien": ("Winkelbemaßung (zwei Linien)", "Angular dimension (two lines)"),
    "blatt:neu": ("Neues Blatt", "New sheet"),
    "block:einfuegen": ("Block / Gerät einfügen", "Insert block / device"),
    "block:explode": ("Block auflösen", "Explode block"),
    "block:laden": ("Block aus Datei laden", "Load block from file"),
    "block:liste": ("Blockauswahl öffnen", "Open block selection"),
    "block:neu": ("Block erzeugen", "Create block"),
    "block:speichern": ("Block als Datei speichern", "Save block to file"),
    "copy": ("Kopieren (verschieben + Kopie)", "Copy"),
    "copybase": ("Kopieren mit Basispunkt", "Copy with base point"),
    "delete": ("Löschen", "Delete"),
    "druck": ("Drucken", "Print"),
    "fang": ("Rasterfang ein/aus", "Grid snap on/off"),
    "fase": ("Fase", "Chamfer"),
    "laenge": ("Länge ändern", "Lengthen"),
    "manip": ("Manipulator", "Manipulator"),
    "masstext": ("Maßtext ändern", "Change dimension text"),
    "matchprop": ("Eigenschaften übertragen", "Match properties"),
    "messen": ("Abstand messen", "Measure distance"),
    "mirror": ("Spiegeln", "Mirror"),
    "move": ("Verschieben", "Move"),
    "nummerieren": ("Geräte automatisch nummerieren", "Number devices automatically"),
    "ofang": ("Objektfang ein/aus", "Object snap on/off"),
    "ortho": ("Ortho ein/aus", "Ortho on/off"),
    "paste": ("Einfügen", "Paste"),
    "raster": ("Raster anzeigen ein/aus", "Show grid on/off"),
    "redo": ("Wiederholen", "Redo"),
    "rotate": ("Drehen", "Rotate"),
    "scale": ("Skalieren", "Scale"),
    "schnellauswahl": ("Schnellauswahl", "Quick select"),
    "stretch": ("Strecken", "Stretch"),
    "suchen": ("Suchen und Ersetzen", "Find and replace"),
    "tool:bemassung": ("Bemaßung", "Dimension"),
    "tool:bogen": ("Bogen", "Arc"),
    "tool:brechen": ("Brechen", "Break"),
    "tool:ellipse": ("Ellipse", "Ellipse"),
    "tool:fenster": ("Fenster in Wand", "Window in wall"),
    "tool:ftext": ("Funktionstext", "Function text"),
    "tool:klemme": ("Klemme", "Terminal"),
    "tool:kreis": ("Kreis", "Circle"),
    "tool:leitung": ("Leitung", "Wire"),
    "tool:linie": ("Linie", "Line"),
    "tool:maske": ("Betriebsmittelmaske", "Device mask"),
    "tool:polylinie": ("Polylinie", "Polyline"),
    "tool:querverweis": ("Querverweis", "Cross reference"),
    "tool:raum": ("Raum", "Room"),
    "tool:rechteck": ("Rechteck", "Rectangle"),
    "tool:spline": ("Spline", "Spline"),
    "tool:stutzen": ("Stutzen (Trim)", "Trim"),
    "tool:text": ("Text", "Text"),
    "tool:tuer": ("Tür in Wand", "Door in wall"),
    "tool:verbindung": ("Verbindung (Abzweig/Kreuzung)", "Junction"),
    "tool:vpunkt": ("Verbindungspunkt (Pin)", "Connection point (pin)"),
    "tool:wand": ("Wand", "Wall"),
    "undo": ("Rückgängig", "Undo"),
    "versatz": ("Versatz (Parallele)", "Offset"),
    "wand:schraffur": ("Wände schraffieren", "Hatch walls"),
    "wand:verbinden": ("Wände verbinden", "Join walls"),
    "zg": ("Alles anzeigen (Zoom Grenzen)", "Show everything (zoom extents)"),
}


def _taste(text, de):
    """Key names as on the keyboard of the UI language (`de`: True/"de", "en" or "es")."""
    if de is True or de == "de":
        return text
    if de == "es":
        for a, b in ES.TASTEN_NAMEN:
            text = text.replace(a, b)
        return text
    for a, b in (("Strg", "Ctrl"), ("Umschalt", "Shift"), ("Entf", "Del"),
                 ("Eingabe (leer)", "Enter (empty)"), ("Tab (Eingabezeile)", "Tab (input line)"),
                 ("Linksklick ziehen", "Left-drag"), ("Doppelklick links", "Double-click left"),
                 ("Doppelklick Mitte/Rechts", "Double-click middle/right"),
                 ("Linksklick", "Left click"), ("Rechtsklick", "Right click"),
                 ("Mausrad", "Mouse wheel"), ("Mitteltaste ziehen", "Middle-drag"),
                 ("Rechtstaste ziehen", "Right-drag")):
        text = text.replace(a, b)
    return text


def _de():
    """Language code of the UI (the parameter `de` of the functions below holds it)."""
    return SPRACHE["aktuell"]


def befehle_zeilen(de=None):
    """[(aliases text, description)] sorted by description."""
    de = _de() if de is None else de
    gruppen = {}
    for name, funktion in BEFEHLE.items():
        gruppen.setdefault(funktion, []).append(name)
    zeilen = []
    for funktion, namen in gruppen.items():
        if de == "es" and funktion in ES.BESCHREIBUNG:
            text = ES.BESCHREIBUNG[funktion]
        else:
            text = BESCHREIBUNG.get(funktion, (funktion, funktion))[0 if de in (True, "de") else 1]
        namen = sorted(set(namen), key=lambda n: (len(n), n))
        zeilen.append((" / ".join(namen), text))
    zeilen.sort(key=lambda z: z[1].lower())
    return zeilen


def abschnitte(de=None):
    """[(title, [(key, text)])] for the window."""
    de = _de() if de is None else de
    i = 1 if de in (True, "de") else 2

    def text(t):
        return ES.TASTEN.get(t[0], t[2]) if de == "es" else t[i]
    return [
        (tr("hilfe.tasten.tastatur"), [(_taste(t[0], de), text(t)) for t in TASTEN]),
        (tr("hilfe.tasten.maus"), [(_taste(t[0], de), text(t)) for t in MAUS]),
        (tr("hilfe.tasten.befehle"), befehle_zeilen(de)),
    ]


def zeige(app):
    """Opens the window (only one at a time, F1 again brings it to the front)."""
    alt = getattr(app, "_tastenhilfe", None)
    try:
        if alt is not None and alt.winfo_exists():
            alt.deiconify()
            alt.lift()
            alt.focus_force()
            return
    except tk.TclError:
        pass
    from katiecad.model.core import FARBEN
    win = tk.Toplevel(app.root)
    app._tastenhilfe = win
    win.title(tr("hilfe.tasten.titel") + " - KatieCAD")
    win.transient(app.root)
    win.configure(bg=FARBEN["bg_mittel"])
    win.geometry("640x560")
    win.minsize(420, 300)

    kopf = ttk.Frame(win, padding=(10, 10, 10, 4))
    kopf.pack(fill=tk.X)
    ttk.Label(kopf, text=tr("hilfe.tasten.suche")).pack(side=tk.LEFT)
    filter_var = tk.StringVar()
    eingabe = ttk.Entry(kopf, textvariable=filter_var)
    eingabe.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0))

    rahmen = ttk.Frame(win, padding=(10, 0, 10, 4))
    rahmen.pack(fill=tk.BOTH, expand=True)
    baum = ttk.Treeview(rahmen, columns=("taste", "text"), show="tree headings",
                        selectmode="browse")
    baum.heading("#0", text="")
    baum.heading("taste", text=tr("hilfe.tasten.spalte.taste"), anchor=tk.W)
    baum.heading("text", text=tr("hilfe.tasten.spalte.funktion"), anchor=tk.W)
    baum.column("#0", width=0, stretch=False)
    baum.column("taste", width=210, stretch=False)
    baum.column("text", width=380, stretch=True)
    sb = ttk.Scrollbar(rahmen, orient=tk.VERTICAL, command=baum.yview)
    baum.configure(yscrollcommand=sb.set)
    baum.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    baum.tag_configure("kopf", font=("TkDefaultFont", 10, "bold"))

    ttk.Label(win, text=tr("hilfe.tasten.hinweis"), style="Hint.TLabel",
              wraplength=600, justify=tk.LEFT, padding=(10, 0, 10, 10)).pack(fill=tk.X)

    def fuellen(*_):
        baum.delete(*baum.get_children())
        such = filter_var.get().strip().lower()
        for titel, zeilen in abschnitte():
            treffer = [z for z in zeilen
                       if not such or such in z[0].lower() or such in z[1].lower()]
            if not treffer:
                continue
            knoten = baum.insert("", tk.END, text="", values=(titel, ""),
                                 tags=("kopf",), open=True)
            for taste, text in treffer:
                baum.insert(knoten, tk.END, text="", values=(taste, text))

    filter_var.trace_add("write", fuellen)
    fuellen()
    win.bind("<Escape>", lambda e: win.destroy())
    win.bind("<F1>", lambda e: win.destroy())
    eingabe.focus_set()
