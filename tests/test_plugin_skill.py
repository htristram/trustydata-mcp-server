"""La skill d'accueil du plugin ChatGPT : déclarée dans le manifeste, en-tête
YAML, plans, et les cinq prompts du serveur repris comme recettes."""
import json
import re

from tests.test_plugin_manifest import OUTILS, RACINE


def test_la_skill_d_accueil_est_declaree_et_bien_formee():
    manifeste = json.loads((RACINE / "plugin.json").read_text(encoding="utf-8"))
    chemin = manifeste["extensions"]["com.openai"]["onboardingSkill"]
    assert chemin == "./skills/get-started/SKILL.md"
    texte = (RACINE / chemin).read_text(encoding="utf-8")
    entete = re.match(r"---\nname: get-started\ndescription: .+\n---\n", texte)
    assert entete, "en-tête YAML avec name et description"
    for mot in ("Discovery", "Growth", "Business", "Pass Zones", "app.trustydata.app"):
        assert mot in texte
    # Finding du portail (2026-11-08) : pas d'offre commerciale ; et le Pass Zones
    # n'a pas de quota mensuel, le mot « monthly » était faux.
    for motif in (r"\(free\)", r"\bbought\b", r"monthly quota", r"€"):
        assert not re.search(motif, texte), motif
    for prompt in ("zone_de_chalandise", "comparer_emplacements", "potentiel_commerce",
                   "verifier_adresses", "qualifier_entreprise"):
        assert prompt in texte, "les cinq prompts du serveur, repris comme recettes"
    assert {o for o in OUTILS if o in texte} >= {"zone_stats", "verify_address", "search_company"}
