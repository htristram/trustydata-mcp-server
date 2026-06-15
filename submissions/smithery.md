# Smithery submission kit

TrustyData is an **already-hosted remote MCP server**. Smithery proxies to it
("bring your own hosting") — no `smithery.yaml`, no Smithery deployment.

## Steps

1. Go to **https://smithery.ai/new** and sign in with GitHub.
2. Enter the public server URL: `https://mcp.trustydata.app/mcp`
3. Smithery auto-scans the live server and detects the tools. It supports
   Streamable HTTP + OAuth, so the OAuth sign-in prompt is surfaced at connect time.
4. Fill the listing metadata using the copy below.

## Listing metadata

| Field | Value |
|---|---|
| **Display name** | TrustyData |
| **Server URL** | `https://mcp.trustydata.app/mcp` |
| **Transport** | Streamable HTTP |
| **Auth** | OAuth 2.1 — sign in with a TrustyData account |
| **Homepage** | https://trustydata.fr |
| **Documentation** | https://trustydata.fr/docs/ |
| **Repository** | https://github.com/htristram/trustydata-mcp-server |

**Tagline (short)**

> French address quality, geocoding & routing from official data (BAN, INSEE, OpenStreetMap).

**Description (long)**

> TrustyData connects your LLM to authoritative French address data. Verify and
> normalize postal addresses against the official BAN reference, search addresses
> and communes by name / postal code / INSEE code, run proximity searches, and
> compute road routes or travel-time/distance matrices in France. Data comes from
> official, regularly-updated open sources — BAN and INSEE for addresses and
> communes, OpenStreetMap (ODbL) for routing. Results are authoritative: an empty
> result means no match, never a guess.

**Tags / categories**

```
address-validation, geocoding, france, routing, maps, data-quality,
ban, insee, openstreetmap
```

**Tools (auto-detected by Smithery; min plan for reference)**

| Tool | Description | Min plan |
|---|---|---|
| `verify_address` | Verify & normalize a French address against the BAN | Discovery |
| `search_address` | Autocomplete / search full addresses | Discovery |
| `get_address_details` | Full detail for a given address id | Discovery |
| `search_locality` | Search French communes / localities | Discovery |
| `search_nearby` | Proximity search around a point | Growth |
| `route_matrix` | Travel-time / distance matrix | Growth |
| `compute_route` | Full road route between points | Business |

**Example prompts**

```
Vérifie et normalise cette adresse : "1 rue de Rivol 75001 Pari"
Quelle est la population de la commune de Bourg-en-Bresse ?
Trouve les adresses proches du 2 avenue de la Gare à Annecy.
Calcule l'itinéraire routier entre Lyon Part-Dieu et l'aéroport Saint-Exupéry.
```

## Optional — richer auto-metadata

Smithery (and other crawlers) can read an optional **server card** at
`https://mcp.trustydata.app/.well-known/mcp/server-card.json`. If we want full
control over the scanned metadata (title, description, icon, links), expose that
file from the MCP host. Not required — the live scan already extracts the tools.
