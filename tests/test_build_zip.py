"""Le constructeur du ZIP du plugin ChatGPT : liste blanche, chasse aux
secrets, URL de vidéo injectée au build seulement, nom versionné."""
import importlib.util
import json
import shutil
import zipfile

import pytest

from tests.test_plugin_manifest import RACINE

spec = importlib.util.spec_from_file_location("build_zip", RACINE / "build_zip.py")
build_zip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_zip)


def test_le_zip_ne_contient_que_la_liste_blanche(tmp_path):
    zip_path = build_zip.construire(RACINE, tmp_path, video_url="https://example.com/demo")
    noms = zipfile.ZipFile(zip_path).namelist()
    assert "plugin.json" in noms and "mcp.json" in noms and "skills/get-started/SKILL.md" in noms
    assert all(n.startswith(("plugin.json", "mcp.json", "skills/", "assets/")) for n in noms)
    assert not any(n.startswith(("schemas/", "build_zip.py", "dist/")) or ".DS_Store" in n for n in noms)


def test_la_video_est_injectee_dans_le_zip_seulement(tmp_path):
    zip_path = build_zip.construire(RACINE, tmp_path, video_url="https://example.com/demo")
    dans_zip = json.loads(zipfile.ZipFile(zip_path).read("plugin.json"))
    assert dans_zip["extensions"]["com.openai"]["review"]["demo_recording_url"] == "https://example.com/demo"
    sur_disque = json.loads((RACINE / "plugin.json").read_text(encoding="utf-8"))
    assert "demo_recording_url" not in sur_disque["extensions"]["com.openai"]["review"]


def test_un_fichier_etranger_ou_un_secret_fait_echouer(tmp_path):
    copie = tmp_path / "paquet"
    shutil.copytree(RACINE, copie)
    (copie / "skills" / "brouillon.txt").write_text("x", encoding="utf-8")
    with pytest.raises(SystemExit):
        build_zip.construire(copie, tmp_path, video_url=None)
    (copie / "skills" / "brouillon.txt").unlink()
    (copie / "skills" / "get-started" / "SKILL.md").write_text("token sk-ABCDEFGHIJKLMNOPQRSTUV", encoding="utf-8")
    with pytest.raises(SystemExit):
        build_zip.construire(copie, tmp_path, video_url=None)


def test_le_nom_du_zip_porte_la_version(tmp_path):
    version = json.loads((RACINE / "plugin.json").read_text(encoding="utf-8"))["version"]
    assert build_zip.construire(RACINE, tmp_path, None).name == f"trustydata-plugin-{version}.zip"


def _paquet(tmp_path):
    copie = tmp_path / "paquet"
    shutil.copytree(RACINE, copie)
    return copie


@pytest.mark.parametrize("secret", [
    "td_live_AbCdEfGhIjKlMnOpQrSt",
    "td_staging_AbCdEfGhIjKlMnOp",
    "sk-proj-AbCdEfGhIjKlMnOpQrStUvWxYz",
    "sk-ant-api03-AbCdEfGhIjKlMnOpQrStUv",
    "clientSecret",
    "test_credentials",
    "reviewer_instructions",
])
def test_les_vrais_formats_de_secrets_font_echouer(tmp_path, secret):
    copie = _paquet(tmp_path)
    skill = copie / "skills" / "get-started" / "SKILL.md"
    skill.write_text(skill.read_text(encoding="utf-8") + f"\n{secret}\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        build_zip.construire(copie, tmp_path, video_url=None)


@pytest.mark.parametrize("cle, fichier", [
    ("headers", "mcp.json"),
    ("clientSecret", "mcp.json"),
    ("test_credentials", "plugin.json"),
    ("reviewer_instructions", "plugin.json"),
])
def test_une_cle_interdite_dans_un_manifeste_fait_echouer(tmp_path, cle, fichier):
    copie = _paquet(tmp_path)
    chemin = copie / fichier
    contenu = json.loads(chemin.read_text(encoding="utf-8"))
    if fichier == "mcp.json":
        contenu["mcpServers"]["trustydata"][cle] = {"X": "y"} if cle == "headers" else "s"
    else:
        contenu["extensions"]["com.openai"].setdefault("review", {})[cle] = "s"
    chemin.write_text(json.dumps(contenu), encoding="utf-8")
    with pytest.raises(SystemExit):
        build_zip.construire(copie, tmp_path, video_url=None)


def test_une_cle_interdite_imbriquee_dans_le_bloc_auth_fait_echouer(tmp_path):
    """Le bloc `extensions.com.openai.auth` d'OpenAI ouvre une profondeur où une
    clé interdite peut se glisser. `headers` est choisi parce que la chasse aux
    secrets par texte ne le voit pas (un `clientSecret`, elle, l'attrape déjà) :
    seul le parcours récursif des clés du serveur peut refuser ce paquet."""
    copie = _paquet(tmp_path)
    chemin = copie / "mcp.json"
    contenu = json.loads(chemin.read_text(encoding="utf-8"))
    auth = contenu["mcpServers"]["trustydata"]["extensions"]["com.openai"]["auth"]
    auth["headers"] = {"X-Trace": "y"}  # valeur neutre : rien que la regex des secrets attraperait
    chemin.write_text(json.dumps(contenu), encoding="utf-8")
    with pytest.raises(SystemExit):
        build_zip.construire(copie, tmp_path, video_url=None)
