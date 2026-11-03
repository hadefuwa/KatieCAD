# -*- coding: utf-8 -*-
"""Single-pole second representation: nothing is counted twice."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stub  # noqa: F401
import katiecad.common.i18n as katiecad_i18n; katiecad_i18n.SPRACHE["aktuell"] = "de"
import katiecad.model.core as core
import katiecad.electrical.logic as L
from katiecad.electrical import nummerierung as NU
from katiecad.electrical.pruefung import pruefe
from katiecad.reports import netz as N, daten as D, daten_listen as DL, daten_sps as DS
ok = 0


def check(c, m):
    global ok
    assert c, "FEHLER: " + m
    ok += 1


VP = core.Verbindungspunkt
nr = lambda i: i + 1


def geraet(x, y, ind, typ="", einpolig=False, rolle="haupt"):
    m = core.ElektroMaske(8, 0, rolle=rolle, einpolig=einpolig)
    sym = [core.Rechteck(-5, -5, 5, 5), VP(0, 5, wert="1", tag="P1"),
           VP(0, -5, wert="2", tag="P2"), m]
    b = core.BlockReferenz(x, y, "Sym", sym)
    b.attribute.update({"IND": ind, "TYP": typ, "PER": ""})
    return b


# ---- flag, helper, save / load -------------------------------------
a = geraet(0, 0, "-K1", "LC1D09")
e = geraet(50, 0, "-K1", "LC1D09", einpolig=True)
check(not core.ist_einpolig(a) and core.ist_einpolig(e), "ist_einpolig (Block)")
k = core.Klemme(0, 0, {"IND": "-X1", "NUM": "1"}, einpolig=True)
kb = core.Kabel(0, 0, {"CAB": "W1"}, einpolig=True)
mk = core.ElektroMaske(0, 0, {"IND": "-Q1"})
check(core.ist_einpolig(k) and core.ist_einpolig(kb) and not core.ist_einpolig(mk), "ist_einpolig (Klemme/Kabel/Maske)")
check("einpolig" not in mk.to_dict() and k.to_dict().get("einpolig") is True, "Speichern: Flag nur wenn gesetzt")
k2 = core.Klemme(**{x: y for x, y in k.to_dict().items() if x != "typ"})
check(k2.einpolig, "Laden: Flag bleibt")
check(core.ElektroMaske(**{x: y for x, y in
      core.ElektroMaske(0, 0, {"IND": "-Q1"}, einpolig=True).to_dict().items() if x != "typ"}).einpolig,
      "Laden: Maske")

# ---- device list / parts list: multi-pole + single-pole = once --------
blaetter = [(0, [a]), (1, [e])]
gl = D.geraeteliste(blaetter, nr, None, False, None)
check(len(gl) == 1 and gl[0]["anzahl"] == "1" and len(gl[0]["orte"]) == 1, f"Geraeteliste einmal: {gl}")
n = N.Netz.aufbauen(blaetter)
sl = DL.stueckliste(blaetter, nr, n)
check(len(sl) == 1 and sl[0]["anzahl"] == "1", f"Stueckliste einmal: {sl}")
# only single-pole drawn: never counted
check(D.geraeteliste([(0, [e])], nr, None, False, None) == [], "nur einpolig: nie gezaehlt")
# without the flag it would be counted twice
nb = [(0, [geraet(0, 0, "-K1", "LC1D09")]), (1, [geraet(50, 0, "-K1", "LC1D09")])]
check(D.geraeteliste(nb, nr, None, False, None)[0]["anzahl"] == "2", "Gegenprobe ohne Flag: 2")

# ---- check: no duplicate main symbol --------------------------------
check(not [f for f in pruefe([(0, "A", [a]), (1, "B", [e])]) if f.stufe == "fehler"], "Pruefung: kein Doppelt-Fehler")
check(sum(1 for f in pruefe([(0, "A", [a]), (1, "B", [geraet(0, 0, "-K1")])]) if f.stufe == "fehler") == 2,
      "Pruefung Gegenprobe: Fehler ohne Flag")
kl = [core.Klemme(0, 0, {"IND": "-X1", "NUM": "1"}), core.Klemme(30, 0, {"IND": "-X1", "NUM": "1"}, einpolig=True)]
check(not [f for f in pruefe([(0, "A", kl)]) if f.stufe == "fehler"], "Pruefung: Klemme einpolig kein Doppelt")

# ---- net / terminal plan / cables ----------------------------------
elem = [core.Klemme(0, 0, {"IND": "-X1", "NUM": "1"}),
        core.Klemme(30, 0, {"IND": "-X1", "NUM": "1"}, einpolig=True),
        core.Kabel(0, 40, {"CAB": "W1"}, einpolig=True)]
n2 = N.Netz.aufbauen([(0, elem)])
check(len(n2.klemmen) == 1 and not n2.kabel, f"Netz: Klemmen {len(n2.klemmen)}, Kabel {len(n2.kabel)}")

# ---- references: no cross references to the single-pole copy --------
h = geraet(0, 0, "-K1", rolle="haupt"); h.attribute["PER"] = "-K1"
hi = geraet(0, 50, "-K1", rolle="hilfs"); hi.attribute["PER"] = "-K1"
ez = geraet(80, 0, "-K1", einpolig=True); ez.attribute["PER"] = "-K1"
ez.refs = [(9, "A/1")]
g = L.geraete([h, hi, ez], 1)
check(len(g) == 2 and ez.refs == [], "geraete(): einpolig ausgenommen, refs geleert")
L.geraete_referenzen(g, 1, {})
check(h.refs and len(h.refs) == 1 and not ez.refs, "Referenzen ohne einpolige Kopie")

# ---- numbering: single-pole copy keeps its identifier -----------------
n1 = geraet(0, 0, "-K"); n1.attribute["IND"] = "-K"
n3 = geraet(40, 0, "-K", einpolig=True); n3.attribute["IND"] = "-K"
aend, _o = NU.plan([(0, [n1, n3])])
check(len(aend) == 1 and aend[0][3] == "-K1" and n3.attribute["IND"] == "-K", f"Nummerierung: {aend}")

# ---- from the sheet file (other sheets) ---------------------------------
dd = {"elemente": [{"typ": "block", "x": 0, "y": 0, "attribute": {"IND": "-K1", "PER": "-K1"},
                    "elemente": [{"typ": "maske", "rolle": "haupt", "einpolig": True}]},
                   {"typ": "block", "x": 0, "y": 0, "attribute": {"IND": "-K2", "PER": "-K2"},
                    "elemente": [{"typ": "maske", "rolle": "haupt"}]}]}
gb = L.geraete_aus_blattdaten(dd)
check(len(gb) == 1 and gb[0][2] == "-K2", f"Blattdatei: {gb}")

# ---- SPS list --------------------------------------------------------
check(DS.sps_liste(n, [(0, [e])], nr) == [], "SPS-Liste ignoriert einpolig")

# ---- pole count in the mask (own devices) --------------------------------
mp = core.ElektroMaske(0, 0, {"IND": "-F1"}, einpolig=True, pole="3+N")
texte = [e.inhalt for e in mp.aufgeloest(True)]
check("3+N" in texte, f"Polzahl sichtbar: {texte}")
mp2 = core.ElektroMaske(0, 0, {"IND": "-F1"}, einpolig=False, pole="3")
check(not [e for e in mp2.aufgeloest(True) if getattr(e, "inhalt", "") == "3"], "ohne Haekchen keine Polzahl")
check("pole" not in core.ElektroMaske(0, 0).to_dict() and mp.to_dict()["pole"] == "3+N", "Speichern: pole nur wenn gesetzt")
mp3 = core.ElektroMaske(**{x: y for x, y in mp.to_dict().items() if x != "typ"})
check(mp3.pole == "3+N" and mp3.einpolig, "Laden: pole")
bb = core.BlockReferenz(0, 0, "X", [core.Rechteck(-5, -5, 5, 5), mp])
check(core.ist_einpolig(bb) and bb.geraet_maske().pole == "3+N", "Block traegt Polzahl")

# ---- text positions of the mask survive "create device" / insertion ------------
md = core.ElektroMaske(8, 0, {"IND": "-F"}, einpolig=True, pole="3", versatz={"POLE": [-4.0, -2.0], "IND": [1.0, 0.0]})
def pos(ref, inhalt):
    for m in ref.aufgeloest():
        if isinstance(m, core.ElektroMaske):
            for e in m.aufgeloest(False):
                if getattr(e, "inhalt", None) == inhalt:
                    return (e.x, e.y)
bd = core.BlockReferenz(0, 0, "Sym", [core.Rechteck(-5, -5, 5, 5), md])
bd.attribute["IND"] = "-F"
frei = core.ElektroMaske(8, 0, {"IND": "-F"}, einpolig=True, pole="3")
bf = core.BlockReferenz(0, 0, "Sym", [core.Rechteck(-5, -5, 5, 5), frei]); bf.attribute["IND"] = "-F"
px, py = pos(bd, "3"); fx, fy = pos(bf, "3")
check(abs((px - fx) + 4.0) < 1e-6 and abs((py - fy) + 2.0) < 1e-6, f"Polzahl-Position aus Definition: {(px-fx, py-fy)}")
ix, iy = pos(bd, "-F"); jx, jy = pos(bf, "-F")
check(abs((ix - jx) - 1.0) < 1e-6, "IND-Position aus Definition")
bd.text_versatz["M:POLE"] = [0.0, 5.0]; bd._cache = None
qx, qy = pos(bd, "3")
check(abs(qx - fx) < 1e-6 and abs(qy - fy - 5.0) < 1e-6, "Instanz-Versatz ueberschreibt Definition")

# ---- project option "evaluate single-pole too" ---------------------------
core.EINPOLIG_MIT[0] = True
try:
    check(not core.ist_einpolig(e) and not core.ist_einpolig(k), "Option an: nichts ist ausgenommen")
    check(len(D.geraeteliste([(0, [e])], nr, None, False, None)) == 1, "Option an: nur einpolig wird gezaehlt")
    check(len(L.geraete_aus_blattdaten(dd)) == 2, "Option an: Blattdatei zaehlt beide")
    n4 = geraet(0, 0, "-K"); n4.attribute["IND"] = "-K"
    n5 = geraet(40, 0, "-K", einpolig=True); n5.attribute["IND"] = "-K"
    aend5, _o = NU.plan([(0, [n4, n5])])
    check(len(aend5) == 2, f"Option an: einpolige Geraete werden nummeriert: {aend5}")
    check(len(L.geraete([h, hi, ez], 1)) == 3, "Option an: geraete() mit einpoligem Geraet")
finally:
    core.EINPOLIG_MIT[0] = False
check(core.ist_einpolig(e) and len(L.geraete_aus_blattdaten(dd)) == 1, "Option aus: wie bisher")

print(f"OK ({ok} Pruefungen)")
