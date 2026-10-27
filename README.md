# FreeVPN Subscription Mirror

A free, automatically refreshed mirror of **public third-party proxy configurations** for v2rayN (Windows) and v2rayNG (Android).

> This is **not your own VPN server**. It mirrors public community nodes; operators are unknown and nodes can disappear or be blocked. It cannot guarantee service during a complete international-internet shutdown.

## Subscription

After the first successful GitHub Actions run, use this URL in both clients:

`https://raw.githubusercontent.com/pctaha501-create/FreeVPN-Subscription-Mirror/main/output/v2ray-base64.txt`

Plain-text links (for troubleshooting/import where supported):

`https://raw.githubusercontent.com/pctaha501-create/FreeVPN-Subscription-Mirror/main/output/v2ray.txt`

Status/count:

`https://raw.githubusercontent.com/pctaha501-create/FreeVPN-Subscription-Mirror/main/output/status.json`

## How it works

- GitHub Actions refreshes the feed every 6 hours and can also be started manually from **Actions → Refresh public subscription → Run workflow**.
- The upstream project performs its own TCP/TLS/config checks and HTTP-over-proxy tests before publishing nodes.
- This repository checks that the downloaded feed decodes into actual supported proxy links and contains a minimum number of entries. It keeps the previous output if the upstream feed is empty or malformed.
- The workflow commits output only when it changes.

## Setup

### Windows — v2rayN
1. Open **Subscriptions / Subscription group settings**.
2. Add a subscription with the URL above.
3. Update subscriptions, then select a working node and connect.

### Android — v2rayNG
1. Open **Subscriptions** and tap **+**.
2. Paste the same URL.
3. Save, update subscription, choose a working node, then connect.

Menu names may differ by client version.

## Security and reliability

- Public proxy operators may observe metadata and potentially unencrypted traffic. Do not use these nodes for banking, sensitive accounts, or confidential activity.
- HTTPS protects the contents of properly encrypted connections, but does not make an unknown proxy operator trustworthy.
- A node that works from GitHub's runner may be blocked or unreachable from your network. Try another node if one fails.
- GitHub itself must be reachable to update the subscription. If GitHub and all routes to international hosts are blocked, this feed cannot restore connectivity on its own.
- Free community nodes are temporary and are not a substitute for a private, personally controlled VPN server.

Upstream feed: [Au1rxx/free-vpn-subscriptions](https://github.com/Au1rxx/free-vpn-subscriptions). This mirror does not operate or own the upstream servers.
