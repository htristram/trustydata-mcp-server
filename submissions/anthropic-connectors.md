# Anthropic connector directory submission kit

Target: the **claude.ai connector directory** — the highest-leverage listing
for non-developer users (they discover and enable connectors directly inside
Claude). Submissions go through an Anthropic form with a trust & safety review;
check the current process in Anthropic's developer docs.

## Prerequisites (all ✅)

| Requirement | Value |
|---|---|
| Remote MCP server, OAuth | `https://mcp.trustydata.app/mcp` (OAuth 2.1) |
| Privacy policy | https://trustydata.fr/politique-confidentialite |
| Terms | https://trustydata.fr/cgu |
| Support contact | https://trustydata.fr/contact |
| Legal notice | https://trustydata.fr/mentions-legales |

## Listing copy — FR (primary audience)

> Validez, géolocalisez et enrichissez des adresses françaises directement dans
> Claude. TrustyData s'appuie exclusivement sur les référentiels officiels (BAN,
> INSEE, IGN, OpenStreetMap) : vérification d'adresse, coordonnées GPS, code
> IRIS, données socio-démographiques de quartier, itinéraires routiers. Aucun
> code à écrire — connectez-vous et posez votre question. Plan gratuit : 5 000
> requêtes/mois.

## Listing copy — EN

> Verify, geocode and enrich French addresses directly inside Claude.
> TrustyData relies exclusively on official French reference data (BAN, INSEE,
> IGN, OpenStreetMap): address verification, GPS coordinates, INSEE territorial
> codes, neighborhood-level demographics and road routing. No code required —
> sign in and ask. Free plan: 5,000 requests/month.

## Example prompts to include

```
Vérifie cette adresse : "215 acac ste euphemie"
Quel est le code IRIS du 12 rue de la République à Lyon ?
Compare les temps de trajet entre ces trois agences et le centre de Dijon.
```
