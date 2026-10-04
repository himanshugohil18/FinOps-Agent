#!/usr/bin/env python3
"""
Renders a clean FinOps summary card to the terminal.
Run this, then take a screenshot.
"""

W = 72  # card width

def line(char="─", left="│", right="│"):
    return f"{left}{char * (W-2)}{right}"

def row(label, value, label_w=36):
    label_col = label.ljust(label_w)
    value_col = value.rjust(W - 2 - label_w - 1)
    return f"│ {label_col}{value_col} │"

def center(text, fill=" "):
    return f"│{text.center(W-2, fill)}│"

def blank():
    return f"│{'':^{W-2}}│"

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
WHITE  = "\033[97m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
BG_DARK = "\033[48;5;17m"   # dark navy background
BG_MID  = "\033[48;5;18m"
BG_NONE = "\033[49m"

print()

# ── Top border ────────────────────────────────────────────────────────────
print(f"{BOLD}{BLUE}╔{'═'*(W-2)}╗{RESET}")

# ── Title block ───────────────────────────────────────────────────────────
print(f"{BOLD}{BLUE}║{RESET}{BOLD}{WHITE}{'AWS FinOps Analysis Agent'.center(W-2)}{RESET}{BOLD}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}║{RESET}{DIM}{'Read-Only · QC-Validated · Kiro CLI'.center(W-2)}{RESET}{BOLD}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}╠{'═'*(W-2)}╣{RESET}")

# ── Audit metadata ────────────────────────────────────────────────────────
print(f"{BLUE}║{RESET}  {CYAN}Audit Date{RESET}{'2026-10-04'.rjust(W-14)}{BLUE}  ║{RESET}")
print(f"{BLUE}║{RESET}  {CYAN}Period{RESET}   {'Oct 2026 MTD + Sep 2026 (full)'.rjust(W-11)}{BLUE}  ║{RESET}")
print(f"{BLUE}║{RESET}  {CYAN}Mode{RESET}     {'READ-ONLY — No resources modified'.rjust(W-11)}{BLUE}  ║{RESET}")
print(f"{BOLD}{BLUE}╠{'═'*(W-2)}╣{RESET}")

# ── Cost Snapshot ─────────────────────────────────────────────────────────
print(f"{BLUE}║{RESET}{BOLD}{'  💰  COST SNAPSHOT'.ljust(W-2)}{RESET}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}╟{'─'*(W-2)}╢{RESET}")

rows = [
    ("Sep 2026 Net Cost (AWS CE Total)",        f"{GREEN}~$0.00  (credits applied){RESET}"),
    ("Sep 2026 Gross Charges (before credits)", f"{YELLOW}$0.4342{RESET}"),
    ("Oct 2026 MTD Net Cost (AWS CE Total)",    f"{GREEN}~$0.00  (credits applied){RESET}"),
    ("Oct 2026 Gross Charges (before credits)", f"{YELLOW}$0.0328{RESET}"),
    ("CE Reconciliation Difference",           f"{GREEN}$0.0000000000  ✔ PASS{RESET}"),
]
for label, val in rows:
    pad = W - 2 - len(label) - 3
    print(f"{BLUE}║{RESET}  {label}{' '*max(0,pad-30)}{val}  {BLUE}║{RESET}")

print(f"{BOLD}{BLUE}╠{'═'*(W-2)}╣{RESET}")

# ── Resource Inventory ────────────────────────────────────────────────────
print(f"{BLUE}║{RESET}{BOLD}{'  📦  RESOURCE INVENTORY'.ljust(W-2)}{RESET}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}╟{'─'*(W-2)}╢{RESET}")

inv = [
    ("Total resource objects found",              "10"),
    ("Resources with current net cost > $0",      "0   (all offset by credits)"),
    ("Resources with conditional cost",           "3   (EBS vol + 2 KMS CMKs)"),
    ("EBS volumes unattached (orphaned)",         "1   · 10 GB gp3 · us-west-2"),
    ("S3 buckets",                                "2   · us-east-1"),
    ("CloudWatch log groups",                     "5   · 37.5 MB total (within free tier)"),
    ("KMS customer-managed keys",                 "2   · us-east-1"),
]
for label, val in inv:
    gap = W - 4 - len(label) - len(val)
    print(f"{BLUE}║{RESET}  {label}{'·'.rjust(max(1,gap))}{val}  {BLUE}║{RESET}")

print(f"{BOLD}{BLUE}╠{'═'*(W-2)}╣{RESET}")

# ── Savings ───────────────────────────────────────────────────────────────
print(f"{BLUE}║{RESET}{BOLD}{'  💡  SAVINGS ANALYSIS'.ljust(W-2)}{RESET}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}╟{'─'*(W-2)}╢{RESET}")

savings = [
    ("Confirmed current net savings",                 f"{WHITE}$0.00{RESET}", "(net cost is already $0)"),
    ("Conditional — EBS volume (if credits expire)",  f"{YELLOW}$0.80/mo{RESET}", "list price · $0.08/GB × 10 GB"),
    ("Conditional — KMS CMKs (if credits expire)",    f"{YELLOW}$2.00/mo{RESET}", "2 keys · $1.00/key · UNVERIFIED use"),
    ("Total conditional exposure",                    f"{YELLOW}$2.80/mo{RESET}", "if credits expire"),
    ("Historical: cross-region transfer (Sep lab)",   f"{DIM}$0.3511{RESET}", "per session · AWS-reported"),
    ("Historical: NAT Gateway (Sep lab, list price)", f"{DIM}~$2.23{RESET}", "per session · credit-offset"),
]
for label, val, note in savings:
    print(f"{BLUE}║{RESET}  {CYAN}▸{RESET} {label}")
    print(f"{BLUE}║{RESET}    {val}  {DIM}{note}{RESET}")

print(f"{BOLD}{BLUE}╠{'═'*(W-2)}╣{RESET}")

# ── Audit Confidence ──────────────────────────────────────────────────────
print(f"{BLUE}║{RESET}{BOLD}{'  🎯  AUDIT CONFIDENCE BREAKDOWN'.ljust(W-2)}{RESET}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}╟{'─'*(W-2)}╢{RESET}")

conf = [
    ("Cost Explorer billing totals",   95, GREEN),
    ("Resource inventory",             90, GREEN),
    ("CloudWatch log sizes",           85, GREEN),
    ("Calculated cost estimates",      80, YELLOW),
    ("Credit nature (type unknown)",   50, YELLOW),
    ("KMS key necessity",              40, RED),
    ("S3 bucket content / size",       30, RED),
    ("Overall audit confidence",       80, YELLOW),
]
bar_w = 25
for label, pct, color in conf:
    filled   = round(bar_w * pct / 100)
    empty    = bar_w - filled
    bar      = f"{color}{'█' * filled}{RESET}{DIM}{'░' * empty}{RESET}"
    pct_str  = f"{pct:>3}%"
    pad      = 35 - len(label)
    print(f"{BLUE}║{RESET}  {label}{' '*pad} {bar} {color}{BOLD}{pct_str}{RESET}  {BLUE}║{RESET}")

print(f"{BOLD}{BLUE}╠{'═'*(W-2)}╣{RESET}")

# ── QC corrections ────────────────────────────────────────────────────────
print(f"{BLUE}║{RESET}{BOLD}{'  ✅  QC PASS — 8 ERRORS CORRECTED'.ljust(W-2)}{RESET}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}╟{'─'*(W-2)}╢{RESET}")

fixes = [
    "Resource count: 6 → 10  (S3 + KMS were missing)",
    "CloudWatch cost: $0.19/mo → $0.00  (MB≠GB; within free tier)",
    "Cross-AZ formula removed: 'qty×$0.01×2dirs' → AWS-reported $0.0831",
    "All savings reclassified as CONDITIONAL (credits offset net cost)",
    "Oct MTD clarified: gross $0.0328 vs net ~$0.00 after credits",
    "EBS creation date corrected: 2026-10-01 (explains Oct charges)",
    "Anomaly sums NOT added to CE monthly totals (different concepts)",
    "KMS savings marked CONDITIONAL — CloudTrail not queried",
]
for fix in fixes:
    print(f"{BLUE}║{RESET}  {GREEN}✓{RESET} {fix}")

print(f"{BOLD}{BLUE}╠{'═'*(W-2)}╣{RESET}")

# ── Output files ──────────────────────────────────────────────────────────
print(f"{BLUE}║{RESET}{BOLD}{'  📄  REPORT OUTPUT'.ljust(W-2)}{RESET}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}╟{'─'*(W-2)}╢{RESET}")
print(f"{BLUE}║{RESET}  {WHITE}FINOPS_REPORT.md{RESET}   {DIM}Markdown · 584 lines · full analysis + reconciliation{RESET}")
print(f"{BLUE}║{RESET}  {WHITE}FINOPS_REPORT.pdf{RESET}  {DIM}PDF · ~18 pages · cover page + all sections{RESET}")

print(f"{BOLD}{BLUE}╠{'═'*(W-2)}╣{RESET}")

# ── Footer ────────────────────────────────────────────────────────────────
print(f"{BLUE}║{RESET}{DIM}{'  Built with Kiro CLI  ·  All remediation requires human approval'.center(W-2)}{RESET}{BLUE}║{RESET}")
print(f"{BLUE}║{RESET}{DIM}{'  READ-ONLY  ·  No AWS resources were modified during this audit'.center(W-2)}{RESET}{BLUE}║{RESET}")
print(f"{BOLD}{BLUE}╚{'═'*(W-2)}╝{RESET}")
print()
