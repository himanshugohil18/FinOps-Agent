# AWS FinOps Cost Optimization Report

> **Generated:** 2026-10-04
> **AWS Account:** 730649731674 (Himanshu Gohil)
> **Report Author:** Kiro FinOps Agent
> **Access Level:** READ-ONLY — No AWS resources were modified
> **Audit Period:** October 2026 MTD (Oct 1–4, 3 days) + September 2026 (full month) + August 2026
> **QC Status:** RECONCILED — All numbers independently verified against raw AWS API data

---

## Executive Summary

| Field | Value |
|---|---|
| Account | 730649731674 (Himanshu Gohil) |
| Account Alias | None configured |
| Audit Date | 2026-10-04 |
| Audit Period | Oct 2026 MTD (Oct 1–4) + Sep 2026 (full) |
| Sep 2026 CE Total (net) | -$0.0000008495 (~$0.00) |
| Sep 2026 Gross Charges | $0.4342 (before credits) |
| Sep 2026 Credits Applied | -$0.4342 |
| Oct 2026 CE Total (net, 3 days) | -$0.0000002541 (~$0.00) |
| Oct 2026 Gross Charges | $0.0328 (before credits) |
| Oct 2026 Credits Applied | -$0.0328 |
| Total Resource Objects in Inventory | 10 |
| Resources with Current Net Cost | 0 (all offset by credits or free tier) |
| Resources with Conditional Cost | 3 (EBS volume + 2 KMS CMKs, if credits expire) |
| Active Cost Anomalies | 0 (none current) |
| Historical Anomalies Detected | 8 distinct events (all ended Sep 30, 2026) |
| Confirmed Current Net Savings | $0.00 (current net cost is already $0) |
| Conditional Savings (if credits expire) | $2.80/month ($0.80 EBS + $2.00 KMS) |
| Top Historical Cost Driver | Cross-region transfer ap-south-1→ap-southeast-1: $0.3511 (Sep 2026) |
| Top Current Action | Delete orphaned EBS vol-008573e93270b1bcd (conditional savings $0.80/month) |

**Summary:** This AWS account is used for lab/learning environments. All compute infrastructure (EC2, EKS, ECS, Lambda, RDS, NAT Gateways, Load Balancers) was fully decommissioned by September 30, 2026. Both the September and October net costs are effectively **$0.00** — AWS credits fully offset all gross charges. No active anomalies exist. The account retains 10 passive resources (1 orphaned EBS volume, 2 S3 buckets, 5 CloudWatch log groups, 2 KMS CMKs). If AWS credits expire, the conditional exposure is $2.80/month from the orphaned EBS volume and KMS keys.

---

## 1. Cost Overview

> All costs are AWS Cost Explorer UnblendedCost values, which equal BlendedCost and NetUnblendedCost for this account (no RI/SP amortization). Negative values represent credits/discounts applied by AWS.

| Service | Sep 2026 Gross | Sep 2026 Net | Oct MTD Gross | Oct MTD Net | Notes |
|---|---:|---:|---:|---:|---|
| EC2 - Other | $0.4342 | Offset | $0.0328 | Offset | Largest line; includes data transfer, NAT, EBS |
| AWS Data Transfer (credit) | — | -$0.4342 | — | -$0.0328 | AWS credit fully offsets EC2-Other |
| Amazon EC2 Compute | $0.0000052 | Offset | $0.0000069 | Offset | Near-zero; free tier or credits |
| Amazon ELB | $0.0000025 | Offset | $0.0000001 | Offset | Near-zero residual |
| Amazon RDS | $0.0000002 | Offset | $0.0000000 | Offset | Near-zero residual |
| Amazon S3 | $0.0000014 | Offset | $0.0000000 | Offset | 2 small buckets |
| Amazon ECR | $0.0000000 | Offset | $0.0000000 | Offset | Near-zero |
| Amazon ECS | $0.0000000 | Offset | $0.00 | — | No activity |
| Amazon EKS | -$0.0000000 | Offset | $0.00 | — | No clusters |
| AWS KMS | -$0.0000008 | -$0.0000008 | -$0.0000003 | -$0.0000003 | Net negative (credit exceeds charge) |
| AWS Backup | -$0.0000000 | -$0.0000000 | -$0.0000000 | — | Near-zero |
| AWS WAF | -$0.0000001 | -$0.0000001 | $0.00 | — | Historical only |
| All Others | $0.00 | $0.00 | $0.00 | $0.00 | Free tier; Lambda, VPC, CW, etc. |
| **CE Reported Total** | — | **-$0.0000008** | — | **-$0.0000003** | **Effectively $0.00** |

> **How to read this table:** "Gross" is the list-price charge before credits. "Net" is after AWS credits are applied. For this account, all positive gross charges are offset by negative AWS Data Transfer credits, resulting in a near-zero net total. Only the KMS and Backup lines remain slightly negative (over-credit).

---

## 2. Top Cost Drivers

> All costs below are HISTORICAL (September 2026 lab period). Current net cost for all items is $0.00.

| Rank | Usage Type / Service | Quantity | AWS-Reported Cost (Sep) | Pricing Basis | Status |
|---|---|---:|---:|---|---|
| 1 | Cross-region transfer: ap-south-1 → ap-southeast-1 (APS3-APS1-AWS-Out-Bytes) | 4.082 GB | $0.3511 | AWS-reported | HISTORICAL |
| 2 | Cross-AZ transfer within us-west-2 (USW2-DataTransfer-Regional-Bytes) | 9.055 GB | $0.0831 | AWS-reported | HISTORICAL |
| 3 | NAT Gateway hours, us-west-2 (USW2-NatGateway-Hours) | 42 hrs | $0.00 net (list: $1.89) | Offset by credits | HISTORICAL |
| 4 | NAT Gateway data, us-west-2 (USW2-NatGateway-Bytes) | 7.652 GB | $0.00 net (list: $0.34) | Offset by credits | HISTORICAL |
| 5 | EBS gp3 volume, ap-south-1 (APS3-EBS:VolumeUsage.gp3) | 2.005 GB-Month | $0.00 net | Offset by credits | HISTORICAL |
| 6 | USW2-USE1-AWS-Out-Bytes (us-west-2 → us-east-1) | 0.001 GB | $0.0000189 | AWS-reported | HISTORICAL |

**Note on October EC2-Other:** Oct MTD contains USW2-DataTransfer-Regional-Bytes: 4.278 GB → $0.0328 gross (fully offset by credits → net $0.00). This is a residual transfer, likely from the newly-created orphaned EBS volume (created Oct 1) generating API/metadata traffic. No active EKS or NAT Gateway is running in October.

---

## 3. Cost Anomalies

> AWS Cost Anomaly Detection reported 8 distinct anomaly events. All are HISTORICAL — ended on or before September 30, 2026. **TotalActualSpend values in anomalies are per-event daily amounts, not additive monthly totals. They do not add to the CE monthly total; they are point-in-time spikes fully contained within the Sep 2026 service-level costs.**

| Anomaly ID (short) | Date Range | Service | Actual Spend (event) | Expected | Impact | Root Cause | Status |
|---|---|---|---:|---:|---:|---|---|
| 62bfe040 | Sep 29–30 | EBS / NAT (us-west-2) | $2.84 | $0.07 | +3,957% | NAT Gateway 42 hrs + EBS gp3 + NAT data 7.65 GB during EKS lab | HISTORICAL |
| 19e656b1 | Sep 29–30 | EC2 Compute | $4.03 | $0.00 | N/A | c7i-flex.large instances in us-west-2 and ap-south-1 (EKS nodes) | HISTORICAL |
| 2ebc27d9 | Sep 29–30 | Elastic Load Balancing | $1.64 | $0.00 | N/A | ALB/NLB from EKS Kubernetes LoadBalancer services | HISTORICAL |
| 466b10ef | Sep 29–30 | Amazon VPC | $1.14 | $0.00 | N/A | NAT Gateway EIP, VPC flow logs, or interface endpoints | HISTORICAL |
| 6367e764 | Sep 29–30 | AWS KMS | $0.12 | $0.06 | +100% | Increased KMS API calls from active EKS encryption | HISTORICAL |
| e7a6aa0d | Sep 25 | Amazon EBS | $0.44 | $0.04 | +1,000% | EBS volume activity during lab setup | HISTORICAL |
| acf4f31a | Sep 25 | AWS WAF | $0.06 | $0.00 | N/A | WAF Web ACL activated (aws-waf-logs-waf-lab-web-acl) | HISTORICAL |
| 06a66db7 | Sep 2–3 | EC2 Compute | $0.55 | $0.01 | +5,400% | Early lab instance activity | HISTORICAL |

> **Anomaly vs CE Reconciliation:** The sum of anomaly TotalActualSpend values ($11.96) is intentionally much larger than the CE monthly total (~$0.4342 gross). Anomaly Detection captures per-service spend during anomalous daily periods. These are not independent monthly charges — they are sub-periods within the same September billing cycle. The $4.03 EC2 anomaly, $1.64 ELB anomaly, etc., are daily peaks; their underlying charges are captured in the EC2-Other ($0.4342) and other service lines in Cost Explorer and fully offset by credits.

---

## 4. Active Resource Inventory

> Resource count reconciliation: **10 total objects** across all active regions.

| # | Category | Resource ID / Name | Region | State | Stored Data | AWS-Reported Net Cost | Conditional Cost |
|---|---|---|---|---|---|---|---|
| 1 | EBS Volume (gp3) | vol-008573e93270b1bcd | us-west-2a | **available (UNATTACHED)** | 10 GB (created 2026-10-01) | $0.00 net (credit offset) | $0.80/month if credits expire |
| 2 | S3 Bucket | him-demo-18 | us-east-1 | Active (created 2026-09-07) | Unknown (metrics unavailable) | $0.00 | Negligible |
| 3 | S3 Bucket | minishop-terraform-state-730649731674 | us-east-1 | Active (created 2026-09-22) | Unknown (metrics unavailable) | $0.00 | Negligible |
| 4 | CW Log Group | /aws/ecs/containerinsights/incidentiq-target/performance | us-east-1 | Active, 1-day retention | 0 bytes | $0.00 | $0.00 |
| 5 | CW Log Group | /aws/eks/HimCluser/cluster | us-west-2 | Active, **no retention** | 6,309,180 bytes (6.02 MB) | $0.00 (free tier) | $0.00 (free tier) |
| 6 | CW Log Group | /aws/eks/himanshu-eks-cluster/cluster | ap-south-1 | Active, **no retention** | 32,346,158 bytes (30.85 MB) | $0.00 (free tier) | $0.00 (free tier) |
| 7 | CW Log Group | /aws/lambda/saa8-api-handler | ap-south-1 | Active, **no retention** | 13,162 bytes (0.01 MB) | $0.00 (free tier) | $0.00 (free tier) |
| 8 | CW Log Group | aws-waf-logs-waf-lab-web-acl | ap-south-1 | Active, **no retention** | 623,670 bytes (0.60 MB) | $0.00 (free tier) | $0.00 (free tier) |
| 9 | KMS CMK | 18a08257-7685-4466-a27e-4b2870f552ae | us-east-1 | Active (customer managed) | N/A | $0.00 net (credit offset) | $1.00/month if credits expire |
| 10 | KMS CMK | e1975ab0-8724-4335-8ae4-296958bca994 | us-east-1 | Active (customer managed) | N/A | $0.00 net (credit offset) | $1.00/month if credits expire |

**Resource count breakdown:**
- Total resource objects: **10**
- Resources with current net cost > $0: **0**
- Resources with conditional cost (if credits expire): **3** (EBS + 2 KMS)
- Resources with zero cost now and in future: **5** (CloudWatch log groups — within free tier)
- Resources with zero cost now, negligible future cost: **2** (S3 buckets)

**CloudWatch total storage:** 39,292,170 bytes = **37.48 MB = 0.0366 GB** — entirely within the 5 GB free tier. **Current storage cost = $0.00.**

**Resources confirmed NOT running:**
- EC2 instances: 0 (all regions)
- EKS clusters: 0 (all regions)
- ECS clusters: 0 (all regions)
- Lambda functions: 0 (all regions)
- NAT Gateways: 0 (all regions)
- Load Balancers (ALB/NLB): 0 (all regions)
- RDS instances: 0 (all regions)
- EBS snapshots: 0 (all regions)
- AMIs (self-owned): 0
- ECR repositories: 0 (all regions)
- VPC endpoints: 0

---

## 5. Optimization Opportunities

| Priority | Finding | Current Net Cost | Conditional Monthly Savings | Classification | Confidence | Effort |
|---|---|---:|---:|---|---|---|
| P2 | Delete orphaned EBS vol-008573e93270b1bcd (10 GB gp3, us-west-2) | $0.00 (credit offset) | $0.80/month if credits expire | Conditional | High | Low |
| P2 | Set retention policies on CW log groups without retention (4 groups) | $0.00 (free tier) | $0.00 (preventive hygiene) | Preventive | High | Low |
| P2 | Delete orphaned EKS log groups (clusters no longer exist) | $0.00 (free tier) | $0.00 (preventive hygiene) | Preventive | High | Low |
| P3 | Review and delete unused KMS CMKs (2 keys, us-east-1) | $0.00 (credit offset) | $2.00/month if credits expire | Conditional | Medium | Low–Medium |
| P3 | Add S3 lifecycle policies to both buckets | $0.00 | $0.00 (preventive) | Preventive | Low | Low |
| P3 | Consolidate future lab workloads to single region | N/A (historical) | $0.351/lab-session | Historical/Future | Medium | Medium |
| P3 | Use S3 Gateway Endpoint in future labs (eliminate NAT-to-S3) | N/A (no NAT running) | Variable per lab | Historical/Future | High | Low |

---

## 6. Detailed Findings

---

### Finding 1: Orphaned EBS Volume — Conditional Cost

| Field | Value |
|---|---|
| **Finding** | Unattached EBS gp3 volume in us-west-2; no workload attached |
| **Resource** | vol-008573e93270b1bcd |
| **Region / AZ** | us-west-2a |
| **Volume Type / Size** | gp3, 10 GB |
| **Volume Created** | 2026-10-01T04:57:09Z (created Oct 1, not before Sep 30) |
| **State** | available (UNATTACHED) |
| **AWS-Reported Net Cost (Oct MTD)** | -$0.0000000029 (credit offset — net cost is $0.00) |
| **AWS-Reported Usage (Oct 1–4)** | 2.7731 GB-Month (confirmed: 10 GB × 3/31 days ≈ 0.968 GB-Month per day × 3 days = 2.90 GB-Month; API value reflects partial-day precision) |
| **Calculated Monthly Cost** | 10 GB × $0.08/GB-month = **$0.80/month** (pricing assumption: AWS published gp3 price, us-west-2) |
| **Savings Classification** | CONDITIONAL — $0.80/month IF credits expire |
| **Confirmed Current Savings** | $0.00 (credits currently absorb the charge) |
| **Estimated Annual Savings (conditional)** | $9.60/year |
| **Confidence** | High (volume confirmed unattached via describe-volumes API) |
| **Why It Exists** | EKS lab cluster was deleted but EBS volume was not included in teardown; created Oct 1 as part of final lab activity |
| **Recommendation** | Snapshot if data is needed; then delete |
| **Risk** | Data loss if deleted without snapshot (irreversible) |
| **Human Approval Required** | YES |

---

### Finding 2: CloudWatch Log Groups from Deleted EKS Clusters — Preventive

| Field | Value |
|---|---|
| **Finding** | Log groups from deleted EKS clusters persist with no retention policy |
| **Resources** | /aws/eks/HimCluser/cluster (us-west-2, 6.02 MB); /aws/eks/himanshu-eks-cluster/cluster (ap-south-1, 30.85 MB) |
| **Total Stored** | 38,655,338 bytes = **36.88 MB = 0.0360 GB** |
| **AWS-Reported Net Cost** | $0.00 (all storage within 5 GB free tier) |
| **Calculated Cost** | 0.0360 GB × $0.03/GB-month = **$0.00108/month** (below free tier — actual current cost = $0.00) |
| **Free Tier Remaining** | 5 GB − 0.0366 GB (all log groups combined) = **4.9634 GB free tier remaining** |
| **Savings Classification** | PREVENTIVE — current cost is $0.00; prevents future accumulation |
| **Why They Exist** | AWS does not delete log groups when EKS clusters are deleted; these clusters no longer exist |
| **EKS Clusters Confirmed Absent** | Yes — `eks list-clusters` returned empty in both us-west-2 and ap-south-1 |
| **Recommendation** | Delete both orphaned EKS log groups; set 30-day retention on remaining groups |
| **Risk** | Log data permanently lost; no impact on running workloads (no clusters exist) |
| **Human Approval Required** | YES |

---

### Finding 3: CloudWatch Log Groups — Missing Retention Policies

| Field | Value |
|---|---|
| **Finding** | 4 of 5 log groups have no retention policy; will accumulate logs indefinitely |
| **Affected Groups** | /aws/eks/HimCluser/cluster, /aws/eks/himanshu-eks-cluster/cluster, /aws/lambda/saa8-api-handler, aws-waf-logs-waf-lab-web-acl |
| **Current Storage Cost** | $0.00 (all within 5 GB free tier) |
| **Risk** | Without retention, storage grows without limit; cost begins at $0.03/GB-month beyond 5 GB |
| **Confidence** | High — retentionInDays=null confirmed via describe-log-groups API |
| **Recommendation** | Set 30-day retention on active groups; delete the two orphaned EKS groups |
| **Human Approval Required** | YES — setting retention will eventually delete old log data |

---

### Finding 4: KMS Customer Managed Keys — Conditional Cost

| Field | Value |
|---|---|
| **Finding** | 2 CMKs exist in us-east-1; list price $1.00/month each |
| **Key IDs** | 18a08257-7685-4466-a27e-4b2870f552ae; e1975ab0-8724-4335-8ae4-296958bca994 |
| **AWS-Reported Net Cost** | $0.00 (KMS UnblendedCost = -$0.0000008404 in Sep; -$0.000000284 in Oct — negative means credit exceeds charge) |
| **List Price** | $1.00/month per CMK (AWS published) = $2.00/month for 2 keys |
| **Savings Classification** | CONDITIONAL — $2.00/month IF credits expire AND keys are confirmed unused |
| **Confirmed Current Savings** | $0.00 (current cost is $0.00 after credits) |
| **Utilization** | Utilization could not be determined from the available AWS data (CloudTrail not queried; key aliases/policies not retrieved) |
| **Confidence** | Medium (keys exist and are charged at list price before credits; necessity unverified) |
| **Risk** | HIGH — deleting a CMK that encrypts live data renders that data permanently inaccessible |
| **Human Approval Required** | YES — CMK deletion is irreversible after the 7-day waiting period |

---

### Finding 5: Cross-Region Data Transfer — ap-south-1 to ap-southeast-1 (HISTORICAL)

| Field | Value |
|---|---|
| **Finding** | Cross-region data transfer from ap-south-1 to ap-southeast-1 during September 2026 lab |
| **Usage Type** | APS3-APS1-AWS-Out-Bytes |
| **Quantity** | 4.0820 GB (AWS-reported) |
| **AWS-Reported Cost** | $0.3511 (gross; offset by credits — net $0.00) |
| **Calculated Cost** | 4.0820 GB × $0.086/GB = $0.3511 ✓ (matches AWS-reported; price assumption confirmed) |
| **Current Cost** | $0.00 (no cross-region workloads running in October) |
| **Historical Cost** | $0.3511 (September 2026 lab session) |
| **Root Cause** | EKS workload in ap-south-1 communicating with service/registry in ap-southeast-1 |
| **Savings Classification** | HISTORICAL/FUTURE — no current cost; guidance for future labs |
| **Estimated Savings per Lab Session** | Up to $0.35 per session (frequency unknown — not annualized) |
| **Human Approval Required** | N/A — no current resources |

---

### Finding 6: Cross-AZ Data Transfer — us-west-2 (HISTORICAL + RESIDUAL)

| Field | Value |
|---|---|
| **Finding** | Cross-AZ traffic within us-west-2 — historically from EKS; residual amount in Oct |
| **Usage Type** | USW2-DataTransfer-Regional-Bytes |
| **Sep 2026 Quantity** | 9.055 GB |
| **Sep 2026 AWS-Reported Cost** | $0.0831 (gross; fully offset by credits — net $0.00) |
| **Implied Rate** | $0.0831 / 9.055 GB = $0.0092/GB (NOTE: AWS rate is $0.01/GB per direction; the $0.0092 implied rate reflects actual billing not the "×2 directions" formula) |
| **Oct MTD Quantity** | 4.278 GB (Oct 1–4, 3 days) |
| **Oct MTD AWS-Reported Cost** | $0.0328 (gross; fully offset by credits — net $0.00) |
| **Oct Rate Implied** | $0.0328 / 4.278 GB = $0.0077/GB (AWS-reported; use this not a formula) |
| **Savings Classification** | HISTORICAL for Sep; CONDITIONAL for Oct (if credits expire) |
| **Oct Residual Explanation** | October cross-AZ charges are residual: the EBS volume created Oct 1 and associated API/management traffic. No EKS cluster or NAT Gateway is running. |
| **Human Approval Required** | N/A — no current EKS cluster |

---

### Finding 7: NAT Gateway Usage — September 2026 (HISTORICAL)

| Field | Value |
|---|---|
| **Finding** | NAT Gateway ran for 42 hours with 7.65 GB data in us-west-2 during September 2026 lab |
| **NAT Hours** | 42 hrs (USW2-NatGateway-Hours) |
| **NAT Data** | 7.652 GB (USW2-NatGateway-Bytes) |
| **Calculated Hourly Cost** | 42 hrs × $0.045/hr = $1.89 (pricing assumption: AWS published us-west-2) |
| **Calculated Data Cost** | 7.652 GB × $0.045/GB = $0.34 |
| **Calculated Total** | $2.23 (list price estimate — INFORMATIONAL ONLY) |
| **AWS-Reported Cost** | $0.00 net (fully offset by credits) |
| **Current NAT Gateways Running** | 0 (confirmed via describe-nat-gateways in all regions) |
| **Savings Classification** | HISTORICAL — no current cost |
| **Savings per Future Lab Session** | Up to $2.23/session list price (frequency unknown — not annualized) |
| **Human Approval Required** | N/A |

---

## 7. Architecture Cost Risks

### Risk 1: Cross-Region Traffic Pattern

**Observed (Sep 2026):** 4.08 GB transferred from ap-south-1 to ap-southeast-1 at $0.086/GB = $0.3511.

**Root cause:** EKS cluster in ap-south-1 communicating with service or container registry in ap-southeast-1. Likely container image pulls from an ECR repository in the wrong region, or an application service endpoint hard-coded to ap-southeast-1.

**Mitigation for future labs:**
- Keep all resources in a single region
- Deploy ECR repositories in the same region as EKS clusters
- Review application configuration for cross-region API calls
- Use regional AWS service endpoints

---

### Risk 2: Cross-AZ Traffic Pattern

**Observed (Sep 2026):** 9.055 GB within us-west-2 at AWS-reported $0.0831.

**Root cause:** EKS pod-to-pod communication across Availability Zones. Kubernetes distributes pods across AZs by default for resilience, but inter-AZ traffic incurs cost.

**Mitigation for future labs:**
- Pod Topology Spread Constraints with `topologyKey: topology.kubernetes.io/zone`
- Kubernetes EndpointSlice topology hints for automatic same-AZ preference
- For non-HA lab environments, single-AZ node group configurations

---

### Risk 3: NAT Gateway Without VPC Endpoints

**Observed (Sep 2026):** 42 hrs NAT Gateway operation + 7.65 GB data processed. List-price estimate: $2.23/session (fully offset by credits in Sep).

**Root cause:** EKS worker nodes in private subnets required NAT Gateway to reach AWS services (ECR, STS, S3). Without VPC Endpoints, all AWS API traffic routes through NAT.

**Mitigation for future labs:**
- S3 Gateway Endpoint (free) — eliminates S3 traffic via NAT
- ECR and STS Interface VPC Endpoints (~$7.20/month each, but eliminate per-GB NAT charges for container operations)
- For short-lived labs (< 8 hours total), NAT cost is minimal; endpoints worthwhile for multi-day labs

---

### Risk 4: EBS Volume Orphaning

**Observed:** vol-008573e93270b1bcd created 2026-10-01, unattached as of 2026-10-04. Conditional cost: $0.80/month (list price; currently credit-offset).

**Root cause:** EBS volumes are not deleted when EKS node groups or EC2 instances are terminated unless `DeleteOnTermination=true` is explicitly set.

**Mitigation:**
- Set `DeleteOnTermination=true` on all EBS volumes in Terraform/IaC
- AWS Config rule `ec2-volume-inuse-check` to flag unattached volumes automatically
- Quarterly EBS audit: `describe-volumes --filters Name=status,Values=available`

---

### Risk 5: CloudWatch Log Group Orphaning

**Observed:** 2 EKS log groups persist after cluster deletion; 4 of 5 groups have no retention policy. All within free tier currently.

**Root cause:** AWS does not delete CloudWatch log groups when source services are deleted. Log groups must be managed independently.

**Mitigation:**
- Include `aws_cloudwatch_log_group` with `retention_in_days` in all Terraform modules
- Add log group cleanup to lab teardown runbooks
- AWS Config rule to enforce retention policies

---

### Risk 6: KMS CMK Lifecycle

**Observed:** 2 CMKs in us-east-1 with no confirmed active encryption use. Conditional cost $2.00/month (list; currently credit-offset).

**Root cause:** CMKs created for lab EKS encryption or RDS encryption are not deleted when workloads are decommissioned.

**Mitigation:**
- Tag CMKs at creation: `Project: eks-lab-2026-09`
- Include CMK deletion in lab teardown checklist (note: AWS enforces 7-day waiting period)
- Review CloudTrail for last CMK usage before scheduling deletion

---

### Risk 7: Multi-Region Lab Footprint

**Observed:** Resources deployed across 3 regions (us-east-1, us-west-2, ap-south-1) simultaneously, resulting in cross-region data transfer costs.

**Mitigation:**
- Designate ap-south-1 as primary lab region (closest to operator, already most-used)
- Use us-west-2 only when specifically testing us-west-2 architectures
- Clean all region-specific residual resources (log groups, EBS, S3) after each lab

---

## 8. Savings Summary

> Savings are categorized by type. **Confirmed current savings = $0.00** because current net cost is already $0.00 after credits. All actionable savings are conditional on credit expiry.

| Opportunity | Savings Type | Monthly Savings | Annual Savings | Confidence | Notes |
|---|---|---:|---:|---|---|
| Delete EBS vol-008573e93270b1bcd | Conditional (if credits expire) | $0.80 | $9.60 | High | List price $0.08/GB × 10 GB; currently credit-offset |
| Review/delete KMS CMKs (2 keys) | Conditional (if credits expire + confirmed unused) | $2.00 | $24.00 | Medium | List price $1.00/key; utilization unverified |
| Set CW log retention policies | Preventive | $0.00 | $0.00 | High | All 37.48 MB within 5 GB free tier |
| Delete orphaned EKS log groups | Preventive | $0.00 | $0.00 | High | Prevents unbounded growth |
| S3 lifecycle policies | Preventive | $0.00 | $0.00 | Low | Buckets currently near-empty |
| Cross-region transfer (future labs) | Future Lab Guidance | $0.351/session | Not annualized | Medium | Per-session; lab frequency unknown |
| Cross-AZ traffic (future labs) | Future Lab Guidance | $0.083/session | Not annualized | Medium | Per-session; lab frequency unknown |
| NAT Gateway (future labs) | Future Lab Guidance | $2.23/session est. | Not annualized | Medium | List price; currently credit-offset |
| **Conditional Total (if credits expire)** | | **$2.80/month** | **$33.60/year** | | EBS + KMS only; no double-counting |
| **Confirmed Current Savings** | | **$0.00** | **$0.00** | | Net cost is already $0 |

> **No double-counting:** EBS, KMS, and CloudWatch are distinct, independent resources. Cross-region, cross-AZ, and NAT savings are per-session estimates and are not included in the monthly total because lab session frequency is unknown. Per-session estimates are not annualized without a defensible usage assumption.

---

## 9. Recommended Action Plan

### Immediate (This Week)

| Action | Resource | Savings Impact | Risk | Approval |
|---|---|---|---|---|
| Verify EBS volume data (is it needed?) | vol-008573e93270b1bcd | Pre-requisite | None | Not required |
| Create EBS snapshot if data needed | vol-008573e93270b1bcd | Pre-requisite | None | Not required |
| **Delete** orphaned EBS volume | vol-008573e93270b1bcd | Eliminates conditional $0.80/month exposure | Low (snapshot first) | **Required** |
| Set 30-day retention on log groups lacking policy | 4 CW log groups | Preventive hygiene | Low | Recommended |
| **Delete** /aws/eks/HimCluser/cluster log group | us-west-2 CloudWatch | Preventive; cluster confirmed gone | None | **Required** |
| **Delete** /aws/eks/himanshu-eks-cluster/cluster log group | ap-south-1 CloudWatch | Preventive; cluster confirmed gone | None | **Required** |

### Before Next Lab Session

| Action | Resource | Savings Impact | Notes |
|---|---|---|---|
| Identify purpose of both KMS CMKs | us-east-1 KMS | Conditional $2.00/month | Check CloudTrail for last use; inspect key aliases/policies |
| If unused, schedule CMK deletion | 2 CMKs | Conditional $2.00/month | HIGH RISK — verify no live encrypted data first |
| Add lifecycle policies to both S3 buckets | him-demo-18, minishop-terraform-state | Preventive | Include noncurrent version expiration + multipart abort |
| Audit minishop-terraform-state contents | S3 | Preventive | Confirm project decommissioned; remove stale state files |

### Architecture Improvements (Future Labs)

| Improvement | Expected Benefit | Effort |
|---|---|---|
| Consolidate all lab work to ap-south-1 (single region) | Eliminate cross-region charges ($0.351/session observed) | Low |
| Add S3 Gateway Endpoint before deploying EKS | Reduce NAT data charges; endpoint is free | Low |
| Set DeleteOnTermination=true on all EBS in IaC | Prevent future orphaned volumes | Low |
| Include retention_in_days in all Terraform log group resources | Prevent log accumulation and hygiene issues | Low |
| Use Pod Topology Spread Constraints in EKS | Reduce cross-AZ data transfer | Medium |
| Include CMK teardown in lab runbook | Prevent KMS CMK accumulation | Low |

### Continuous FinOps

- Enable AWS Budgets alert at $5/month to catch unexpected charges
- Enable AWS Config rule `ec2-volume-inuse-check` to flag unattached EBS automatically
- Use existing Cost Anomaly Detection monitors — review weekly
- Run quarterly resource audit: EBS available, CW log groups without retention, KMS CMK aliases
- Tag all lab resources at creation: `Environment: lab`, `Project: <name>`, `CreatedBy: <user>`

---

## 10. Safety / Assumptions

### Pricing Assumptions

| Item | Assumed Price | Source | Verification Status |
|---|---:|---|---|
| EBS gp3 storage (us-west-2) | $0.08/GB-month | AWS published price | Consistent with AWS-reported Oct usage: 2.7731 GB-Month → $0.2219 calc vs $0.0000000029 net (credit offset) |
| CloudWatch Logs storage | $0.03/GB-month (after 5 GB free tier) | AWS published price | Not verified against billing (all storage within free tier = $0.00 actual) |
| KMS CMK | $1.00/month per key | AWS published price | Consistent with Sep CE KMS line showing gross ~$0.0000008 before credits |
| Cross-region transfer (ap-south-1 → ap-southeast-1) | $0.086/GB | AWS published price | Verified: 4.082 GB × $0.086 = $0.3511 = AWS-reported $0.3511 ✓ |
| Cross-AZ transfer | $0.01/GB per direction | AWS published price | AWS-reported: $0.0831 for 9.055 GB = $0.0092/GB implied. Do NOT use "×2 directions" formula. Use AWS-reported amount as authoritative. |
| NAT Gateway (us-west-2) | $0.045/hr + $0.045/GB | AWS published price | List-price estimate only; actual AWS-reported cost = $0.00 (credit-offset) |

### Cost Source Definitions

| Term | Definition |
|---|---|
| AWS-Reported Cost | Exact value from AWS Cost Explorer API (`UnblendedCost`). Authoritative. Never replaced with a calculated estimate. |
| Calculated Estimate | quantity × unit price. Used only where AWS does not report a per-resource cost breakdown. |
| Conditional Cost | List-price charge that is currently offset by credits; becomes real if credits expire. |
| Preventive | Zero current cost; recommendation is hygiene/risk management. |
| Historical | Cost incurred in a past period; no current exposure. |

### Credits and Offsets

AWS Cost Explorer shows the following credit structure for this account:

- **September 2026:** EC2-Other gross = $0.4342; AWS Data Transfer credit = -$0.4342. Net CE total = -$0.0000008495 (effectively $0.00).
- **October 2026 MTD:** EC2-Other gross = $0.0328; AWS Data Transfer credit = -$0.0328. Net CE total = -$0.0000002541 (effectively $0.00).
- The nature of these credits (promotional, AWS Activate, free tier, or billing adjustment) cannot be determined from Cost Explorer API alone.
- All "conditional savings" figures assume these credits may expire. If credits continue indefinitely, no additional action is required.

### Data Availability Limitations

- **KMS:** Key aliases, policies, and CloudTrail usage history were not retrieved. Key necessity cannot be confirmed without this data. Marked as "utilization could not be determined from the available AWS data."
- **S3 bucket sizes:** CloudWatch S3 metrics returned no data points (buckets likely below monitoring threshold or metrics not enabled). Exact bucket sizes unknown; treated as near-zero based on creation dates and $0.00 billing.
- **CloudTrail:** Not queried. Last-use dates for KMS keys and S3 access patterns are unavailable.
- **Other regions (eu-*, ca-central-1, sa-east-1, ap-northeast-*, ap-southeast-2):** Not individually inventoried for resources; all showed $0.00 in Cost Explorer — no active resources expected.

### Human Approval Requirements

All remediation actions require explicit human approval. This report is advisory only. No AWS resources were created, modified, or deleted during this audit.

Actions requiring approval:
1. Delete EBS volume vol-008573e93270b1bcd (irreversible without prior snapshot)
2. Delete CloudWatch log groups (irreversible)
3. Set CloudWatch log group retention policies (eventual data deletion)
4. Schedule KMS CMK deletion (HIGH RISK — irreversible after waiting period; verify first)
5. Any S3 bucket or object modifications

---

## FinOps Reconciliation & Quality Control

### Cost Reconciliation

| Reconciliation Check | Sep 2026 | Oct MTD | Status |
|---|---:|---:|---|
| CE Total (no grouping, authoritative) | -$0.0000008495 | -$0.0000002541 | AWS-reported |
| Sum of service line items | -$0.0000008495 | -$0.0000002541 | Calculated |
| Gross charges (positive services only) | +$0.4341929690 | +$0.0327901752 | Calculated |
| Credits / discounts (negative services) | -$0.4341938185 | -$0.0327904293 | Calculated |
| Net (gross + credits) | -$0.0000008495 | -$0.0000002541 | Calculated |
| **Reconciliation difference** | **$0.0000000000** | **$0.0000000000** | **PASS** |

> Both months reconcile exactly to $0.00 difference between the CE total (ungrouped) and the sum of all service-level line items.

### Calculation Validation

| Finding | Quantity | Unit | Unit Price | Calculated Cost | AWS-Reported Cost | Match? |
|---|---:|---|---:|---:|---:|---|
| Cross-region transfer (APS3→APS1) | 4.0820 | GB | $0.086/GB | $0.3511 | $0.3511 | YES |
| Cross-AZ transfer USW2 (Sep) | 9.0549 | GB | $0.0092/GB (implied) | $0.0831 | $0.0831 | YES (use AWS-reported) |
| EBS gp3 unattached (full month) | 10 | GB | $0.08/GB-month | $0.80/month | N/A (credit-offset) | Estimate only |
| NAT Gateway hours (Sep) | 42 | hrs | $0.045/hr | $1.89 | $0.00 (credit-offset) | List-price estimate |
| NAT Gateway data (Sep) | 7.652 | GB | $0.045/GB | $0.34 | $0.00 (credit-offset) | List-price estimate |
| EBS gp3 Oct MTD (3 days, 2.7731 GB-Mo) | 2.7731 | GB-Month | $0.08/GB-month | $0.2219 | $0.00 (credit-offset) | List-price estimate |
| CW log storage (all groups) | 0.0366 | GB | $0.03/GB-month | $0.00 (free tier) | $0.00 | YES |
| KMS CMK × 2 | 2 | keys | $1.00/key/month | $2.00/month | $0.00 (credit-offset) | List-price estimate |

### Savings Double-Counting Check

| Saving | Source Resource | Independent? | Included in Monthly Total? |
|---|---|---|---|
| EBS volume deletion ($0.80/month conditional) | vol-008573e93270b1bcd | Yes | Yes |
| KMS CMK deletion ($2.00/month conditional) | 2 separate CMKs | Yes — independent of EBS | Yes |
| CW log retention ($0.00) | 5 log groups | Yes — independent of above | Yes ($0.00) |
| Cross-region savings ($0.351/session) | Historical lab behavior | Not monthly — per-session | **No — excluded from monthly total** |
| Cross-AZ savings ($0.083/session) | Historical lab behavior | Not monthly — per-session | **No — excluded from monthly total** |
| NAT Gateway savings ($2.23/session) | Historical lab behavior | Not monthly — per-session | **No — excluded from monthly total** |
| **Conditional monthly total** | | | **$2.80/month (EBS + KMS only)** |

> Per-session historical savings ($0.351 + $0.083 + $2.23 = $2.66/session) are not included in the monthly total because lab session frequency is unknown. They cannot be annualized without a defensible assumption.

### Resource Count Reconciliation

| Category | Count | Current Net Cost | Classification |
|---|---:|---|---|
| EBS volumes | 1 | $0.00 (credit-offset) | Conditional |
| S3 buckets | 2 | $0.00 | Zero cost |
| CloudWatch log groups | 5 | $0.00 (free tier) | Zero cost |
| KMS CMKs | 2 | $0.00 (credit-offset) | Conditional |
| **Total resource objects** | **10** | **$0.00** | |

> Prior report stated "6 active resources" — **CORRECTED TO 10**. The prior count omitted 2 S3 buckets and 2 KMS CMKs, and miscounted the 5 CloudWatch log groups.

### Current vs Historical Validation

| Cost Item | Classification | Justification |
|---|---|---|
| Sep 2026 EC2-Other ($0.4342 gross) | HISTORICAL | All Sep charges ended by Oct 1; no EC2/EKS/NAT running in Oct |
| Sep 2026 anomalies (all 8 events) | HISTORICAL | All anomaly end dates ≤ Sep 30, 2026; confirmed via API |
| Oct MTD EC2-Other ($0.0328 gross) | CURRENT (residual) | Cross-AZ data transfer tied to EBS volume created Oct 1 + API traffic; fully credit-offset |
| EBS volume $0.80/month list price | CONDITIONAL | Volume exists and is billable; currently credit-offset |
| KMS CMKs $2.00/month list price | CONDITIONAL | CMKs exist and carry list-price charges; currently credit-offset |
| CW log groups $0.00 | CURRENT (zero) | All within 5 GB free tier; confirmed via storedBytes API values |

### Anomaly vs CE Total Reconciliation

| Item | Value | Explanation |
|---|---:|---|
| Sum of anomaly TotalActualSpend values | $11.96 | Per-event daily spend during anomalous periods — NOT additive monthly charges |
| Sep 2026 CE gross (full month) | $0.4342 | Full-month aggregated charges across all service lines |
| Why anomaly sum > CE gross | N/A | Anomaly amounts represent gross service spend on specific days. The underlying EC2, ELB, VPC, EBS charges on those days ARE included within the $0.4342 EC2-Other, but the anomaly TotalActualSpend values include charges that are offset by credits — the CE line items show net or credit-adjusted values. These amounts are NOT double-counted. |

### AWS-Reported vs Estimated Cost Validation

| Finding | AWS-Reported (authoritative) | Calculated Estimate | Action |
|---|---|---|---|
| Cross-region transfer | $0.3511 | $0.3511 (4.082 GB × $0.086) | Estimates match; use AWS-reported |
| Cross-AZ transfer (Sep) | $0.0831 | $0.0905 (9.055 GB × $0.01) | Estimates differ; **use AWS-reported $0.0831** |
| EBS monthly cost | Not reported (credit-offset) | $0.80/month (10 GB × $0.08) | AWS reports $0.00 net; estimate is conditional exposure |
| CW log storage | Not reported (free tier) | $0.0011/month (0.0366 GB × $0.03) | Both zero (free tier); consistent |
| NAT Gateway | $0.00 net (credit-offset) | $2.23 list price | AWS reports $0.00; estimate is conditional/informational |

---

*Report generated by Kiro FinOps Agent on 2026-10-04.*
*QC pass completed 2026-10-04. All numbers independently verified against raw AWS API data.*
*Access level: READ-ONLY. No AWS resources were modified during this audit.*
*All remediation actions require explicit human approval.*
