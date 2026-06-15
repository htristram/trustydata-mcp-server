# TrustyData MCP Server

Connect your LLM (Claude, ChatGPT, IDE assistants…) to **[TrustyData](https://trustydata.fr)** —
French **address data quality**, geocoding and routing, built on official open
data sources (**BAN**, **INSEE**, **OpenStreetMap**).

This is a **hosted, remote MCP server** — there is nothing to install or run.
Point your MCP client at the endpoint below and sign in with your TrustyData
account.

| | |
|---|---|
| **Endpoint** | `https://mcp.trustydata.app/mcp` |
| **Transport** | Streamable HTTP |
| **Auth** | OAuth 2.1 (sign in with your TrustyData account) |
| **Docs** | https://trustydata.fr/docs/ |
| **Status** | https://status.trustydata.app |

> This repository hosts the **public listing metadata** for the TrustyData MCP
> server (`server.json`, documentation, examples). The server itself is a hosted
> service — the source of the underlying data API is not part of this repo.

## What it does

TrustyData turns messy French addresses into clean, authoritative data and adds
geographic context, directly inside your LLM conversation:

- **Verify & normalize** a French postal address against the official **BAN**
  reference (the result is authoritative — an empty result means no match).
- **Search** addresses and localities by name, postal code or INSEE code, with
  optional filters (department, region, population).
- **Proximity search** — find addresses or points near a location.
- **Routing** — compute a road route or a travel-time/distance matrix in France
  (OpenStreetMap).

Richer fields (e.g. INSEE Filosofi statistical grid, Lambert 93 coordinates) are
returned depending on your plan.

## Tools

| Tool | What it does | Minimum plan |
|---|---|---|
| `verify_address` | Verify & normalize a French address against the BAN | Discovery |
| `search_address` | Autocomplete / search full addresses | Discovery |
| `get_address_details` | Full detail for a given address id | Discovery |
| `search_locality` | Search French communes / localities | Discovery |
| `search_nearby` | Proximity search around a point | Growth |
| `route_matrix` | Travel-time / distance matrix | Growth |
| `compute_route` | Full road route between points | Business |

All tools are advertised to every client. If your plan doesn't cover a tool, it
returns an actionable upgrade message instead of failing silently.

## Connect

### Claude (claude.ai / Claude Desktop)

Add a **custom connector** pointing to:

```
https://mcp.trustydata.app/mcp
```

You'll be prompted to sign in via OAuth with your TrustyData account the first
time a tool is used.

### Generic MCP client (Streamable HTTP)

```json
{
  "mcpServers": {
    "trustydata": {
      "url": "https://mcp.trustydata.app/mcp"
    }
  }
}
```

Don't have an account yet? Start free on
**[trustydata.fr](https://trustydata.fr)** (15-day trial, no card).

## Example prompts

```
Vérifie et normalise cette adresse : "1 rue de Rivol 75001 Pari"

Quelle est la population de la commune de Bourg-en-Bresse ?

Trouve les adresses proches du 2 avenue de la Gare à Annecy.

Calcule l'itinéraire routier entre Lyon Part-Dieu et l'aéroport Saint-Exupéry.
```

## Data sources & attribution

TrustyData relies on official, regularly-updated open data. Please keep the
attributions returned by the tools:

- **Addresses & communes** — Base Adresse Nationale (BAN) & INSEE
- **Statistical context** — INSEE Filosofi
- **Routing** — OpenStreetMap contributors (ODbL)

## Documentation

Full API guides, endpoint reference and examples:
**https://trustydata.fr/docs/**

## License

The contents of this listing repository (documentation, `server.json`, examples)
are released under the [MIT License](./LICENSE). The hosted service and the
underlying data API are operated by TrustyData and governed by its terms.
