#!/usr/bin/env python3
"""
AWS FinOps QC & Validation Card — LinkedIn screenshot visual
Run: python3 ~/finops_qc_card.py
"""

# ── ANSI codes ────────────────────────────────────────────────────────────
R   = "\033[0m"
B   = "\033[1m"          # bold
D   = "\033[2m"          # dim
U   = "\033[4m"          # underline

# Foreground
WHITE  = "\033[97m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
MGNT   = "\033[95m"
GRAY   = "\033[90m"

# Background accents (used sparingly)
BG_GREEN  = "\033[42m"
BG_RED    = "\033[41m"
BG_BLUE   = "\033[44m"

W = 74   # total card width (chars)
INN = W - 2   # inner width

# ── Helpers ───────────────────────────────────────────────────────────────
def top():    print(f"{B}{BLUE}╔{'═'*INN}╗{R}")
def bot():    print(f"{B}{BLUE}╚{'═'*INN}╝{R}")
def div():    print(f"{B}{BLUE}╠{'═'*INN}╣{R}")
def thinl():  print(f"{BLUE}╟{'─'*INN}╢{R}")
def blank():  print(f"{BLUE}║{R}{' '*INN}{BLUE}║{R}")

def title_row(text, color=WHITE):
    print(f"{BLUE}║{R}{B}{color}{text.center(INN)}{R}{BLUE}║{R}")

def sub_row(text):
    print(f"{BLUE}║{R}{D}{GRAY}{text.center(INN)}{R}{BLUE}║{R}")

def section(icon, label, color=CYAN):
    txt = f"  {icon}  {label}"
    print(f"{BLUE}║{R}{B}{color}{txt:<{INN}}{R}{BLUE}║{R}")

def kv(label, value, val_color=GREEN, label_w=42):
    lpart = f"  {label}"
    vpart = f"{val_color}{B}{value}{R}"
    # pad between label and value
    raw_pad = INN - len(lpart) - len(value) - 2
    pad = " " * max(1, raw_pad)
    print(f"{BLUE}║{R}{lpart}{pad}{vpart}  {BLUE}║{R}")

def check(text, color=GREEN, symbol="✓"):
    line = f"  {color}{B}{symbol}{R}  {text}"
    # pad to inner width
    visible_len = 2 + 1 + 2 + len(text)   # spaces + symbol + spaces + text
    pad = " " * max(0, INN - visible_len)
    print(f"{BLUE}║{R}{line}{pad}{BLUE}║{R}")

def warn(text, color=YELLOW, symbol="⚠"):
    line = f"  {color}{symbol}{R}  {text}"
    visible_len = 2 + 1 + 2 + len(text)
    pad = " " * max(0, INN - visible_len)
    print(f"{BLUE}║{R}{line}{pad}{BLUE}║{R}")

def bullet(text, indent=4):
    line = f"{' '*indent}{CYAN}▸{R}  {text}"
    visible = indent + 1 + 2 + len(text)
    pad = " " * max(0, INN - visible)
    print(f"{BLUE}║{R}{line}{pad}{BLUE}║{R}")

def recon_row(month, status="PASS", diff="$0.0000000000"):
    sc = GREEN if status == "PASS" else RED
    bar = f"{sc}{B}[{status}]{R}"
    lbl = f"  {CYAN}{month}{R}"
    mid = f"  diff = {GREEN}{B}{diff}{R}"
    # build visible string
    raw = f"  {month}  diff = {diff}  [{status}]"
    pad = " " * max(1, INN - len(raw) - 1)
    print(f"{BLUE}║{R}{lbl}{mid}{pad}{bar}  {BLUE}║{R}")

def conf_bar(label, pct, label_w=34, bar_w=18):
    if pct >= 80:
        col = GREEN
    elif pct >= 50:
        col = YELLOW
    else:
        col = RED
    filled = round(bar_w * pct / 100)
    empty  = bar_w - filled
    bar    = f"{col}{'█'*filled}{R}{D}{GRAY}{'░'*empty}{R}"
    pct_s  = f"{pct:>3}%"
    lpad   = " " * max(0, label_w - len(label))
    print(f"{BLUE}║{R}  {label}{lpad}  {bar}  {col}{B}{pct_s}{R}  {BLUE}║{R}")

def safety_badge(text, bg=BG_GREEN):
    inner = f" {text} "
    lpad  = (INN - len(inner)) // 2
    rpad  = INN - len(inner) - lpad
    print(f"{BLUE}║{R}{' '*lpad}{bg}{B}{WHITE}{inner}{R}{' '*rpad}{BLUE}║{R}")

# ── RENDER ────────────────────────────────────────────────────────────────
print()
top()

# Title
blank()
title_row("AWS FinOps Report — QC & Validation", WHITE)
sub_row("Independent Reconciliation  •  Read-Only  •  Human-Approved Remediation")
blank()

# ── QC STATUS ─────────────────────────────────────────────────────────────
div()
section("✅", "QC STATUS")
thinl()
check("FinOps QC  PASS  — Both reporting months reconciled")
check("8 previous report errors identified and corrected")
check("Final figures independently verified against AWS API data")
check("FINOPS_REPORT.md  (584 lines)  and  FINOPS_REPORT.pdf  (~18 pages)  verified")

# ── RECONCILIATION ────────────────────────────────────────────────────────
div()
section("⚖ ", "COST EXPLORER RECONCILIATION", CYAN)
thinl()
kv("September 2026  —  service sum = CE total",  "PASS ✔", GREEN)
kv("  Reconciliation difference",                "$0.0000000000", GREEN)
blank()
kv("October 2026 MTD  —  service sum = CE total", "PASS ✔", GREEN)
kv("  Reconciliation difference",                "$0.0000000000", GREEN)
blank()
kv("Sep gross charges (before credits)",          "$0.4342", YELLOW)
kv("Sep credits applied",                         "-$0.4342", CYAN)
kv("Sep net cost  (AWS CE total)",                "~$0.00", GREEN)
blank()
kv("Oct MTD gross charges (before credits)",      "$0.0328", YELLOW)
kv("Oct MTD credits applied",                     "-$0.0328", CYAN)
kv("Oct MTD net cost  (AWS CE total)",            "~$0.00", GREEN)

# ── 8 CORRECTIONS ─────────────────────────────────────────────────────────
div()
section("🔧", "CORRECTIONS VERIFIED IN QC PASS", MGNT)
thinl()
check("Resource inventory corrected:  6  →  10  resources")
check("CloudWatch cost corrected:  $0.19/mo  →  $0.00  (MB ≠ GB; within free tier)")
check("Cross-AZ cost:  wrong formula removed  →  AWS-reported  $0.0831  used")
check("Savings reclassified:  CONFIRMED  →  CONDITIONAL  (credits offset net cost)")
check("Oct MTD clarified:  gross  $0.0328  vs  net  ~$0.00  after credits")
check("EBS volume creation date verified:  2026-10-01  (explains Oct charges)")
check("Anomaly spend separated from CE monthly totals  (different concepts)")
warn("KMS savings marked CONDITIONAL  —  CloudTrail not queried; key usage unverified", YELLOW)

# ── DATA CONFIDENCE ───────────────────────────────────────────────────────
div()
section("🎯", "DATA CONFIDENCE BREAKDOWN  (self-reported)", CYAN)
thinl()
conf_bar("Cost Explorer billing totals",   95)
conf_bar("Resource inventory",             90)
conf_bar("CloudWatch log sizes",           85)
conf_bar("Calculated cost estimates",      80)
conf_bar("Overall audit confidence",       80)
conf_bar("Credit nature  (type unknown)",  50)
conf_bar("KMS key necessity",              40)
conf_bar("S3 bucket content / size",       30)
blank()
kv("  Low-confidence areas disclosed in report", "NOT hidden", YELLOW)

# ── FINOPS PRINCIPLES ─────────────────────────────────────────────────────
div()
section("📐", "FINOPS DATA INTEGRITY PRINCIPLES", CYAN)
thinl()
bullet("Never confuse historical spend with current ongoing spend")
bullet("Never add anomaly event amounts to monthly CE totals")
bullet("Never present conditional savings as confirmed savings")
bullet("Never invent resource-level costs when AWS data is unavailable")
bullet("Separate gross charges / credits / net cost / potential savings")
bullet("State confidence levels and data gaps — do not hide uncertainty")

# ── SAFETY ────────────────────────────────────────────────────────────────
div()
section("🔒", "SAFETY CONTROLS", GREEN)
thinl()
blank()
safety_badge("  READ-ONLY AWS ANALYSIS  —  NO RESOURCES MODIFIED  ", BG_GREEN)
blank()
safety_badge("  ALL REMEDIATION REQUIRES EXPLICIT HUMAN APPROVAL  ", "\033[48;5;17m")
blank()

# ── Footer ────────────────────────────────────────────────────────────────
div()
sub_row("Built with Kiro CLI   ·   AWS Cost Explorer API   ·   2026-10-04")
sub_row("No account IDs · No ARNs · No credentials · No private identifiers")
bot()
print()
