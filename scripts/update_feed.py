#!/usr/bin/env python3
"""Fetch and validate the upstream public V2Ray subscription; preserve last good output on failure."""
from __future__ import annotations
import base64
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE = "https://raw.githubusercontent.com/Au1rxx/free-vpn-subscriptions/main/output/v2ray-base64.txt"
OUT = Path("output")
SCHEMES = ("vless://", "vmess://", "trojan://", "ss://", "socks://", "wireguard://", "hysteria2://", "tuic://", "hy2://", "anytls://")
MIN_NODES = 5

def has_links(value: str) -> bool:
    low = value.lower()
    return any(s in low for s in SCHEMES)

def main() -> int:
    req = Request(SOURCE, headers={"User-Agent": "FreeVPN-Subscription-Mirror/1.0"})
    with urlopen(req, timeout=45) as response:
        payload = response.read(12 * 1024 * 1024 + 1)
    if len(payload) > 12 * 1024 * 1024:
        raise RuntimeError("Upstream feed exceeds 12 MiB safety limit")
    raw_text = payload.decode("utf-8-sig", errors="strict").strip()
    decoded_text = raw_text
    try:
        candidate = base64.b64decode(re.sub(r"\\s+", "", raw_text) + "=" * (-len(re.sub(r"\\s+", "", raw_text)) % 4), validate=False).decode("utf-8-sig")
        if has_links(candidate):
            decoded_text = candidate
    except (ValueError, UnicodeDecodeError):
        pass
    if not has_links(decoded_text):
        raise RuntimeError("Upstream did not contain recognizable proxy links; refusing to replace the previous feed")
    lines = []
    seen = set()
    for line in decoded_text.splitlines():
        item = line.strip().lstrip("\ufeff")
        if item.lower().startswith(SCHEMES) and item not in seen:
            seen.add(item)
            lines.append(item)
    if len(lines) < MIN_NODES:
        raise RuntimeError(f"Only {len(lines)} valid-looking entries found; keeping previous feed")
    OUT.mkdir(parents=True, exist_ok=True)
    plain = "\n".join(lines) + "\n"
    encoded = base64.b64encode(plain.encode("utf-8")).decode("ascii") + "\n"
    (OUT / "v2ray.txt").write_text(plain, encoding="utf-8")
    (OUT / "v2ray-base64.txt").write_text(encoded, encoding="ascii")
    status = {
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": SOURCE,
        "nodes": len(lines),
        "validation": "URI scheme and minimum-count validation only; upstream performs its own connectivity tests",
        "warning": "Public third-party nodes; not a private VPN server; no guarantee of availability or censorship resistance"
    }
    (OUT / "status.json").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {len(lines)} unique proxy links from upstream.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
