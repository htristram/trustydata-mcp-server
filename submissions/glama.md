# Glama submission kit

Target: **glama.ai/mcp/servers**. Glama grades servers (A–F) on security and
quality signals — this repo is optimized for a good grade (MIT license, README,
public status page, OAuth).

## Steps

1. Go to https://glama.ai/mcp/servers and sign in (GitHub).
2. Submit / claim the server. If Glama already indexed it from the official
   registry or GitHub (`mcp-server` topic), **claim** the existing listing
   instead of creating a duplicate.
3. Fill the metadata below.

## Listing metadata

| Field | Value |
|---|---|
| **Name** | TrustyData |
| **Server URL** | `https://mcp.trustydata.app/mcp` |
| **Transport** | Streamable HTTP |
| **Auth** | OAuth 2.1 |
| **Repository** | https://github.com/htristram/trustydata-mcp-server |
| **Homepage** | https://trustydata.fr/usecases/mcp-qualite-donnees |
| **Live demo** | https://trustydata.fr/demo/mcp-agent |

**Description (reliability/security angle — Glama audience)**

> A hosted remote MCP server for French address data, built for reliability:
> OAuth 2.1 (no API keys pasted into clients), Streamable HTTP, EU hosting with
> a public status page (status.trustydata.app). Tools cover address verification
> against the official BAN registry, geocoding (WGS84/Lambert 93), INSEE
> territorial enrichment, proximity search, road routing, company lookup in the
> official SIRENE registry and catchment-area statistics (INSEE). Results are
> authoritative: an empty result means no match, never a guess. Free tier
> available (5,000 requests/month).

**Tags**: `address-validation, geocoding, france, routing, data-quality, ban, insee, openstreetmap, sirene, company-data, catchment-area`
