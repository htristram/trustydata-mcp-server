"""La vitrine annonce `verify_email` sans promettre qu'une boîte existe.

Le service contrôle le domaine et le genre de l'adresse ; il ne se connecte à
aucune boîte. La copy publique ne dit donc jamais qu'une adresse est « valid »
ni qu'une boîte « exists ». La description du registre reste sous 100
caractères (une description plus longue a déjà été refusée par le registre).
"""
import json
import pathlib

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
TEXTES = ["README.md", *sorted(str(p.relative_to(RACINE)) for p in (RACINE / "submissions").glob("*.md"))]
INTERDITS = ("validates email", "validate email", "valid email", "email validation",
             "e-mail validation", "valid e-mail", "mailbox exists", "verified mailbox",
             "adresse valide", "boîte existe")


def test_description_du_registre_sous_cent_caracteres():
    d = json.loads((RACINE / "server.json").read_text(encoding="utf-8"))
    assert len(d["description"]) < 100 and "email" in d["description"].lower()


def test_le_readme_liste_verify_email_au_plan_starter():
    lignes = (RACINE / "README.md").read_text(encoding="utf-8").splitlines()
    ligne = next(l for l in lignes if l.startswith("| `verify_email`"))
    assert ligne.rstrip().endswith("| Starter |")
    assert "never" in ligne.lower()  # la ligne dit ce que l'outil ne confirme pas


def test_le_readme_liste_treize_outils():
    lignes = (RACINE / "README.md").read_text(encoding="utf-8").splitlines()
    debut = lignes.index("## Tools")
    fin = next(i for i in range(debut + 1, len(lignes)) if lignes[i].startswith("## "))
    outils = [l for l in lignes[debut:fin] if l.startswith("| `")]
    assert len(outils) == 13


@pytest.mark.parametrize("chemin", TEXTES)
def test_aucune_promesse_sur_l_existence_d_une_boite(chemin):
    texte = (RACINE / chemin).read_text(encoding="utf-8").lower()
    for interdit in INTERDITS:
        assert interdit not in texte, interdit


@pytest.mark.parametrize("chemin", [t for t in TEXTES if t != "submissions/official-registry.md"])
def test_chaque_texte_cite_le_controle_d_e_mail(chemin):
    assert "e-mail" in (RACINE / chemin).read_text(encoding="utf-8").lower()
