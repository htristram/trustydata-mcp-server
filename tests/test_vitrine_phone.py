"""La vitrine annonce `verify_phone` sans promettre qu'une ligne existe.

Le service dit si un numéro tient dans le plan de numérotation de son pays
(tranches attribuées par l'ARCEP pour un numéro français) et s'il a l'air
fabriqué ; il n'appelle jamais la ligne. La copy publique ne dit donc jamais
qu'un numéro est « valid », qu'une ligne « exists » ou qu'elle est « active »,
et ne nomme aucun opérateur. La description du registre reste sous 100
caractères.
"""
import json
import pathlib
import re

import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent
TEXTES = ["README.md", *sorted(str(p.relative_to(RACINE)) for p in (RACINE / "submissions").glob("*.md"))]
# Seul le kit du registre officiel ne porte aucune copy : il renvoie à server.json.
TEXTES_AVEC_COPY = [t for t in TEXTES if t != "submissions/official-registry.md"]
INTERDITS = re.compile(
    r"\bvalidates?\b|\bvalid\b|\bvalidity\b|\bexists?\b|\bactive\b|in service|carrier|\bHLR\b",
    re.IGNORECASE,
)


def blocs(texte):
    """Découpe en blocs : paragraphes, puces, lignes de tableau. Un bloc de
    citation (`>`) ou un paragraphe continu reste d'un seul tenant."""
    courant, resultat = [], []
    for ligne in texte.splitlines():
        if not ligne.strip():
            if courant:
                resultat.append(" ".join(courant))
                courant = []
        elif ligne.startswith(("- ", "| ")):
            if courant:
                resultat.append(" ".join(courant))
            courant = [ligne]
        else:
            courant.append(ligne.strip())
    if courant:
        resultat.append(" ".join(courant))
    return resultat


# Limite connue : seuls les blocs qui contiennent le mot « phone » sont examinés ;
# une phrase sur le téléphone qui dit seulement « number » n'est pas lue. Ce garde
# ne remplace pas la relecture.
def interdits_sur_le_telephone(texte):
    """Les mots interdits trouvés dans les seuls blocs qui parlent de téléphone."""
    trouves = []
    for bloc in blocs(texte):
        if "phone" in bloc.lower():
            trouves += [m.group(0) for m in INTERDITS.finditer(bloc)]
    return trouves


def test_le_garde_attrape_un_mot_interdit_sur_le_telephone():
    assert interdits_sur_le_telephone("The phone check validates numbers.") == ["validates"]
    assert interdits_sur_le_telephone("Tells whether the phone line exists.") == ["exists"]
    assert interdits_sur_le_telephone("A phone number lookup by carrier (HLR).") == ["carrier", "HLR"]
    assert interdits_sur_le_telephone("Is this phone number valid? Is it active?") == ["valid", "active"]
    # Les autres copies du dépôt ne sont pas visées : pas de faux positif.
    assert interdits_sur_le_telephone("Only active establishments are counted.") == []
    assert interdits_sur_le_telephone("- Phone checks.\n- Only active establishments.") == []


def test_description_du_registre_sous_cent_caracteres():
    d = json.loads((RACINE / "server.json").read_text(encoding="utf-8"))
    assert len(d["description"]) < 100 and "phone" in d["description"].lower()
    assert d["version"] == "1.8.0"


def test_le_readme_liste_verify_phone_au_plan_starter():
    lignes = (RACINE / "README.md").read_text(encoding="utf-8").splitlines()
    ligne = next(l for l in lignes if l.startswith("| `verify_phone`"))
    assert ligne.rstrip().endswith("| Starter |")
    assert "never" in ligne.lower()  # la ligne dit ce que l'outil ne fait pas


@pytest.mark.parametrize("chemin", TEXTES)
def test_aucune_promesse_sur_l_existence_d_une_ligne(chemin):
    texte = (RACINE / chemin).read_text(encoding="utf-8")
    assert interdits_sur_le_telephone(texte) == []


@pytest.mark.parametrize("chemin", TEXTES_AVEC_COPY)
def test_chaque_texte_cite_le_controle_de_numero(chemin):
    assert "phone" in (RACINE / chemin).read_text(encoding="utf-8").lower()


def test_le_readme_dit_les_deux_niveaux_de_preuve_et_aucun_appel_de_ligne():
    texte = " ".join((RACINE / "README.md").read_text(encoding="utf-8").split())
    assert "ARCEP" in texte
    assert "never calls the line" in texte
    assert "not only French" in texte


def test_le_kit_pulsemcp_compte_treize_outils():
    texte = (RACINE / "submissions/pulsemcp.md").read_text(encoding="utf-8")
    assert "13 tools" in texte and "12 tools" not in texte


def test_aucun_detail_interne_dans_la_vitrine():
    for chemin in TEXTES:
        texte = (RACINE / chemin).read_text(encoding="utf-8").lower()
        assert "/internal" not in texte, chemin
        assert "scalekit" not in texte, chemin
