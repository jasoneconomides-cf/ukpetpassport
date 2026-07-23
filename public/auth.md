# /auth.md — Agent registration metadata for ukpetpassport.com
# Per https://workos.com/auth.md and https://github.com/workos/auth.md

# Site info
site:
  name: "UK Pet Passport"
  url: "https://ukpetpassport.com"
  description: "Free guidance website for UK pet owners navigating post-Brexit pet travel documentation requirements."
  contact: "resources@connectingpieces.com"

# Agent registration block (per workos/auth.md spec)
# Required for Auth.md agent registration check
agent_auth:
  enabled: false
  register_uri: ""
  supported_identity_types: []
  credential_types_supported: []
  claim_uri: ""
  revocation_uri: ""

# Authentication metadata
authentication:
  required: false
  oauth_discovery: "https://ukpetpassport.com/.well-known/openid-configuration"
  oauth_protected_resource: "https://ukpetpassport.com/.well-known/oauth-protected-resource"

# MCP and agent capabilities
agent_capabilities:
  mcp_server_card: "https://ukpetpassport.com/.well-known/mcp/server-card.json"
  agent_skills_index: "https://ukpetpassport.com/.well-known/agent-skills/index.json"
  api_catalog: "https://ukpetpassport.com/.well-known/api-catalog"
  llms_txt: "https://ukpetpassport.com/llms.txt"
  content_signals: "search=yes, ai-input=yes, ai-train=no"

# Notes for agents
notes: |
  This site is read-only guidance content. No authentication, no user accounts,
  no protected resources. All content is freely available to AI agents for reading
  and citation. AI training on this content is reserved (see Content Signals).