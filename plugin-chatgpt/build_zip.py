#!/usr/bin/env python3
"""Construit le ZIP du plugin ChatGPT depuis plugin-chatgpt/, et rien d'autre.

Liste blanche des chemins emballés, refus de tout fichier étranger (un
brouillon, un .DS_Store) et de tout texte qui ressemble à un secret, URL de
la vidéo de démonstration posée dans le plugin.json du ZIP seulement, jamais
dans le dépôt. Stdlib seule.

    python3 plugin-chatgpt/build_zip.py --video https://… --sortie dist/
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

AUTORISES = ("plugin.json", "mcp.json", "skills/", "assets/")
IGNORES = ("schemas/", "build_zip.py", "dist/", "__pycache__/")
SECRETS = (r"sk-[A-Za-z0-9]{20,}", r"tdp_live_", r"client_secret", r"skc_", r"Bearer ")
TEXTE = {".json", ".md", ".txt", ".svg", ".yaml", ".yml"}
# Dans les deux dossiers, seule la forme attendue passe : une skill est
# `skills/<nom>/SKILL.md` avec ses sous-dossiers de convention, une icône est
# une image. Un brouillon posé à côté fait échouer le build plutôt que
# d'entrer dans le paquet public.
FORME = {
    "skills/": re.compile(r"^skills/[a-z0-9-]+/(SKILL\.md|(references|scripts|assets)/.+)$"),
    "assets/": re.compile(r"^assets/[^/]+\.(png|svg|jpe?g|webp)$"),
}


def _relatif(chemin: Path, racine: Path) -> str:
    return chemin.relative_to(racine).as_posix()


def _refuser(message: str) -> None:
    print(f"build_zip: {message}", file=sys.stderr)
    sys.exit(2)


def _fichiers(racine: Path) -> list[Path]:
    """Les fichiers à emballer, après refus de tout ce qui n'est pas attendu."""
    retenus = []
    for chemin in sorted(p for p in racine.rglob("*") if p.is_file()):
        rel = _relatif(chemin, racine)
        if rel.startswith(IGNORES):
            continue
        if not rel.startswith(AUTORISES):
            _refuser(f"fichier hors liste blanche : {rel}")
        for prefixe, forme in FORME.items():
            if rel.startswith(prefixe) and not forme.match(rel):
                _refuser(f"fichier inattendu dans {prefixe} : {rel}")
        if chemin.suffix in TEXTE:
            texte = chemin.read_text(encoding="utf-8", errors="replace")
            for motif in SECRETS:
                if re.search(motif, texte):
                    _refuser(f"secret probable ({motif}) dans {rel}")
        retenus.append(chemin)
    return retenus


def construire(racine: Path, sortie: Path, video_url: str | None) -> Path:
    """Écrit trustydata-plugin-<version>.zip dans `sortie` et rend son chemin."""
    racine, sortie = Path(racine), Path(sortie)
    fichiers = _fichiers(racine)
    manifeste = json.loads((racine / "plugin.json").read_text(encoding="utf-8"))
    if video_url:
        manifeste["extensions"]["com.openai"].setdefault("review", {})["demo_recording_url"] = video_url
    sortie.mkdir(parents=True, exist_ok=True)
    zip_path = sortie / f"trustydata-plugin-{manifeste['version']}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for chemin in fichiers:
            rel = _relatif(chemin, racine)
            if rel == "plugin.json":
                zf.writestr(rel, json.dumps(manifeste, ensure_ascii=False, indent=2) + "\n")
            else:
                zf.write(chemin, rel)
    return zip_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--video", default=None, help="URL de la vidéo de démonstration (jamais versionnée)")
    parser.add_argument("--sortie", default="dist", help="dossier de sortie (défaut : dist/)")
    args = parser.parse_args(argv)
    chemin = construire(Path(__file__).resolve().parent, Path(args.sortie), args.video)
    print(chemin)
    return 0


if __name__ == "__main__":
    sys.exit(main())
