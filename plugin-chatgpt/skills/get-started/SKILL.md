---
name: get-started
description: Set up TrustyData in ChatGPT, check which plan the signed-in account has, and run five ready-made recipes on French addresses, companies and catchment areas.
---

# Get started with TrustyData

TrustyData answers from official French references: BAN and IGN for addresses, INSEE for communes and statistics, SIRENE, INPI and BODACC for companies, OpenStreetMap for routes. Every tool result is authoritative. An empty result means that nothing matches: never fill the gap from memory, never invent a population figure, a commune or a company.

## What this plugin does

- **Addresses**: `verify_address` checks one French postal address against the BAN and returns it split into three postal lines (`ligne_voie`, `ligne_complement`, `ligne_commune`), ready to paste. `search_address` searches by text, `get_address_details` gives the full record of an address, `search_nearby` lists addresses around a point.
- **Communes**: `search_locality` finds a commune by name, postal code or INSEE code.
- **Companies**: `search_company` searches the SIRENE registry; each hit is an establishment (one SIRET). `get_company_details` opens the full record of an establishment or a legal unit.
- **Catchment areas**: `zone_stats` profiles a zone defined by travel time or radius around an address; `zone_compare` compares two to ten zones.
- **Routes**: `compute_route` computes a road route, `route_matrix` a travel-time and distance matrix.

## Plans

The plugin uses the TrustyData account you signed in with. Create one at https://app.trustydata.app if you do not have one yet.

| Plan | What it opens |
|---|---|
| Discovery | Addresses, communes, companies |
| Growth | Discovery, plus catchment areas, proximity search and travel-time matrices |
| Business | Growth, plus full road routes |
| Pass Zones | Catchment areas, for a limited period |

A field missing from an answer may belong to a higher plan rather than not exist: say so instead of concluding that the data does not exist. Prompts cost nothing; tool calls count against the account's quota.

## Recipes

The server ships the same five recipes as MCP prompts. Each one names the tool to call and the one precaution that shapes the answer.

### 1. Catchment-area profile (`zone_de_chalandise`)

Inputs: an address or a commune name, a travel time from 1 to 30 minutes (default 10), a mode (`car`, `walking` or `cycling`, default `car`).

Call `zone_stats`. Present, in this order: population and households, average income, age profile, household and housing profile, socio-professional categories with their affinity index, then real-estate sale prices (apartments, houses, business premises; sale prices, never rents) and their trend. INSEE figures are estimates; the response carries an `attribution` block that accompanies every figure you quote.

### 2. Compare locations (`comparer_emplacements`)

Inputs: two to ten addresses or commune names separated by semicolons, one travel time applied to all.

Call `zone_compare`. Rank the locations on `exclusive_population`, the population each zone is alone to cover, not on total population: the gap between the two says what the locations take from each other. Point out the pairs that overlap the most.

### 3. Spending potential of a location (`potentiel_commerce`)

Inputs: an address or commune, a business sector in plain words (restaurant, bakery, gym), a travel time, and optionally a capture coefficient between 0 and 1.

Call `zone_stats`. Quote disposable income per household and present the theoretical potential for what it is: an estimate built on the residents' income, not a revenue forecast. Without a coefficient, pick the one matching the sector in the "Zone de chalandise" guide of the TrustyData documentation (restaurants ≈ 0.048), say which one you chose and why, and never invent a value.

### 4. Verify a list of addresses (`verifier_adresses`)

Input: addresses, one per line or separated by semicolons.

Call `verify_address` once per address: the tool handles one address per call. Return a table with the verdict (`match_exact`, `match_probable` or `aucun_match`) and the three postal lines exactly as the API returns them, without recomposing them. List separately the addresses with no match.

### 5. Qualify a company (`qualifier_entreprise`)

Input: a company name, a SIREN (9 digits) or a SIRET (14 digits), optionally a city to lift an ambiguity.

Call `search_company`, then `get_company_details` on the best hit. Report identity, activity, workforce, administrative status and, when served, executives and financial items. A search hit is an establishment, not a company: never count several establishments of one SIREN as several companies.

## Rules

- **France only**, overseas departments included. For an address or a company outside France, say that the coverage is France and stop; do not answer from memory.
- **One address per call**: verification is unitary. For a list, call the tool once per address.
- **Executives are personal data** from the INPI register. Their names are never a search criterion, and the plugin does not build prospecting lists. For each executive, relay `opposition_prospection`: `true` means the person refused commercial solicitation, `false` that no opposition is recorded, `null` that the information is not available. `null` is not `false`.
- **Two confidentiality flags mean different things**: `diffusible: false` comes from the INSEE and masks a company's name and address by law; `opposition_prospection` comes from the INPI and concerns a person.
- **Always relay `attribution`** with every figure quoted (BAN/INSEE and IGN for addresses, SIRENE and INPI for companies, OSM ODbL for routes and isochrones).
- Catchment-area statistics describe the INSEE 200 m grid around a point, not the occupants of a given building.
- Full documentation: https://trustydata.fr/docs/
