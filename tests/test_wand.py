import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import stub  # noqa: F401
import katiecad.common.i18n as I; I.SPRACHE["aktuell"] = "de"
import katiecad.model.core as core
from katiecad.model.core import Wand, Oeffnung, wand_verknuepfen, wand_in_linien
import katiecad.fileio.pdf as PDF
ok = 0
def check(c, m):
    global ok
    assert c, "FEHLER: " + m
    ok += 1

w = Wand([(0, 0), (4000, 0), (4000, 3000)], dicke=240)
check(w.typ == "wand" and isinstance(w, core.Polylinie), "Wand ist Polylinie-Unterklasse")
n0 = len(w.prims())
t = Oeffnung("tuer", 1500, 10, 0.0, dicke=240)          # slightly beside the line: still in the wall
f = Oeffnung("fenster", 4000, 1500, 90.0, dicke=240)
wand_verknuepfen([w, t, f])
check(len(w._luecken) == 1, "nur die Tuer schneidet eine Luecke")
check(abs(t._lage()[0] - 1500) < 1e-9 and abs(t._lage()[1]) < 1e-9, "Tuer richtet sich auf die Mittellinie aus")
check(t.dicke == 240 and abs(t.winkel) < 1e-9 and abs(f.winkel - 90) < 1e-9, "Winkel/Dicke aus der Wand")
innen = [pl for pl, _c in w.prims() if len(pl) == 2 and abs(pl[0][1] - 120) < 1e-6
         and abs(pl[1][1] - 120) < 1e-6 and pl[0][0] < 1500 < pl[1][0]]
check(not innen, "Wandkante ist in der Tuer unterbrochen")
xs = [p[0] for pl, _c in w.prims() for p in pl]
check(min(xs) == 0.0 and max(xs) == 4120.0, "Ausdehnung mit Gehrungsecke")
# moving the door: the wall follows (door is a normal object)
t.verschieben(1000, 0)
wand_verknuepfen([w, t, f])
check(abs(t._lage()[0] - 2500) < 1e-9 and abs(w._luecken[0][1] - (2500 - 505) / 4000) < 1e-9, "Tuer verschoben -> Luecke wandert")
# door outside the wall: no gap, free symbol
t.verschieben(0, 1000)
wand_verknuepfen([w, t])
check(w._luecken == [] and t._geo is None, "Tuer ausserhalb: keine Luecke, freies Symbol")
check(len(t.prims()) == 4, "Tuer: 2 Laibungen, Blatt, Bogen")
check(len(f.prims()) == 4, "Fenster: 2 Laibungen + 2 Glaslinien")
# flags: hinge and swing
a = Oeffnung("tuer", 0, 0, 0.0, breite=1000, dicke=200)
def blatt(o):
    return o.prims()[2][0]
b0 = blatt(a)
a.spiegeln = True; b1 = blatt(a)
check(b0[0][0] == -500 and b1[0][0] == 500 and b0[1][1] == b1[1][1], "Scharnier spiegeln: andere Seite, gleicher Aufschlag")
a.spiegeln = False; a.umkehren = True; b2 = blatt(a)
check(b2[1][1] < 0 < b0[1][1], "Aufschlag umkehren: andere Wandseite")
# grips
a.griff_bewegen("w2", 700, 0)
check(abs(a.breite - 1400) < 1e-9, "Endgriff aendert die Breite")
a.griff_bewegen("c", 50, 60)
check((a.x, a.y) == (50, 60), "Mittelgriff verschiebt")
# serialization (runtime fields must not be saved)
for el in (w, t, f):
    d = json.loads(json.dumps(el.to_dict()))
    check("_luecken" not in d and "_geo" not in d, "keine Laufzeitdaten in to_dict")
d = json.loads(json.dumps(t.to_dict())); d.pop("typ")
t2 = Oeffnung(**d)
check(t2.breite == t.breite and t2.art == "tuer", "Oeffnung Rekonstruktion")
d = json.loads(json.dumps(w.to_dict())); d.pop("typ")
check(len(Wand(**d).prims()) == n0, "Wand Rekonstruktion")
# scale / mirror via the registered transforms
w4 = Wand([(0, 0), (1000, 0)], dicke=100); w4.skalieren(0, 0, 2.0)
check(w4.dicke == 200, "Wand skalieren")
o4 = Oeffnung("tuer", 500, 0, 0.0); sb = o4.breite
o4.skalieren(0, 0, 2.0); check(abs(o4.breite - 2 * sb) < 1e-9 and o4.x == 1000, "Oeffnung skalieren")
um = o4.umkehren
core._sp_oeffnung(o4, 0, 0, 1, 0); check(o4.umkehren != um and o4.winkel == 0.0, "Oeffnung spiegeln kehrt Aufschlag um")
# closed wall
wc = Wand([(0, 0), (3000, 0), (3000, 2000), (0, 2000)], geschlossen=True, dicke=200)
check(sum(1 for _p, cl in wc.prims() if cl) == 2, "Geschlossene Wand: innere und aeussere Kontur")
# alignment
wl = Wand([(0, 0), (1000, 0)], dicke=200, ausrichtung="links")
ys = sorted({round(p[1]) for pl, _c in wl.prims() for p in pl})
check(ys == [-200, 0] or ys == [0, 200], f"Ausrichtung links: {ys}")
# pdf prims
for el in (w, t):
    pp = PDF._prims(el, 1.0, 1.0, False)
    check(len(pp) == len(el.prims()) and all(p[0] == "l" for p in pp), "PDF-Primitive")
# blocks: plain lines
w5 = Wand([(0, 0), (4000, 0)], dicke=240); t5 = Oeffnung("tuer", 2000, 0, 0.0)
bl = wand_in_linien([w5, t5])
check(all(type(e) is core.Polylinie for e in bl) and len(bl) > 4, "Block aus Wand + Tuer: einfache Polylinien")
# hit test
check(w.punkt_im_koerper(2000, 100) and not w.punkt_im_koerper(2000, 500), "Klick auf Wandkoerper")
check(t5.trifft(2000, 0) and not t5.trifft(2000, 500), "Klick in die Tuer")
# ---- hatch ----
hw = Wand([(0, 0), (3000, 0)], dicke=240, schraffur="schraeg", schraffur_abstand=60)
n_k = len(hw.prims(schraffur=False)); n_s = len(hw.prims())
check(n_s > n_k + 20, "Schraffur erzeugt Linien")
for pl, _c in hw.prims()[n_k:]:
    for (x, y) in pl:
        assert -1e-6 <= x <= 3000 + 1e-6 and -120 - 1e-6 <= y <= 120 + 1e-6, "Schraffur ausserhalb"
check(True, "Schraffur bleibt im Wandkoerper")
kw = Wand([(0, 0), (3000, 0)], dicke=240, schraffur="kreuz", schraffur_abstand=60)
check(len(kw.prims()) > len(hw.prims()), "Kreuzschraffur hat mehr Linien")
check(len(Wand([(0, 0), (3000, 0)]).prims()) == n_k, "ohne Schraffur nur Kontur")
# door gap: no hatch line inside the gap
hd = Wand([(0, 0), (3000, 0)], dicke=240, schraffur="schraeg", schraffur_abstand=40)
hd2 = Oeffnung("tuer", 1500, 0, 0.0, breite=1000)
wand_verknuepfen([hd, hd2])
for pl, _c in hd.prims()[len(hd.prims(schraffur=False)):]:
    assert not (max(p[0] for p in pl) > 1000 + 1e-6 and min(p[0] for p in pl) < 2000 - 1e-6), "Schraffur in der Tuerluecke"
check(True, "keine Schraffur in der Tuerluecke")
d = json.loads(json.dumps(hw.to_dict())); d.pop("typ")
check(Wand(**d).schraffur == "schraeg" and Wand(**d).schraffur_abstand == 60, "Schraffur wird gespeichert")
# ---- join ----
a = Wand([(0, 0), (3000, 0)], dicke=240); b = Wand([(3100, 50), (3100, 2000)], dicke=240)
r = core.wand_verbinden(a, b)
check(isinstance(r, dict) and r["punkte"] == [(0, 0), (3100, 0), (3100, 2000)] or
      [tuple(round(c, 3) for c in p) for p in r["punkte"]] == [(0, 0), (3100, 0), (3100, 2000)], "Verbinden: Ecke am Schnittpunkt")
check(not r["rev_a"] and not r["rev_b"], "Verbinden: keine Umkehrung noetig")
c = Wand([(3100, 2000), (3100, 50)], dicke=240)          # drawn the other way round
r2 = core.wand_verbinden(a, c)
check(r2["rev_b"] and not r2["rev_a"], "Verbinden: B wird umgedreht")
r3 = core.wand_verbinden(Wand([(3000, 0), (0, 0)], dicke=240, ausrichtung="links"), b)
check(r3["rev_a"] and r3["ausrichtung"] == "rechts", "Verbinden: A umgedreht tauscht die Lage")
g = Wand([(3150, 0), (6000, 0)], dicke=240)
rg = core.wand_verbinden(a, g)
check([round(p[0]) for p in rg["punkte"]] == [0, 3000, 3150, 6000], "Verbinden gerade (Parallele mit kleiner Luecke)")
check(core.wand_verbinden(a, a) == "gleich", "Verbinden: gleiche Wand")
check(core.wand_verbinden(a, Wand([(0, 0), (1, 0), (1, 1)], geschlossen=True)) == "geschlossen", "Verbinden: geschlossen")
check(core.wand_verbinden(a, Wand([(0, 9000), (3000, 9000)])) == "parallel", "Verbinden: parallel und weit weg")
check(core.wand_verbinden(a, Wand([(9000, 5000), (9000, 6000)])) == "zu_weit", "Verbinden: zu weit")
# the joined wall is one outline with a mitred outer corner
m = Wand(r["punkte"], dicke=240)
check(not any(len(pl) == 2 and abs(pl[0][0] - 3100) < 1e-6 and abs(pl[1][0] - 3100) < 1e-6
              and abs(pl[0][1]) < 1e-6 for pl, _c in m.prims()), "keine Endkappe mehr in der Ecke")
# ---- fill, windows, tolerance, defaults ----
vw = Wand([(0, 0), (3000, 0)], dicke=240, schraffur="voll")
check(len(vw.flaechen()) == 1 and len(vw.prims()) == len(vw.prims(schraffur=False)), "Vollflaeche: Flaeche, keine Linien")
check(Wand([(0, 0), (3000, 0)]).schraffur_abstand == 180, "Standard-Linienabstand 180")
fw = Wand([(0, 0), (3000, 0)], dicke=240, schraffur="voll")
fo = Oeffnung("fenster", 1500, 0, 0.0, breite=1000); wand_verknuepfen([fw, fo])
check(len(fw.flaechen()) == 2 and fw._luecken == [] and len(fw._fenster) == 1, "Fenster: Flaeche ausgespart, Kanten laufen durch")
hf = Wand([(0, 0), (3000, 0)], dicke=240, schraffur="schraeg", schraffur_abstand=40)
wand_verknuepfen([hf, fo])
for pl, _c in hf.prims()[len(hf.prims(schraffur=False)):]:
    assert not (max(p[0] for p in pl) > 1000 + 1e-6 and min(p[0] for p in pl) < 2000 - 1e-6), "Schraffur im Fenster"
check(True, "keine Schraffur im Fenster")
for ausr in ("mitte", "links", "rechts"):
    for ang in (0, 30, 77):
        a_ = math.radians(ang)
        wx = Wand([(100, 200), (100 + 3000 * math.cos(a_), 200 + 3000 * math.sin(a_))], dicke=240, ausrichtung=ausr)
        px, py = 100 + 1700 * math.cos(a_), 200 + 1700 * math.sin(a_)      # on the line
        od = Oeffnung("tuer", px, py, 0.0); wand_verknuepfen([wx, od])
        assert len(wx._luecken) == 1, f"Tuer auf der Linie ({ausr}, {ang})"
check(True, "Tuer auf der Wandlinie wird in jeder Lage gefunden")
d = json.loads(json.dumps(vw.to_dict()))
check("_fenster" not in d and d["schraffur"] == "voll", "Vollflaeche gespeichert, keine Laufzeitdaten")
check(core.WAND_SCHRAFFUREN[-1] == "voll", "Schraffurart voll vorhanden")
for k in ("tb.wz.wand", "tb.wz.tuer", "tb.wz.fenster", "dlg.wand.titel", "dlg.wand.titel_tuer", "dlg.wand.spiegeln",
          "dlg.wand.umkehren", "menu.wand.spiegeln", "menu.wand.umkehren", "menu.wand.tuer_bearbeiten",
          "msg.wand.klick", "menu.einfuegen.wand", "menu.wand.verbinden", "menu.wand.schraffur", "dlg.wand.schraffur",
          "msg.wand.zwei", "msg.wand.verb_zu_weit", "tb.wz.wandverb", "dlg.wand.schr.voll", "msg.wand.verb_erste"):
    check(k in I.TEXTE["de"] and k in I.TEXTE["en"], k)
check(core.BEFEHLE.get("WAND") == "tool:wand", "Befehl WAND")
check(core.BEFEHLE.get("WANDVERBINDEN") == "wand:verbinden", "Befehl WANDVERBINDEN")
check(core.WAND_LAYER_FARBE[0] == "#c29bff", "Wandebene in der Standardfarbe")
from katiecad.ui import icons as IC
check(all(n in IC.NAMEN for n in ("wand", "tuer", "fenster", "wandverb")), "Icons registriert")
# doppelt liegende Waende: eine Tuer / ein Fenster schneidet in alle
_a = core.Wand([(0, 0), (4000, 0)], dicke=240, schraffur="schraeg")
_b = core.Wand([(0, 0), (4000, 0)], dicke=240, schraffur="schraeg")
_t = core.Oeffnung("tuer", 1000, 0)
_f = core.Oeffnung("fenster", 3000, 0)
core.wand_verknuepfen([_a, _b, _t, _f])
check(bool(_a._luecken) and bool(_b._luecken), "Doppelte Waende: Tuer schneidet in beide")
check(bool(_a._fenster) and bool(_b._fenster), "Doppelte Waende: Fenster in beiden")
# Wandanschluss (T) und gemeinsame Kontur
_B = core.Wand([(0, 0), (6000, 0)], dicke=240, schraffur="schraeg")
_A = core.Wand([(3000, -3000), (3000, -300)], dicke=240, schraffur="schraeg")
_r = core.wand_verbinden(_A, _B)
check(isinstance(_r, dict) and _r.get("modus") == "t" and abs(_r["punkt"][1]) < 1e-6 and abs(_r["punkt"][0] - 3000) < 1e-6,
      "T-Anschluss: Wandende wird auf die andere Wand gesetzt")
_A.punkte[_r["index"]] = _r["punkt"]
core.wand_verknuepfen([_B, _A])
check(max(p[1] for pl, _c in _A.prims(schraffur=False) for p in pl) < 1.0
      and max(p[1] for pl, _c in _A.prims(schraffur=False) for p in pl) > -121,
      "T-Anschluss: Wandflaechen enden an der Flaeche der anderen Wand, Kappe verschwindet")
_A2 = core.Wand([(3000, -3000), (3000, 500)], dicke=240)
core.wand_verknuepfen([_B, _A2])
check(all(not (-100 < min(p[1] for p in pl) and max(p[1] for p in pl) < 100) for pl, _c in _A2.prims(schraffur=False)),
      "Ueberstand: nichts im Inneren der anderen Wand gezeichnet")
_W1 = core.Wand([(0, 0), (3000, 0)]); _W2 = core.Wand([(3100, 100), (3100, 3000)])
check(core.wand_verbinden(_W1, _W2).get("modus") != "t", "Ecke bleibt Ecke (Verschmelzen)")
check("_abzug" not in json.loads(json.dumps(_A.to_dict())), "Laufzeitdaten werden nicht gespeichert")
check("msg.wand.angeschlossen" in I.TEXTE["de"] and "msg.wand.angeschlossen" in I.TEXTE["en"], "Meldung angeschlossen")
# Tuer in einem spaeteren Wandsegment (Raum): Luecke/Schraffur an der richtigen Stelle
_R = core.Wand([(0, 0), (5000, 0), (5000, 4000), (0, 4000)], geschlossen=True, dicke=240, schraffur="schraeg")
_tt = core.Oeffnung("tuer", 5000, 2000)
core.wand_verknuepfen([_R, _tt])
check(len(_R._luecken) == 1 and _R._luecken[0][0] == 1 and 0.0 < _R._luecken[0][1] < _R._luecken[0][2] <= 1.0,
      "Tuer im 2. Segment: Luecke liegt im Segment (nicht kumulativ)")
check(not [1 for pl in _R._schraffurlinien() for p in pl if abs(p[0] - 5000) < 125 and 1500 < p[1] < 2500
           and abs(p[0] - 5000) < 125 and (1550 < sum(q[1] for q in pl) / 2 < 2450)],
      "Tuer im 2. Segment: keine Schraffur in der Tuer")
# Wand schliessen (Anfang und Ende derselben Wand)
_O = core.Wand([(70, 410), (600, 440), (610, 20), (-10, 0), (-20, 500)], dicke=24)
_s = core.wand_schliessen(_O)
check(isinstance(_s, dict) and len(_s["punkte"]) == 4, "Wand schliessen: Schnittpunkt ersetzt Anfang und Ende")
check(core.wand_schliessen(_R) == "geschlossen", "Wand schliessen: schon geschlossen")
check("menu.wand.schliessen" in I.TEXTE["de"] and "menu.wand.schliessen" in I.TEXTE["en"], "Text Wand schliessen")
# Raeume
_rm = core.Raum([(0, 0), (5000, 0), (5000, 4000), (0, 4000)], nummer="1.01", bezeichnung="Buero")
check(abs(_rm.flaeche_m2() - 20.0) < 1e-9, "Raum: Flaeche 20 m2")
check(_rm.text_pos() == (2500.0, 2000.0), "Raum: Schrift im Schwerpunkt")
check(_rm.trifft(2500, 2000) and not _rm.trifft(300, 300), "Raum: nur die Schrift trifft, der Kasten ist unsichtbar")
check(all(p[0] == "t" for p in _rm.prims()), "Raum: gezeichnet wird nur Text")
_rm.griff_bewegen("p2", 6000, 4000)
check(abs(_rm.flaeche_m2() - 22.0) < 1e-9, "Raum: Ecke verschieben rechnet Flaeche neu")
_rm.griff_bewegen("t", 100, 100)
check(_rm.text_pos() == (100.0, 100.0), "Raum: Schrift mit Griff verschiebbar")
_d = json.loads(json.dumps(_rm.to_dict()))
check(_d["typ"] == "raum" and core.Raum(**{k: v for k, v in _d.items() if k != "typ"}).nummer == "1.01", "Raum: speichern / laden")
_rm.verschieben(10, 10); _rm.drehen(0, 0, 90)
check(abs(_rm.flaeche_m2() - 22.0) < 1e-6, "Raum: verschieben / drehen behaelt die Flaeche")
for k in ("tb.wz.raum", "menu.einfuegen.raum", "menu.raum.bearbeiten", "msg.raum.klick", "msg.raum.hinweis",
          "dlg.raum.titel", "dlg.raum.nummer", "dlg.raum.bezeichnung", "dlg.raum.hoehe", "dlg.raum.flaeche", "dlg.raum.hinweis"):
    check(k in I.TEXTE["de"] and k in I.TEXTE["en"], k)
check(core.BEFEHLE.get("RAUM") == "tool:raum" and "raum" in IC.NAMEN, "Befehl und Icon Raum")
# Ecken bleiben Ecken (kein T-Anschluss), auch mit Ueberstand / Luecke
for _n, (_p, _q) in {"exakt": ([(0, 0), (3000, 0)], [(3000, 0), (3000, 3000)]),
                     "Luecke": ([(0, 0), (2900, 0)], [(3000, 100), (3000, 3000)]),
                     "Ueberstand": ([(0, 0), (3200, 0)], [(3000, -200), (3000, 3000)]),
                     "gerade": ([(0, 0), (3000, 0)], [(3100, 0), (6000, 0)])}.items():
    _r = core.wand_verbinden(core.Wand(_p, dicke=240), core.Wand(_q, dicke=240))
    check(isinstance(_r, dict) and _r.get("modus") != "t" and "punkte" in _r, "Ecke verschmilzt: " + _n)
_L = core.Raum([(0, 0), (5000, 0), (5000, 2000), (2000, 2000), (2000, 4000), (0, 4000)])
check(abs(_L.flaeche_m2() - 14.0) < 1e-9 and len(_L.griffe()) == 7, "Raum mit 6 Ecken: Flaeche 14 m2, 6 Eckgriffe + Schrift")
_F = core.Raum([(0, 0), (1000, 0), (1000, 1000)], schriftart=core.schrift_setzen("Courier", True))
check(_F.prims()[0][6] == "Courier|b" and _F.text_obj().schriftart == "Courier|b", "Raum: Schriftart (fett) in Anzeige und Trefferflaeche")
check(core.Raum(**{k: v for k, v in core.Raum([(0, 0), (1, 0), (1, 1)]).to_dict().items() if k != "typ"}).schriftart == "Arial", "Raum: Standardschrift Arial")
# Tuermodelle
_ein = core.Oeffnung("tuer", 0, 0, 0, breite=1500)
_dp = core.Oeffnung("tuer", 0, 0, 0, breite=1500, modell="doppel")
_du = core.Oeffnung("tuer", 0, 0, 0, breite=1500, modell="doppel_ungleich", anteil=0.67)
_rt = core.Oeffnung("tuer", 0, 0, 0, breite=3000, modell="rolltor")
check(len(_ein.prims()) == 4 and len(_dp.prims()) == 6 and len(_du.prims()) == 6, "Tuermodelle: Einfach 1, Doppel 2 Fluegel")
_hoch = lambda o: max(p[1] for pl, _c in o.prims() for p in pl)
check(abs(_hoch(_ein) - (120 + 1500)) < 1e-6 and abs(_hoch(_dp) - (120 + 750)) < 1e-6
      and abs(_hoch(_du) - (120 + 1005)) < 1e-6, "Tuermodelle: Flügelbreiten (gleich / ungleich)")
_ds = core.Oeffnung("tuer", 0, 0, 0, breite=1500, modell="doppel_ungleich", spiegeln=True)
_spitze = lambda o: [p[0] for pl, _c in o.prims() for p in pl if abs(p[1] - (120 + 1005)) < 1e-6 and len(pl) == 2]
check(_spitze(_du) == [-750.0] and _spitze(_ds) == [750.0], "Tuermodelle: spiegeln tauscht die Seite des grossen Fluegels")
check(all(abs(p[1]) <= 120 + 1e-6 for pl, _c in _rt.prims() for p in pl) and len(_rt.prims()) > 6, "Rolltor: gestrichelt in der Wand, kein Tuerblatt")
check(core.Oeffnung("fenster", modell="rolltor").modell == "einfach", "Fenster hat kein Tuermodell")
_dd = json.loads(json.dumps(_du.to_dict()))
check(_dd["modell"] == "doppel_ungleich" and core.Oeffnung(**{k: v for k, v in _dd.items() if k != "typ"}).anteil == 0.67, "Tuermodell speichern / laden")
_wd = core.Wand([(0, 0), (6000, 0)], dicke=240, schraffur="schraeg")
core.wand_verknuepfen([_wd, core.Oeffnung("tuer", 3000, 0, breite=3000, modell="rolltor")])
check(len(_wd._luecken) == 1 and abs((_wd._luecken[0][2] - _wd._luecken[0][1]) - 0.5) < 1e-6, "Rolltor schneidet die Wandluecke")
for k in ("dlg.wand.modell", "dlg.wand.modell.einfach", "dlg.wand.modell.doppel", "dlg.wand.modell.doppel_ungleich",
          "dlg.wand.modell.rolltor", "dlg.wand.anteil", "dlg.wand.spiegeln_gross", "dlg.wand.titel_vorgabe_tuer",
          "dlg.wand.titel_vorgabe_fenster"):
    check(k in I.TEXTE["de"] and k in I.TEXTE["en"], k)
# Anschluss einer Wand an die Ecke eines bestehenden Winkels (Wand laeuft in der Verlaengerung weiter,
# Luecke ca. eine halbe Wandstaerke): T-Anschluss statt Verschmelzen ueber den Winkel zurueck
_K = 240 / 107.0
_S = lambda p: (p[0] * _K, -p[1] * _K)
for _lw in ([(364.5, -50), (364.5, 111.5), (900, 111.5)], [(900, 111.5), (364.5, 111.5), (364.5, -50)]):
    for _un in ([(364.5, 216), (364.5, 500)], [(364.5, 500), (364.5, 216)]):
        _a = core.Wand([_S(p) for p in _lw], dicke=240)
        _b = core.Wand([_S(p) for p in _un], dicke=240)
        for _x, _y in ((_a, _b), (_b, _a)):
            _r = core.wand_verbinden(_x, _y)
            check(isinstance(_r, dict) and _r.get("modus") == "t" and _r["wand"] is _b
                  and abs(_r["punkt"][0] - 364.5 * _K) < 1e-6 and abs(_r["punkt"][1] + 111.5 * _K) < 1e-6,
                  "Anschluss an Winkelecke: T-Anschluss auf die Ecke")
# nach dem Anschluss: keine Linie der Winkelwand quer durch die anschliessende Wand
_a = core.Wand([_S(p) for p in [(364.5, -50), (364.5, 111.5), (900, 111.5)]], dicke=240)
_b = core.Wand([_S(p) for p in [(364.5, 216), (364.5, 500)]], dicke=240)
_r = core.wand_verbinden(_a, _b)
_b.punkte[0] = _r["punkt"]
core.wand_verknuepfen([_a, _b])
_quer = [pl for pl, _c in _a.prims(schraffur=False)
         if len(pl) == 2 and abs(pl[0][1] - pl[1][1]) < 1e-6 and abs(pl[0][1] + 165 * _K) < 1.0
         and min(pl[0][0], pl[1][0]) < 400 * _K < max(pl[0][0], pl[1][0]) and min(pl[0][0], pl[1][0]) < 350 * _K]
check(not _quer, "Winkelwand: keine Linie quer durch die anschliessende Wand")

# Wand beruehrt eine andere schon mit einem Ende (unten links), das andere Ende (oben rechts) ist noch frei:
# "Verbinden" setzt das freie Ende an, nicht das schon angeschlossene
_K2 = 240 / 16.0
_S2 = lambda p: (p[0] * _K2, -p[1] * _K2)
for _xr in (560, 900):
    _a = core.Wand([_S2(p) for p in [(98, 440), (98, 99), (_xr, 99)]], dicke=240)
    _b = core.Wand([_S2(p) for p in [(489, 117), (489, 365.5), (98, 365.5)]], dicke=240)
    for _x, _y in ((_a, _b), (_b, _a)):
        _r = core.wand_verbinden(_x, _y)
        check(_r.get("modus") == "t" and _r["wand"] is _b and _r["index"] == 0
              and abs(_r["punkt"][1] + 99 * _K2) < 1e-6 and abs(_r["punkt"][0] - 489 * _K2) < 1e-6,
              f"freies Ende wird angeschlossen (Laenge {_xr})")


# Strecken: Wandende + Tuer im Fenster wandern mit
import types
from katiecad.ui.app import CadApp as _CA
_w1 = core.Wand([(0, 0), (4000, 0)], dicke=240)
_o = core.Oeffnung("tuer", 4000, 0, 0, dicke=240)
_a = types.SimpleNamespace(_op=None, layers={}, _aktuelle_elemente_liste=lambda: [_w1, _o])
_a._stretch_element = lambda el, i, dx, dy: _CA._stretch_element(_a, el, i, dx, dy)
_CA._stretch_anwenden(_a, (3500, -500, 4500, 500), 1000, 0)
check(_w1.punkte == [(0, 0), (5000, 0)] and _o.x == 5000, "Strecken: Wand + Tuer wandern mit")


# Bloecke: Text/Attribut wird bei Drehung nie auf den Kopf gestellt (90/270 bleiben erlaubt)
for _w, _erw in ((0, 0), (90, 90), (180, 0), (270, 270), (45, 45), (135, 315)):
    _blk = core.BlockReferenz(0, 0, "T", [core.Linie(0, 0, 5, 0), core.Text(10, 0, "E", 3.5),
                                          core.AttributDefinition(20, 0, tag="IND", wert="K1")], winkel=_w)
    for _t in _blk.aufgeloest():
        if isinstance(_t, core.Text):
            check(abs(_t.winkel - _erw) < 1e-6, f"Text bei Blockdrehung {_w}: {_t.winkel}")
_blk = core.BlockReferenz(0, 0, "T", [core.Text(10, 0, "E", 3.5)], winkel=180)
_t = [e for e in _blk.aufgeloest() if isinstance(e, core.Text)][0]
check(_t.einfuegepunkt == "oben_rechts" and abs(_t.x + 10) < 1e-6, "180 Grad: Anker gespiegelt, Position gedreht")

print(f"test_wand - {ok} Checks bestanden")
