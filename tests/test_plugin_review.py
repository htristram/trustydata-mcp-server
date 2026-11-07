"""Les cas de revue OpenAI, la traduction française et les notes de version
du plugin ChatGPT, dans plugin.json."""
import json

from tests.test_plugin_manifest import OUTILS, RACINE


def _openai():
    return json.loads((RACINE / "plugin.json").read_text(encoding="utf-8"))["extensions"]["com.openai"]


def test_cinq_cas_positifs_et_trois_negatifs_complets():
    cas = _openai()["review"]["test_cases"]
    assert len(cas["positive"]) == 5 and len(cas["negative"]) == 3
    for c in cas["positive"]:
        assert c["description"] and c["prompt"] and c["expected_behavior"]
        assert set(map(str.strip, c["tools_triggered"].split(","))) <= OUTILS
    for c in cas["negative"]:
        assert c["description"] and c["prompt"]


def test_les_cas_positifs_couvrent_les_cinq_familles():
    outils = {c["tools_triggered"].split(",")[0].strip() for c in _openai()["review"]["test_cases"]["positive"]}
    assert outils == {"zone_stats", "zone_compare", "verify_address", "search_company", "search_locality"}


def test_chaque_prompt_positif_nomme_sa_demande():
    attendu = {"zone_stats": "minutes", "zone_compare": "compare", "verify_address": "valid",
               "search_company": "SIRET", "search_locality": "communes"}
    for c in _openai()["review"]["test_cases"]["positive"]:
        assert attendu[c["tools_triggered"].split(",")[0].strip()].lower() in c["prompt"].lower()


def test_les_negatifs_couvrent_dirigeants_hors_france_et_hors_perimetre():
    descriptions = " ".join(c["description"].lower() for c in _openai()["review"]["test_cases"]["negative"])
    for mot in ("director", "france", "pass zones"):
        assert mot in descriptions


def test_pas_de_commerce_ni_de_video_dans_le_depot():
    revue = _openai()["review"]
    assert revue["commerce"] is False and revue["commerce_description"]
    assert "demo_recording_url" not in revue, "injectée au build, jamais versionnée"


def test_la_traduction_francaise():
    fr = _openai()["publication"]["translations"]["fr-FR"]
    assert fr["subtitle"] == "Adresses, entreprises, zones" and len(fr["subtitle"]) <= 30
    assert 200 <= len(fr["description"]) <= 4000 and "Pass Zones" in fr["description"]
    assert "countries" not in _openai()["publication"]
