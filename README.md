# AWS FinOps Analysis Agent

> **Read-Only AWS Cost Intelligence — QC-Validated — Human-Approved Remediation**

An AI-assisted AWS FinOps analysis agent built with [Kiro CLI](https://kiro.dev).
It performs a complete, read-only audit of an AWS account, generates a structured cost intelligence report, and runs an independent QC reconciliation pass to verify every number before publishing.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Mode: Read-Only](https://img.shields.io/badge/Mode-Read--Only-green)
![Remediation: Human Approved](https://img.shields.io/badge/Remediation-Human%20Approved-orange)
![QC Status](https://img.shields.io/badge/QC%20Status-PASS-brightgreen)

---

## What This Is

This project demonstrates how an AI agent (Kiro FinOps Agent) can autonomously:

1. Query AWS Cost Explorer and resource APIs in **read-only mode**
2. Identify orphaned resources, architecture cost risks, and savings opportunities
3. Generate a full FinOps report in **Markdown and PDF**
4. Run a **QC reconciliation pass** to catch errors before publishing
5. Clearly separate AWS-reported costs, historical spend, credits, gross charges, net costs, and conditional savings

**It does not remediate anything automatically.** All recommendations require explicit human approval.

---

## Project Structure

```
FinOps-Agent/
├── README.md                        ← You are here
├── .gitignore
│
├── reports/
│   ├── FINOPS_REPORT.md             ← Full audit report (584 lines)
│   └── FINOPS_REPORT.pdf            ← PDF version (~18 pages)
│
├── scripts/
│   ├── finops_audit.sh              ← Read-only AWS data collection script
│   └── finops_pdf.py                ← Markdown → PDF generator (ReportLab)
│
├── visuals/
│   ├── finops_card.py               ← Terminal dashboard card (screenshot)
│   └── finops_qc_card.py            ← QC validation card (screenshot)
│
└── docs/
    ├── iam-permissions.md           ← Minimum required IAM policy
    └── lessons-learned.md           ← 10 engineering lessons from this project
```

---

## Audit Results — 2026-10-04

### Cost Snapshot

| Metric | Value |
|---|---|
| Sep 2026 Net Cost (AWS CE Total) | ~$0.00 (credits applied) |
| Sep 2026 Gross Charges (before credits) | $0.4342 |
| Oct 2026 MTD Net Cost (AWS CE Total) | ~$0.00 (credits applied) |
| Oct 2026 MTD Gross Charges | $0.0328 |
| CE Reconciliation Difference (Sep) | **$0.0000000000 — PASS** |
| CE Reconciliation Difference (Oct) | **$0.0000000000 — PASS** |
| Total Resources in Inventory | 10 |
| Active Cost Anomalies | 0 (all 8 detected events are historical, ended Sep 30) |
| Confirmed Current Savings | $0.00 (net cost is already $0 after credits) |
| Conditional Exposure (if credits expire) | $2.80/month ($0.80 EBS + $2.00 KMS) |

### Resources Found

| Resource | Count | Region(s) | Status |
|---|---|---|---|
| EBS volumes (unattached) | 1 | us-west-2 | 10 GB gp3 — orphaned after lab teardown |
| S3 buckets | 2 | us-east-1 | Active, near-zero cost |
| CloudWatch log groups | 5 | us-east-1, us-west-2, ap-south-1 | 4 without retention policy |
| KMS CMKs | 2 | us-east-1 | Purpose unverified (CloudTrail not queried) |
| EC2 instances | 0 | All regions | None running |
| EKS clusters | 0 | All regions | All decommissioned |
| ECS clusters | 0 | All regions | None |
| NAT Gateways | 0 | All regions | None running |
| Load Balancers | 0 | All regions | None running |
| RDS instances | 0 | All regions | None running |

### Top Historical Cost Drivers (September 2026 Lab)

| Usage Type | Quantity | AWS-Reported Cost | Status |
|---|---|---|---|
| Cross-region transfer ap-south-1 → ap-southeast-1 | 4.082 GB | $0.3511 | Historical |
| Cross-AZ transfer us-west-2 | 9.055 GB | $0.0831 | Historical |
| NAT Gateway hours us-west-2 | 42 hrs | $0.00 net (list: $1.89) | Historical |
| NAT Gateway data us-west-2 | 7.652 GB | $0.00 net (list: $0.34) | Historical |

> All September charges were fully offset by AWS credits. Net CE total = -$0.0000008495.

---

## QC Reconciliation

Both reporting months reconcile exactly:

```
September 2026
  Sum of service line items : -$0.0000008495
  CE Total (no grouping)    : -$0.0000008495
  Difference                : $0.0000000000  ✓ PASS

October 2026 MTD
  Sum of service line items : -$0.0000002541
  CE Total (no grouping)    : -$0.0000002541
  Difference                : $0.0000000000  ✓ PASS
```

### 8 Errors Corrected During QC

| # | Error | Correction |
|---|---|---|
| 1 | Resource count reported as 6 | Corrected to **10** (S3 + KMS were missing) |
| 2 | CloudWatch cost estimated at $0.19/month | Corrected to **$0.00** (0.037 GB < 5 GB free tier; MB ≠ GB) |
| 3 | Cross-AZ formula: `qty × $0.01 × 2 dirs` | Removed; **AWS-reported $0.0831** used as authoritative |
| 4 | Savings shown as confirmed | Reclassified as **CONDITIONAL** (credits offset net cost to $0) |
| 5 | Oct MTD shown as "$0.0328" without context | Clarified: **gross $0.0328 vs net ~$0.00** after credits |
| 6 | EBS volume attributed to pre-Oct activity | Corrected: **created 2026-10-01** (explains Oct charges) |
| 7 | Anomaly totals added to CE monthly total | Corrected: **anomaly events ≠ monthly totals** (different concepts) |
| 8 | KMS labeled as confirmed $2/month saving | Corrected: **CONDITIONAL** — CloudTrail not queried; key usage unverified |

---

## Confidence Breakdown

| Area | Confidence | Reason |
|---|---|---|
| Cost Explorer billing totals | **95%** | Exact API values; reconciliation = $0.00 |
| Resource inventory | **90%** | Direct API calls; 3 primary regions fully scanned |
| CloudWatch log sizes | **85%** | Exact byte counts from API; slight lag possible |
| Calculated cost estimates | **80%** | Standard pricing × quantity; some rounding |
| Overall audit confidence | **80%** | Weighted across all areas |
| Credit nature (type unknown) | **50%** | Cannot determine credit type from CE API alone |
| KMS key necessity | **40%** | CloudTrail not queried; key usage unverified |
| S3 bucket size/content | **30%** | CW metrics not enabled; exact sizes unavailable |

> Low-confidence areas are disclosed in the report, not hidden.

---

## Data Confidence Principles

This project follows strict FinOps data integrity rules:

- ✅ Never confuse historical spend with current ongoing spend
- ✅ Never add anomaly event amounts to monthly CE totals
- ✅ Never present conditional savings as confirmed savings
- ✅ Never invent resource-level costs when AWS data is unavailable
- ✅ Separate gross charges / credits / net cost / potential savings
- ✅ State confidence levels and data gaps — do not hide uncertainty
- ✅ Use AWS-reported costs as authoritative; label calculated estimates clearly
- ✅ Reconcile CE totals before publishing any report

---

## Quick Start

### Prerequisites

- AWS CLI configured with read-only credentials
- Python 3.8+ with `reportlab` (`pip install reportlab`)
- Appropriate IAM permissions (see [`docs/iam-permissions.md`](docs/iam-permissions.md))

### 1. Collect AWS Data

```bash
chmod +x scripts/finops_audit.sh
./scripts/finops_audit.sh
```

This writes raw JSON to `raw_data/` (gitignored — may contain account identifiers).

### 2. Generate the PDF Report

```bash
python3 scripts/finops_pdf.py \
  --input  reports/FINOPS_REPORT.md \
  --output reports/FINOPS_REPORT.pdf
```

### 3. Render the Terminal Visual Cards

```bash
# FinOps Dashboard card
python3 visuals/finops_card.py

# QC Validation card
python3 visuals/finops_qc_card.py
```

Screenshot either card from your terminal for a clean LinkedIn/presentation visual.

---

## Safety

| Control | Detail |
|---|---|
| **Read-only** | All AWS API calls use describe/list/get operations only |
| **No auto-remediation** | The agent makes zero changes to any AWS resource |
| **Human approval required** | All findings are recommendations; execution is human-gated |
| **No credentials in repo** | `.gitignore` excludes `.aws/`, `*.pem`, and all credential files |
| **No account IDs in visuals** | Terminal cards contain no ARNs, account IDs, or private identifiers |
| **Raw data excluded** | `raw_data/` is gitignored — it may contain account-specific identifiers |

---

## Architecture Cost Risks Identified

The September 2026 lab usage revealed these patterns for future reference:

**NAT Gateway + EKS without VPC Endpoints**
- 42 hrs NAT × $0.045/hr + 7.65 GB × $0.045/GB = $2.23/session (list price)
- Fix: S3 Gateway Endpoint (free), ECR/STS Interface Endpoints

**Cross-region traffic (ap-south-1 → ap-southeast-1)**
- 4.08 GB → $0.3511 per session
- Fix: Keep ECR in same region as EKS; use regional endpoints

**Cross-AZ traffic (EKS pods across AZs)**
- 9.055 GB → $0.0831 per session
- Fix: Pod Topology Spread Constraints with `topologyKey: topology.kubernetes.io/zone`

**EBS orphaning after lab teardown**
- 1 unattached volume found (10 GB gp3, us-west-2)
- Fix: Set `DeleteOnTermination=true` in Terraform IaC

**CloudWatch log group orphaning**
- 2 log groups from deleted EKS clusters (no retention policy)
- Fix: Include `retention_in_days` in all Terraform `aws_cloudwatch_log_group` resources

---

## Report Contents

`reports/FINOPS_REPORT.md` contains:

1. Executive Summary
2. Cost Overview (gross / credits / net)
3. Top Cost Drivers
4. Cost Anomalies (with historical/current distinction)
5. Active Resource Inventory
6. Optimization Opportunities
7. Detailed Findings
8. Architecture Cost Risks
9. Savings Summary (categorized: confirmed / conditional / preventive / historical)
10. Recommended Action Plan
11. Safety & Assumptions
12. **FinOps Reconciliation & Quality Control** (calculation validation, savings double-counting check, resource-count reconciliation, AWS-reported vs estimated cost validation)

---

## Built With

- [Kiro CLI](https://kiro.dev) — AI agent framework
- [AWS Cost Explorer API](https://docs.aws.amazon.com/cost-management/latest/APIReference/) — billing data
- [AWS EC2 / EKS / RDS / S3 / CloudWatch APIs](https://docs.aws.amazon.com/index.html) — resource inventory
- [ReportLab](https://www.reportlab.com/) — PDF generation
- Python 3.8 / Bash

---

## License

MIT — see [LICENSE](LICENSE)

---

## Author

**Himanshu Gohil**
[github.com/himanshugohil18](https://github.com/himanshugohil18)

---

> *"A FinOps report that hides its uncertainty is less useful than one that shows it."*
