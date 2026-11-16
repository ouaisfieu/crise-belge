#!/usr/bin/env python3
"""Génère le site statique à partir des fichiers Markdown de _src/pages/.

Usage : python3 _src/build.py   (depuis la racine du dépôt)
Dépendance : pip install markdown
"""
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "pages"
ETAT = "16 novembre 2026, 20 h"

BADGES = {
    "{v}": '<span class="b b-v" title="Recoupé en ligne le 16 novembre 2026">recoupé</span>',
    "{n}": '<span class="b b-n" title="Repris du dossier documentaire, non recoupé par l\'auteur le 16 novembre 2026">non recoupé</span>',
    "{d}": '<span class="b b-d" title="Les sources divergent sur ce point">sources divergentes</span>',
    "{a}": '<span class="b b-a" title="Jugement de l\'auteur, pas un fait">avis</span>',
}


def parse(path: Path):
    raw = path.read_text(encoding="utf-8")
    meta = {}
    if raw.startswith("---"):
        _, head, body = raw.split("---", 2)
        for line in head.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    else:
        body = raw
    return meta, body.strip()


def render(body: str):
    md = markdown.Markdown(
        extensions=["tables", "toc", "admonition", "attr_list", "sane_lists", "def_list", "smarty"],
        extension_configs={
            "toc": {"toc_depth": "2-3", "permalink": "§", "permalink_title": "Lien vers cette section"},
            "smarty": {"smart_quotes": False},
        },
    )
    out = md.convert(body)
    for k, v in BADGES.items():
        out = out.replace(k, v)
    out = out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" rel="noopener"', out)
    return out, md.toc_tokens


def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def sections(page_html: str, slug: str, title: str):
    """Découpe une page en sections (h2/h3) pour l'index de recherche."""
    parts = re.split(r'(<h[23] id="[^"]+">.*?</h[23]>)', page_html, flags=re.S)
    res = []
    cur_id, cur_title, buf = "", title, []
    for p in parts:
        m = re.match(r'<h[23] id="([^"]+)">(.*?)</h[23]>', p, flags=re.S)
        if m:
            txt = re.sub(r"\s+", " ", strip_tags(" ".join(buf))).strip()
            if txt:
                res.append({"u": f"{slug}.html" + (f"#{cur_id}" if cur_id else ""), "p": title, "h": cur_title, "t": txt})
            cur_id = m.group(1)
            cur_title = re.sub(r"\s+", " ", strip_tags(m.group(2))).replace("§", "").strip()
            buf = []
        else:
            buf.append(p)
    txt = re.sub(r"\s+", " ", strip_tags(" ".join(buf))).strip()
    if txt:
        res.append({"u": f"{slug}.html" + (f"#{cur_id}" if cur_id else ""), "p": title, "h": cur_title, "t": txt})
    return res


def toc_html(tokens):
    if not tokens:
        return ""
    items = []
    for t in tokens:
        sub = ""
        if t.get("children"):
            sub = "<ol>" + "".join(f'<li><a href="#{c["id"]}">{c["name"]}</a></li>' for c in t["children"]) + "</ol>"
        items.append(f'<li><a href="#{t["id"]}">{t["name"]}</a>{sub}</li>')
    return '<nav class="toc" aria-label="Sommaire de la page"><p class="toc-t">Sur cette page</p><ol>' + "".join(items) + "</ol></nav>"


TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · La crise budgétaire belge de l'automne 2026</title>
<meta name="description" content="{desc}">
<meta name="author" content="Claude (IA d'Anthropic)">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="top">
  <a class="brand" href="index.html"><span class="brand-k">Dossier</span> La crise budgétaire belge <span class="brand-y">automne 2026</span></a>
  <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
</header>
<div class="wrap">
<aside class="side" id="nav">
  <div class="search">
    <label for="q">Rechercher dans le dossier</label>
    <input id="q" type="search" placeholder="index, Vooruit, 1/9, douzièmes…" autocomplete="off">
    <ol id="res" class="res" hidden></ol>
  </div>
  <nav aria-label="Chapitres">
{nav}
  </nav>
  <p class="state">État des lieux arrêté au<br><strong>{etat}</strong></p>
</aside>
<main id="contenu">
<article>
<p class="kicker">{kicker}</p>
<h1>{title}</h1>
{lead}
{toc}
{content}
</article>
<nav class="pn" aria-label="Chapitre précédent et suivant">{prev}{next}</nav>
<footer class="foot">
<p>Texte et jugements : Claude, modèle d'intelligence artificielle d'Anthropic, auteur de ce dossier. Le commanditaire reste anonyme. État des lieux arrêté au {etat} : la crise est en cours, vérifiez toute information datée avant de la reprendre. <a href="a-propos.html">Méthode, limites et licence</a> · <a href="verification.html">Ce qui est sûr, ce qui ne l'est pas</a></p>
</footer>
</main>
</div>
<script src="assets/search-index.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
"""


def main():
    pages = []
    for f in sorted(SRC.glob("*.md")):
        meta, body = parse(f)
        meta["slug"] = f.stem.split("-", 1)[1]
        meta["body"] = body
        pages.append(meta)

    groups = []
    for p in pages:
        g = p.get("group", "")
        if not groups or groups[-1][0] != g:
            groups.append((g, []))
        groups[-1][1].append(p)

    index = []
    for i, p in enumerate(pages):
        content, tokens = render(p["body"])
        nav = ""
        for g, items in groups:
            nav += f'    <p class="g">{g}</p>\n    <ul>\n'
            for it in items:
                cur = ' aria-current="page"' if it is p else ""
                nav += f'      <li><a href="{it["slug"]}.html"{cur}>{it.get("short", it["title"])}</a></li>\n'
            nav += "    </ul>\n"
        prev = nxt = ""
        if i > 0:
            q = pages[i - 1]
            prev = f'<a class="pn-p" href="{q["slug"]}.html"><span>Précédent</span>{q.get("short", q["title"])}</a>'
        if i < len(pages) - 1:
            q = pages[i + 1]
            nxt = f'<a class="pn-n" href="{q["slug"]}.html"><span>Suivant</span>{q.get("short", q["title"])}</a>'
        lead = f'<p class="lead">{p["lead"]}</p>' if p.get("lead") else ""
        for k, v in BADGES.items():
            lead = lead.replace(k, v)
        page = TEMPLATE.format(
            title=p["title"],
            desc=html.escape(strip_tags(p.get("lead", p["title"])))[:300],
            nav=nav,
            etat=ETAT,
            kicker=p.get("kicker", p.get("group", "")),
            lead=lead,
            toc=toc_html(tokens) if p.get("toc", "oui") != "non" else "",
            content=content,
            prev=prev,
            next=nxt,
        )
        (ROOT / f'{p["slug"]}.html').write_text(page, encoding="utf-8")
        index += sections(content, p["slug"], p["title"])

    (ROOT / "assets" / "search-index.js").write_text(
        "window.IDX=" + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";", encoding="utf-8"
    )
    words = sum(len(s["t"].split()) for s in index)
    print(f"{len(pages)} pages, {len(index)} sections indexées, environ {words} mots")


if __name__ == "__main__":
    main()
