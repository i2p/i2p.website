#!/usr/bin/env python3
"""Set Hugo aliases on content files so old/moved paths redirect to current pages.

This script is the single source of truth for aliases: it rewrites the
aliases of every content file in all 13 languages to match ALIAS_PATHS and
BARE_ALIASES below, and removes aliases that are not listed. To add or
change a redirect, edit the lists here and re-run; do not hand-edit aliases
in content files.

Hugo alias behavior with defaultContentLanguageInSubdir = true:
- Absolute aliases (leading /) are used as-is for the redirect path
- So we must include the language prefix: /en/docs/protocol/i2cp
- Each language's content file gets its own language-prefixed aliases

The translation pipeline (scripts/translate) rewrites /en/ aliases to the
target language when it translates a page, so translations stay in sync.

Usage: add_aliases.py [--dry-run]
"""
import os
import re
import sys

LANGUAGES = ["en", "ar", "cs", "de", "es", "fr", "hi", "ko", "pt", "ru", "tr", "vi", "zh"]

# Alias paths WITHOUT language prefix — the script prepends /{lang}/ for each language.
# Both trailing-slash and non-trailing-slash variants are generated.
ALIAS_PATHS = [
    # --- Original aliases (from broken internal links) ---
    ("docs/specs/i2cp-overview.md", ["docs/protocol/i2cp"]),
    ("docs/specs/i2cp.md", ["docs/api/i2cp", "docs/specs/i2cp-spec"]),
    ("docs/specs/i2np-overview.md", ["docs/protocol/i2np"]),
    ("docs/specs/i2np.md", ["spec/i2np"]),
    ("docs/legacy/ntcp.md", ["docs/transport/ntcp", "docs/ntcp"]),
    ("docs/legacy/ssu.md", [
        "docs/transport/ssu",
        "docs/transports/ssu",
        "docs/specs/ssu-spec",
    ]),
    ("docs/legacy/bob.md", ["docs/api/bob"]),
    ("docs/legacy/sam.md", ["docs/api/sam"]),
    ("docs/legacy/samv2.md", ["docs/api/samv2"]),
    ("docs/applications/git-bundle.md", ["docs/applications/git"]),
    ("docs/overview/performance.md", [
        "about/performance/future",
        "about/performance/history",
    ]),
    # --- docs/develop/* → docs/development/* (renamed section) ---
    ("docs/development/_index.md", ["docs/develop"]),
    ("docs/development/protocol-stack.md", ["docs/develop/protocol-stack"]),
    ("docs/development/security-key.md", ["docs/develop/security-key"]),
    ("docs/development/applications.md", ["docs/develop/applications"]),
    ("docs/development/dev-guidelines.md", ["docs/develop/dev-guidelines"]),
    ("docs/development/licenses.md", ["docs/develop/licenses"]),
    ("docs/development/new-translators.md", ["docs/develop/new-translators"]),
    ("docs/development/release-signing-key.md", ["docs/develop/release-signing-key"]),
    ("docs/development/new-developers.md", ["docs/develop/new-developers", "newdevelopers"]),
    ("docs/development/overview.md", ["docs/develop/overview"]),
    # --- docs/legacy/* → current locations ---
    ("docs/specs/tunnel-message.md", ["docs/legacy/tunnel-message"]),
    ("docs/historical/naming.md", ["docs/legacy/naming"]),
    ("docs/historical/netdb.md", ["docs/legacy/netdb"]),
    # --- docs/specs/* and docs/overview/* old paths ---
    ("docs/specs/tunnel-implementation.md", ["docs/specs/implementation"]),
    ("docs/overview/naming.md", ["docs/specs/naming", "docs/naming"]),
    # --- docs/specs/* old slug names ---
    ("docs/specs/red25519.md", ["docs/specs/red25519-signature-scheme"]),
    ("docs/specs/b32encrypted.md", ["docs/specs/b32-for-encrypted-leasesets"]),
    ("docs/specs/udp-announces.md", ["docs/specs/udp-bittorrent-announces"]),
    ("docs/specs/ecies.md", ["docs/specs/ecies-x25519-aead-ratchet"]),
    ("docs/specs/subscription.md", ["docs/specs/subscription-spec"]),
    ("docs/specs/tunnel-creation-ecies.md", ["docs/specs/tunnel-creation-ecies-spec"]),
    # --- docs/historical/* old paths ---
    ("docs/legacy/old-tunnel-implementation.md", ["docs/historical/tunnel-alt"]),
    ("docs/historical/ntcp-discussion.md", ["docs/discussions/ntcp"]),
    ("docs/historical/tunnel.md", ["docs/discussions/tunnel"]),
    # --- docs/guides renamed pages ---
    ("docs/guides/macos-install.md", ["docs/guides/installing-i2p-on-macos-the-long-way"]),
    # --- get-involved ---
    ("get-involved/roadmap.md", ["get-involved/todo"]),
    # --- Proposals with old/shortened slugs ---
    ("proposals/111-ntcp-2.md", ["proposals/111-ntcp2"]),
    ("proposals/119-bidirectional-tunnels.md", ["proposals/119"]),
    ("proposals/142-new-crypto-template.md", ["proposals/142-ecies-template"]),
    ("proposals/143-build-message-options.md", ["proposals/143"]),
    ("proposals/144-ecies-x25519-aead-ratchet.md", ["proposals/144-ecies-x25519"]),
    ("proposals/145-ecies.md", ["proposals/145-ecies-ecdh-aes"]),
    ("proposals/152-ecies-tunnels.md", ["proposals/152-ecies-config", "proposals/152"]),
    ("proposals/153-chacha20-layer-encryption.md", ["proposals/153-chacha20-layer", "proposals/153"]),
    ("proposals/154-ecies-lookups.md", ["proposals/154-ratchet"]),
    ("proposals/156-ecies-routers.md", ["proposals/156"]),
    ("proposals/157-new-tbm.md", ["proposals/157"]),
    ("proposals/163-datagram2.md", ["proposals/163-datagram2-datagram3"]),
    ("proposals/168-tunnel-bandwidth.md", ["proposals/168"]),
    # --- spec/proposals/* → proposals/* (wrong parent path) ---
    ("proposals/126-ipv6-peer-testing.md", ["spec/proposals/126-ipv6-peer-testing"]),
    ("proposals/158-ipv6-transport-enhancements.md", ["spec/proposals/158"]),
    # --- Legacy short URLs from the old site (i2p.www i2p2www/legacy.py) ---
    # Still linked from router consoles and installers, e.g. /htproxyports.
    # Not mapped (no current equivalent, left as 404): clt, jbigi, jrandom-awol,
    # links, manualwrapper, minwww, myi2p, pressetext-0.7, ratestats, ticket919,
    # ticket1056, transition-guide, transition-guide.txt, upgrade-0.6.1.30
    # Downloads and blog
    ("downloads/_index.md", [
        "d", "get", "download", "installation", "lab",
        "windows", "mac", "macos", "easyinstall", "nsis",
    ]),
    ("docs/guides/debian-ubuntu-install.md", ["debian"]),
    ("docs/guides/browser-config.md", ["firefox", "htproxyports"]),
    ("blog/_index.md", ["announcements", "statusnotes", "meetings"]),
    # About and get involved
    ("about/_index.md", ["team"]),
    ("about/hall-of-fame.md", ["halloffame"]),
    ("contact/_index.md", ["impressum"]),
    ("get-involved/_index.md", ["getinvolved", "bounties"] + [
        f"bounty_{b}" for b in (
            "arabic", "btcclient", "datastore", "debpack", "i2phex", "ipv6",
            "netdb", "rutrans", "silc", "syndie2012", "unittests", "vuzeplugin",
        )
    ]),
    ("get-involved/roadmap.md", ["roadmap", "todo"]),
    ("misc/invisiblenet.md", ["invisiblenet"]),
    # Development
    ("docs/development/applications.md", ["applications"]),
    ("docs/development/dev-guidelines.md", ["dev-guidelines"]),
    ("docs/development/licenses.md", ["licenses", "license-agreements"]),
    ("docs/development/new-developers.md", ["cvs", "monotone"]),
    ("docs/development/new-translators.md", ["newtranslators"]),
    ("docs/development/release-signing-key.md", [
        "release-signing-key", "developerskeys", "signedkeys",
    ]),
    ("docs/development/protocol-stack.md", ["protocols"]),
    # Overview
    ("docs/_index.md", ["how"]),
    ("docs/overview/intro.md", ["intro", "how_intro"]),
    ("docs/overview/tech-intro.md", ["techintro"]),
    ("docs/overview/glossary.md", ["glossary"]),
    ("docs/overview/garlic-routing.md", ["how_garlicrouting"]),
    ("docs/overview/comparison.md", ["how_networkcomparisons", "othernetworks"]),
    ("docs/overview/network-database.md", ["how_networkdatabase"]),
    ("docs/overview/peer-selection.md", ["how_peerselection"]),
    ("docs/overview/threat-model.md", ["how_threatmodel"]),
    ("docs/overview/tunnel-routing.md", ["how_tunnelrouting"]),
    ("docs/overview/naming.md", ["naming"]),
    ("docs/overview/performance.md", ["performance", "performance-history", "benchmarks"]),
    ("docs/overview/ports.md", ["ports"]),
    ("docs/overview/transport.md", ["transport"]),
    # APIs and applications
    ("docs/api/_index.md", ["api"]),
    ("docs/api/datagrams.md", ["datagrams"]),
    ("docs/api/i2pcontrol.md", ["i2pcontrol"]),
    ("docs/api/i2ptunnel.md", ["i2ptunnel", "i2ptunnel_migration", "i2ptunnel_services"]),
    ("docs/api/samv3.md", ["samv3"]),
    ("docs/api/socks.md", ["socks"]),
    ("docs/api/streaming.md", ["streaming"]),
    ("docs/applications/_index.md", ["supported_applications"]),
    ("docs/applications/bittorrent.md", ["bittorrent"]),
    ("docs/guides/plugins.md", ["plugins"]),
    # Specs
    ("docs/specs/blockfile.md", ["blockfile"]),
    ("docs/specs/common-structures.md", ["common_structures_spec"]),
    ("docs/specs/configuration.md", ["configuration"]),
    ("docs/specs/cryptography.md", ["how_cryptography"]),
    ("docs/specs/elgamal-aes.md", ["how_elgamalaes"]),
    ("docs/specs/elgamal-tunnel-creation.md", ["tunnel-alt-creation"]),
    ("docs/specs/i2cp-overview.md", ["i2cp"]),
    ("docs/specs/i2cp.md", ["i2cp_spec"]),
    ("docs/specs/i2np-overview.md", ["i2np"]),
    ("docs/specs/i2np.md", ["i2np_spec"]),
    ("docs/specs/plugin.md", ["plugin_spec"]),
    ("docs/specs/tunnel-implementation.md", ["tunnel-alt"]),
    ("docs/specs/tunnel-message.md", ["tunnel_message_spec"]),
    ("docs/specs/updates.md", ["updates"]),
    # Legacy and historical docs
    ("docs/legacy/bob.md", ["bob"]),
    ("docs/legacy/geoip.md", ["geoip"]),
    ("docs/legacy/ministreaming.md", ["ministreaming"]),
    ("docs/legacy/ntcp.md", ["ntcp"]),
    ("docs/legacy/old-tunnel-implementation.md", ["tunnel"]),
    ("docs/legacy/sam.md", ["sam"]),
    ("docs/legacy/samv2.md", ["samv2"]),
    ("docs/legacy/ssu-overview.md", ["udp"]),
    ("docs/legacy/ssu.md", ["udp_spec"]),
    ("docs/legacy/unidirectional-tunnels.md", ["unidirectional-tunnels"]),
    ("docs/historical/naming.md", ["naming_discussion"]),
    ("docs/historical/netdb.md", ["netdb_discussion"]),
    ("docs/historical/ntcp-discussion.md", ["ntcp_discussion"]),
    ("docs/historical/tunnel.md", ["tunnel_discussion"]),
]

# Bare-path aliases for URLs without a language prefix (e.g., www.i2p.net/docs/...).
# These are added to the ENGLISH file only (no /{lang}/ prefix) so Hugo creates
# a redirect from the bare path to the English version.
BARE_ALIASES = [
    ("docs/specs/common-structures.md", ["docs/specs/common-structures"]),
    ("docs/api/samv3.md", ["docs/api/samv3"]),
    ("docs/api/streaming.md", ["docs/api/streaming"]),
    ("docs/specs/ecies.md", ["docs/specs/ecies"]),
    ("docs/specs/ecies-hybrid.md", ["docs/specs/ecies-hybrid"]),
    ("docs/specs/ecies-routers.md", ["docs/specs/ecies-routers"]),
    ("proposals/134-gost.md", ["proposals/134-gost"]),
    ("proposals/169-pq-crypto.md", ["proposals/169-pq-crypto"]),
    ("docs/development/_index.md", ["docs/develop"]),
    ("docs/development/dev-guidelines.md", ["docs/develop/dev-guidelines"]),
    ("docs/development/licenses.md", ["docs/develop/licenses"]),
    ("docs/development/new-developers.md", ["docs/develop/new-developers"]),
    ("docs/development/new-translators.md", ["docs/develop/new-translators"]),
    ("docs/development/overview.md", ["docs/development/overview"]),
    ("docs/development/protocol-stack.md", ["docs/develop/protocol-stack"]),
    ("docs/development/release-signing-key.md", ["docs/develop/release-signing-key"]),
    ("docs/development/security-key.md", ["docs/develop/security-key"]),
    ("docs/legacy/ssu.md", ["docs/specs/ssu-spec"]),
    ("docs/specs/ecies.md", ["docs/specs/ecies-x25519-aead-ratchet"]),
    ("docs/specs/i2cp.md", ["docs/specs/i2cp-spec"]),
    ("docs/specs/i2np.md", ["spec/i2np"]),
    ("docs/specs/subscription.md", ["docs/specs/subscription-spec"]),
    ("docs/specs/tunnel-creation-ecies.md", ["docs/specs/tunnel-creation-ecies-spec"]),
]


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
ALIASES_BLOCK_RE = re.compile(r"^aliases:[ \t]*\n(?:[ \t]+-[ \t]+.*\n?)*", re.MULTILINE)
ALIASES_INLINE_RE = re.compile(r"^aliases:[ \t]*\[[^\]]*\][ \t]*\n?", re.MULTILINE)


def read_aliases(frontmatter):
    """Return the aliases in a frontmatter string, or None if there is no aliases key."""
    block = ALIASES_BLOCK_RE.search(frontmatter + "\n")
    if block:
        return [line.strip()[1:].strip().strip("'\"")
                for line in block.group(0).split("\n")[1:] if line.strip().startswith("-")]
    inline = ALIASES_INLINE_RE.search(frontmatter + "\n")
    if inline:
        items = inline.group(0).split("[", 1)[1].rsplit("]", 1)[0]
        return [i.strip().strip("'\"") for i in items.split(",") if i.strip()]
    return None


def set_aliases_in_file(filepath, aliases, dry_run=False):
    """Make a file's aliases exactly `aliases`. Returns (added, removed), or None if unchanged."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fm_match = FRONTMATTER_RE.match(content)
    if not fm_match:
        return None

    frontmatter = fm_match.group(1)
    existing = read_aliases(frontmatter)
    if existing == aliases or (existing in (None, []) and not aliases):
        return None

    aliases_yaml = "aliases:\n" + "".join(f'  - "{a}"\n' for a in aliases) if aliases else ""
    padded = frontmatter + "\n"
    if existing is not None:
        # Replace the existing aliases key in place (either format)
        pattern = ALIASES_BLOCK_RE if ALIASES_BLOCK_RE.search(padded) else ALIASES_INLINE_RE
        new_frontmatter = pattern.sub(lambda m: aliases_yaml, padded, count=1)
    else:
        # Insert after slug line if it exists, otherwise after title
        anchor = r"^(slug:.*\n)" if re.search(r"^slug:", padded, re.MULTILINE) else r"^(title:.*\n)"
        new_frontmatter = re.sub(anchor, lambda m: m.group(1) + aliases_yaml, padded, count=1, flags=re.MULTILINE)
    new_frontmatter = new_frontmatter[:-1]

    new_content = content[:fm_match.start(1)] + new_frontmatter + content[fm_match.end(1):]

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    existing = existing or []
    return ([a for a in aliases if a not in existing], [a for a in existing if a not in aliases])


def desired_aliases():
    """Map (lang, relative content path) -> ordered list of aliases."""
    desired = {}
    for target_file, alias_paths in ALIAS_PATHS:
        for lang in LANGUAGES:
            out = desired.setdefault((lang, target_file), [])
            for path in alias_paths:
                for alias in (f"/{lang}/{path}", f"/{lang}/{path}/"):
                    if alias not in out:
                        out.append(alias)
    # Bare-path aliases go on the English file only
    for target_file, alias_paths in BARE_ALIASES:
        out = desired.setdefault(("en", target_file), [])
        for path in alias_paths:
            for alias in (f"/{path}", f"/{path}/"):
                if alias not in out:
                    out.append(alias)
    return desired


def main():
    dry_run = "--dry-run" in sys.argv

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "..", "..")
    content_dir = os.path.join(project_root, "content")

    if not os.path.isdir(content_dir):
        print(f"Error: content directory not found at {content_dir}")
        sys.exit(1)

    if dry_run:
        print("=== DRY RUN - no files will be modified ===\n")

    desired = desired_aliases()
    missing = sorted({f for (_, f) in desired if not os.path.isfile(os.path.join(content_dir, "en", f))})
    for f in missing:
        print(f"Warning: alias target not found: content/en/{f}")

    total_modified = 0

    # Visit every content file so unlisted aliases are removed too
    for lang in LANGUAGES:
        lang_dir = os.path.join(content_dir, lang)
        for root, _, files in os.walk(lang_dir):
            for name in sorted(files):
                if not name.endswith((".md", ".html")):
                    continue
                filepath = os.path.join(root, name)
                rel = os.path.relpath(filepath, lang_dir).replace(os.sep, "/")
                result = set_aliases_in_file(filepath, desired.get((lang, rel), []), dry_run)
                if result is None:
                    continue
                total_modified += 1
                if dry_run:
                    added, removed = result
                    print(f"  {os.path.relpath(filepath, project_root)}")
                    for a in added:
                        print(f"    + {a}")
                    for a in removed:
                        print(f"    - {a}")

    action = "would modify" if dry_run else "modified"
    print(f"\nTotal: {total_modified} files {action}")


if __name__ == "__main__":
    main()
