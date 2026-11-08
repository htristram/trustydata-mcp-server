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


# Menu déroulant « Category » du portail OpenAI, relevé le 2026-11-08 ; la liste
# n'est publiée nulle part dans la documentation. Le portail bloque toute autre valeur.
CATEGORIES_PORTAIL = {"Productivity", "Creativity", "Developer Tools", "Business & Operations",
                      "Data & Analytics", "Communication", "Education & Research", "Security",
                      "Finance", "Healthcare", "Travel", "Entertainment", "Other"}


@pytest.fixture(scope="module")
def manifeste():
    return json.loads((RACINE / "plugin.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def openai(manifeste):
    return manifeste["extensions"]["com.openai"]


@pytest.fixture(scope="module")
def interface(openai):
    return openai["interface"]


def test_le_manifeste_respecte_le_schema_agent_plugins(manifeste):
    schema = json.loads((RACINE / "schemas" / "plugin.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(manifeste, schema)


def test_la_configuration_mcp_pointe_le_seul_serveur_de_production():
    mcp = json.loads((RACINE / "mcp.json").read_text(encoding="utf-8"))
    assert list(mcp["mcpServers"]) == ["trustydata"]
    serveur = mcp["mcpServers"]["trustydata"]
    assert set(serveur) == {"type", "url", "extensions"}, "ni headers ni secret"
    assert serveur["type"] == "streamable-http" and serveur["url"] == "https://mcp.trustydata.app/mcp"
    # Déclaration d'authentification propre à OpenAI (developers.openai.com/plugins/build/plugins,
    # « Declare authentication under each server's extensions["com.openai"].auth object ») :
    # sans elle, ChatGPT installe le plugin comme un serveur sans authentification et ne
    # propose jamais la connexion (constaté le 2026-11-08). DCR : le mode prouvé avec Scalekit.
    assert serveur["extensions"] == {"com.openai": {"auth": {"type": "oauth", "client": {"mode": "dcr"}}}}


def test_les_limites_de_la_fiche(interface):
    assert interface["displayName"] == "TrustyData" and len(interface["shortDescription"]) <= 30
    assert len(interface["longDescription"]) <= 4000 and len(interface["developerName"]) <= 80
    prompts = interface["defaultPrompt"]
    assert 1 <= len(prompts) <= 3 and all(len(p) <= 128 and "@" not in p for p in prompts)
    assert all(re.fullmatch(r"#[0-9A-Fa-f]{6}", interface[c]) for c in ("brandColor", "brandColorDark"))
    assert interface["category"] in CATEGORIES_PORTAIL
    assert interface["category"] == "Data & Analytics"


def test_la_fiche_nomme_les_sources(interface):
    texte = interface["longDescription"]
    for mot in ("BAN", "INSEE", "SIRENE", "INPI", "OpenStreetMap", "France"):
        assert mot in texte
    assert "opposition_prospection" in texte


# Finding du portail OpenAI (2026-11-08, non bloquant) : « Remove pricing,
# subscription offers, and temporary promotions from the description ». Les
# plans se lisent sur le site, la fiche dit seulement que l'accès dépend du compte.
VENTE = [r"\bDiscovery\b", r"\bGrowth\b", r"\bBusiness plan\b", r"plan Business", r"\bPass Zones\b",
         r"\bfree\b", r"\bgratuit", r"\b15[- ]day", r"\b15 jours", r"subscription", r"abonnement", r"€"]

# Finding du portail (même jour) : « Remove or revise promises and guarantees
# that the plugin's functionality does not support ». Comportements non prouvés
# ou faux (OSM n'est pas une institution française), et le mot « normaliser »
# qui frôle l'interdit RNVP.
PROMESSES = [r"returns no result", r"ne rend aucun r[ée]sultat", r"model's memory", r"m[ée]moire du mod[èe]le",
             r"\bnormali[sz]e", r"French institution", r"institution fran[çc]aise"]


def _textes_de_la_fiche(openai):
    inter, pub = openai["interface"], openai["publication"]
    yield "longDescription", inter["longDescription"]
    yield "shortDescription", inter["shortDescription"]
    yield "capabilities", "\n".join(inter["capabilities"])
    for langue, tr in pub["translations"].items():
        yield f"{langue}.description", tr["description"]
        yield f"{langue}.subtitle", tr["subtitle"]


@pytest.mark.parametrize("motif", VENTE)
def test_la_fiche_ne_vend_aucun_plan(openai, motif):
    for nom, texte in _textes_de_la_fiche(openai):
        assert not re.search(motif, texte), f"{motif!r} dans {nom}"


@pytest.mark.parametrize("motif", PROMESSES)
def test_la_fiche_ne_promet_rien_d_invérifiable(openai, motif):
    for nom, texte in _textes_de_la_fiche(openai):
        assert not re.search(motif, texte, re.IGNORECASE), f"{motif!r} dans {nom}"


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
