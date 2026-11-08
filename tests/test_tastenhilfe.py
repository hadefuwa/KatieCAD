# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stub  # noqa: F401
import katiecad.common.i18n as I
from katiecad.model.core import BEFEHLE
from katiecad.ui import tastenhilfe as TH
from katiecad.ui import tastenhilfe_es as THES
ok = 0
def check(c, m):
    global ok
    assert c, "FEHLER: " + m
    ok += 1

check(all(x[0] in THES.TASTEN for x in TH.TASTEN + TH.MAUS), "Spanisch: alle Tasten/Mausaktionen")
check(set(THES.BESCHREIBUNG) == set(TH.BESCHREIBUNG), "Spanisch: alle Befehlsbeschreibungen")
fehlend = sorted({f for f in BEFEHLE.values() if f not in TH.BESCHREIBUNG})
check(not fehlend, f"Befehle ohne Beschreibung: {fehlend}")
check(not [f for f in TH.BESCHREIBUNG if f not in set(BEFEHLE.values())], "Beschreibung ohne Befehl")
for sp in ("de", "en", "es"):
    I.SPRACHE["aktuell"] = sp
    ab = TH.abschnitte()
    check(len(ab) == 3 and all(z for _t, z in ab), f"3 Abschnitte {sp}")
    zeilen = ab[2][1]
    check(sum(len(n.split(" / ")) for n, _t in zeilen) == len(BEFEHLE), f"alle {len(BEFEHLE)} Befehlsnamen {sp}")
    check(any(t == "F1" for t, _x in ab[0][1]), "F1 in der Liste")
    check(all(a and b for _t, z in ab for a, b in z), "keine leeren Zeilen")
# registered keys really exist as bindings
src = open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "katiecad", "ui", "app.py"), encoding="utf-8").read()
for k in ("F1", "F2", "F3", "F4", "F7", "F8", "F9"):
    check(f'self.root.bind("<{k}>"' in src, f"Taste {k} gebunden")
print(f"OK ({ok} Pruefungen)")
