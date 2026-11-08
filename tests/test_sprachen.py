# -*- coding: utf-8 -*-
"""Languages: German, English and Spanish have the same keys and placeholders."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stub  # noqa: F401
import katiecad.common.i18n as I
from katiecad.common import config as C
ok = 0
def check(c, m):
    global ok
    assert c, "FEHLER: " + m
    ok += 1

T = I.TEXTE
check(set(T) == {"de", "en", "es"}, "Sprachen de/en/es")
for sp in ("en", "es"):
    check(set(T[sp]) == set(T["de"]), f"{sp}: gleiche Schluessel wie de: {sorted(set(T['de']) ^ set(T[sp]))[:5]}")
    schlecht = [k for k in T["en"] if sorted(re.findall(r"\{\w+(?:[!:][^}]*)?\}", T[sp][k])) != sorted(re.findall(r"\{\w+(?:[!:][^}]*)?\}", T["en"][k]))]
    check(not schlecht, f"{sp}: Platzhalter stimmen: {schlecht[:5]}")
    check(all(str(v).strip() for v in T[sp].values()), f"{sp}: keine leeren Texte")
for k in ("menu.sprache.de", "menu.sprache.en", "menu.sprache.es"):
    check(all(k in T[sp] for sp in T), k)
check("es" in C._UNTERSTUETZTE_SPRACHEN, "config kennt es")
# fallback: Spanish -> English -> German
I.SPRACHE["aktuell"] = "es"
_alt = T["es"].pop("menu.datei")
check(I.tr("menu.datei") == T["en"]["menu.datei"], "fehlender spanischer Text faellt auf Englisch zurueck")
T["es"]["menu.datei"] = _alt
check(I.tr("menu.datei") == "Archivo", "spanischer Text")

# every tr("txt.NNNN", pN=...) call passes the values for the placeholders of all three languages
import ast, glob
_fehler = []
_benutzt = set()
_wurzel = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "katiecad")
for _f in glob.glob(os.path.join(_wurzel, "**", "*.py"), recursive=True):
    if _f.endswith("i18n.py"):
        continue
    for _n in ast.walk(ast.parse(open(_f, encoding="utf-8").read())):
        if (isinstance(_n, ast.Call) and isinstance(_n.func, ast.Name) and _n.func.id == "tr" and _n.args):
            _a = _n.args[0]
            _keys = []
            if isinstance(_a, ast.Constant) and isinstance(_a.value, str):
                _keys = [_a.value]
            elif isinstance(_a, ast.IfExp) and all(isinstance(x, ast.Constant) for x in (_a.body, _a.orelse)):
                _keys = [_a.body.value, _a.orelse.value]
            for _k in _keys:
                if not _k.startswith("txt."):
                    continue
                _benutzt.add(_k)
                for _sp in T:
                    if _k not in T[_sp]:
                        _fehler.append(f"{_k} fehlt in {_sp}")
                        continue
                    _ph = set(re.findall(r"\{(\w+)", T[_sp][_k]))
                    _kw = {kw.arg for kw in _n.keywords}
                    if _ph - _kw and not any(kw.arg is None for kw in _n.keywords):
                        _fehler.append(f"{os.path.basename(_f)}:{_n.lineno} {_k} {_sp}: Platzhalter {sorted(_ph - _kw)} ohne Wert")
check(not _fehler, "tr()-Aufrufe: " + "; ".join(_fehler[:5]))
check(len(_benutzt) >= 250, f"txt-Schluessel im Code verwendet: {len(_benutzt)}")
_unbenutzt = [k for k in T["de"] if k.startswith("txt.") and k not in _benutzt]
check(len(_unbenutzt) <= 1, f"unbenutzte txt-Schluessel: {_unbenutzt}")
# no hard-coded German/English switch left in the program
_rest = []
for _f in glob.glob(os.path.join(_wurzel, "**", "*.py"), recursive=True):
    if _f.endswith(("i18n.py", "config.py")):
        continue
    for _i, _l in enumerate(open(_f, encoding="utf-8").read().split("\n"), 1):
        if re.search(r"\bif de else\b|\bif _?de\(\) else\b|\bde = SPRACHE", _l):
            _rest.append(f"{os.path.basename(_f)}:{_i}")
check(not _rest, f"harte de/en-Umschaltung uebrig: {_rest[:5]}")
I.SPRACHE["aktuell"] = "de"
print(f"OK ({ok} Pruefungen)")
