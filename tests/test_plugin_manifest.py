"""Le paquet du plugin ChatGPT (plugin-chatgpt/) : manifeste, configuration
MCP, fiche, liens, icônes. Les constantes RACINE, OUTILS et INTERDITS sont
reprises par les autres tests du paquet."""
import json
import pathlib
import re
import struct
import urllib.request

import jsonschema
import pytest

RACINE = pathlib.Path(__file__).resolve().parent.parent / "plugin-chatgpt"
OUTILS = {"compute_route", "get_address_details", "get_company_details", "route_matrix",
          "search_address", "search_company", "search_locality", "search_nearby",
          "verify_address", "zone_compare", "zone_stats"}
INTERDITS = [r"\btraffic\b", r"\btrafic\b", r"\bbulk\b", r"\bbatch\b", r"\bpar lots?\b",
             r"\brnvp\b", r"\bafnor\b", r"\bour customers\b", r"\bnos clients\b",
             r"\bb[êe]ta\b", r"niveau de vie m[ée]dian", r"median income"]


@pytest.fixture(scope="module")
def manifeste():
    return json.loads((RACINE / "plugin.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def interface(manifeste):
    return manifeste["extensions"]["com.openai"]["interface"]


def test_le_manifeste_respecte_le_schema_agent_plugins(manifeste):
    schema = json.loads((RACINE / "schemas" / "plugin.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(manifeste, schema)


def test_la_configuration_mcp_pointe_le_seul_serveur_de_production():
    mcp = json.loads((RACINE / "mcp.json").read_text(encoding="utf-8"))
    assert list(mcp["mcpServers"]) == ["trustydata"]
    serveur = mcp["mcpServers"]["trustydata"]
    assert serveur == {"type": "streamable-http", "url": "https://mcp.trustydata.app/mcp"}, "ni headers ni secret"


def test_les_limites_de_la_fiche(interface):
    assert interface["displayName"] == "TrustyData" and len(interface["shortDescription"]) <= 30
    assert len(interface["longDescription"]) <= 4000 and len(interface["developerName"]) <= 80
    prompts = interface["defaultPrompt"]
    assert 1 <= len(prompts) <= 3 and all(len(p) <= 128 and "@" not in p for p in prompts)
    assert all(re.fullmatch(r"#[0-9A-Fa-f]{6}", interface[c]) for c in ("brandColor", "brandColorDark"))
    assert interface["category"]


def test_la_fiche_dit_les_plans_et_les_sources(interface):
    texte = interface["longDescription"]
    for mot in ("Discovery", "Growth", "Business", "Pass Zones", "BAN", "INSEE", "SIRENE", "France"):
        assert mot in texte
    assert "opposition_prospection" in texte


def test_aucun_terme_interdit():
    for f in RACINE.rglob("*"):
        if f.suffix in (".json", ".md") and "schemas" not in f.parts:
            t = f.read_text(encoding="utf-8").lower()
            for motif in INTERDITS:
                assert not re.search(motif, t), f"{f.name}: {motif}"


@pytest.mark.parametrize("cle", ["websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"])
def test_les_quatre_liens_repondent_et_nomment_trustydata(interface, cle):
    url = interface[cle]
    assert url.startswith("https://trustydata.fr/")
    with urllib.request.urlopen(url, timeout=15) as r:
        corps = r.read(200_000).decode("utf-8", "replace")
    assert r.status == 200 and "TrustyData" in corps.split("</title>")[0]


def test_les_icones_sont_carrees_et_declarees(interface):
    for cle in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        chemin = RACINE / interface[cle]
        assert chemin.exists() and chemin.stat().st_size <= 5 * 1024 * 1024
        entete = chemin.read_bytes()[:24]
        assert entete[:8] == b"\x89PNG\r\n\x1a\n"
        largeur, hauteur = struct.unpack(">II", entete[16:24])
        assert largeur == hauteur >= 48


def test_les_icones_ont_un_fond_transparent_hors_de_la_pastille(interface):
    from PIL import Image
    for cle in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        image = Image.open(RACINE / interface[cle]).convert("RGBA")
        assert image.getpixel((0, 0))[3] == 0, f"{cle} : coin opaque, fond blanc aplati"
        assert image.getpixel((image.width // 2, 40))[:3] == (0x2D, 0x7B, 0xE5), f"{cle} : pastille bleue sous le visage"
