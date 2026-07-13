# Official MCP Registry submission kit

Target: **registry.modelcontextprotocol.io** (Linux Foundation). Do this one
**first** — several aggregators (PulseMCP, Glama…) index it.

The manifest is already in this repo: [`server.json`](../server.json)
(namespace `app.trustydata/trustydata`, schema 2025-12-11).

## Steps

1. Install the publisher CLI:
   ```bash
   brew install mcp-publisher
   # or grab a binary from github.com/modelcontextprotocol/registry
   ```
2. Authenticate the `app.trustydata` namespace (reverse-DNS → DNS verification):
   ```bash
   mcp-publisher login dns --domain trustydata.app
   # add the TXT record it prints to the trustydata.app DNS zone
   ```
3. Publish from the repo root:
   ```bash
   mcp-publisher publish
   ```

**No-DNS fallback:** rename the namespace in `server.json` to
`io.github.htristram/trustydata` and use `mcp-publisher login github` instead.
Less on-brand, zero DNS friction.

## After publishing

- Verify the listing at registry.modelcontextprotocol.io.
- Check within a few days whether PulseMCP / Glama picked it up automatically
  before submitting to them manually.
