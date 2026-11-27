"""Le plugin ChatGPT est publié dans le répertoire d'OpenAI depuis le 2026-11-26.

La vitrine dit comment l'installer et ne renvoie plus au mode développeur de
ChatGPT. Le lien est celui de la fiche, sans le paramètre `?search=` que
ChatGPT ajoute à l'URL copiée. `verify_email` est entré au serveur pendant la
revue, `verify_phone` ensuite : tant qu'OpenAI ne les a pas approuvés, le README le dit.
"""
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
LIEN = "https://chatgpt.com/plugins/plugin_asdk_app_6af0c6aa1aa08191acea5ac872785fb4"
TEXTES = ["README.md", *sorted(str(p.relative_to(RACINE)) for p in (RACINE / "submissions").glob("*.md"))]


def _section_connect():
    readme = (RACINE / "README.md").read_text(encoding="utf-8")
    return readme.split("\n## Connect\n")[1].split("\n## ")[0]


def test_le_readme_ouvre_la_section_connect_par_le_plugin_chatgpt():
    section = _section_connect()
    assert section.lstrip().startswith("### ChatGPT (plugin directory)")
    assert LIEN in section
    assert "same e-mail" in section  # l'e-mail du compte relie ChatGPT au plan


def test_tout_lien_vers_le_repertoire_est_la_fiche_sans_parametre():
    for fichier in TEXTES:
        texte = (RACINE / fichier).read_text(encoding="utf-8")
        for lien in re.findall(r"https://chatgpt\.com/plugins[^\s)\]>]*", texte):
            assert lien == LIEN, (fichier, lien)


def test_plus_aucun_texte_ne_renvoie_au_mode_developpeur():
    for fichier in TEXTES:
        assert "developer mode" not in (RACINE / fichier).read_text(encoding="utf-8").lower(), fichier


def test_le_readme_dit_que_la_verification_d_e_mail_attend_son_approbation():
    """À retirer, avec la phrase, le jour où le portail OpenAI affiche
    `verify_email` approuvé (et `verify_phone`, qui attend la sienne)."""
    section = _section_connect()
    assert "not yet available in the ChatGPT plugin" in section
    assert "`verify_email`" in section
    assert "`verify_phone`" in section
    assert "eleven of the server's thirteen tools" in " ".join(section.split())


def test_le_readme_ne_promet_rien_sur_les_offres_de_chatgpt():
    section = _section_connect().lower()
    for promesse in ("free chatgpt", "any chatgpt plan", "all chatgpt plans can"):
        assert promesse not in section, promesse
    assert "depends on your chatgpt plan" in " ".join(section.split())


def test_le_kit_mcp_so_ne_laisse_pas_croire_que_le_plugin_verifie_les_e_mails():
    """Le kit cite les contrôles d'e-mail et de numéro et ChatGPT dans la même phrase : il
    porte la même réserve que le README, à retirer le même jour."""
    kit = (RACINE / "submissions/mcp-so.md").read_text(encoding="utf-8")
    assert "not yet available in the ChatGPT plugin" in kit
    phrase = next(p for p in kit.split(". ") if "not yet available in the ChatGPT plugin" in p).lower()
    assert "e-mail" in phrase and "phone" in phrase


def test_le_readme_ne_dit_pas_ce_que_la_fiche_d_openai_affiche():
    assert "install button is offered" not in " ".join(_section_connect().split())
