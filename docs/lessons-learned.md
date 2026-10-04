# FinOps Lessons Learned

Key engineering lessons from building and validating this AWS FinOps agent.
All observations are based on the verified audit data from the 2026-10-04 audit run.

---

## 1. Historical Spend ≠ Current Spend

**Problem:** It is easy to look at anomaly data or prior-month costs and treat them as ongoing charges.

**Example:** Eight cost anomalies were detected in September 2026 (EKS, NAT Gateway, ELB, EBS). All ended by September 30. None were generating cost in October. They must be clearly labelled as **HISTORICAL** — not presented as current issues requiring action.

**Rule:** Every cost item in a FinOps report must state whether it is:
- Current ongoing spend (active right now)
- Historical spend (past period, no longer active)
- Conditional exposure (exists but currently offset by credits)
- Estimated future spend (projection)

---

## 2. Anomaly Event Totals ≠ Monthly Billing Totals

**Problem:** AWS Cost Anomaly Detection reports `TotalActualSpend` per anomaly event. These are per-event amounts covering anomalous *days*, not full months.

**Example:** Eight anomaly events had a combined `TotalActualSpend` of ~$11.96. The September monthly total (CE) was $0.4342 gross. The anomaly amounts are not additive to the monthly total — they are sub-period daily peaks already embedded within the monthly service-level costs.

**Rule:** Never add anomaly `TotalActualSpend` values together to produce a "total anomaly impact" figure, and never compare them directly to a monthly CE total.

---

## 3. Credits Can Hide Real Gross Usage

**Problem:** AWS credits (promotional, Activate, educational, or billing adjustments) appear as negative line items in Cost Explorer and can make net billing appear near $0 even when real gross usage exists.

**Example:** September gross charges were $0.4342 (EC2-Other: data transfer, NAT, EBS). AWS Data Transfer credits of -$0.4342 fully offset them. Net CE total = -$0.0000008495 (~$0.00).

**Implications:**
- If credits expire, the account's actual monthly bill would be ~$0.40–$2.80+/month depending on usage
- A FinOps report showing only net cost misses the underlying gross usage pattern
- Always report: gross charges | credits applied | net cost — separately

---

## 4. Unit Conversion Errors Kill Accuracy

**Problem:** Mixing MB and GB in storage cost calculations produces errors of 1000×.

**Example (caught in QC):** CloudWatch log storage was initially calculated as ~$0.19/month:
```
38 MB × $0.03/GB-month = $1.14  ← WRONG (treating MB as GB)
```
Correct calculation:
```
38 MB = 0.037 GB → 0.037 × $0.03 = $0.0011/month
All storage within 5 GB free tier → actual cost = $0.00
```

**Rule:** Always convert to the same unit as the pricing tier before multiplying. Label all quantities with their unit. Never omit "per GB" vs "per MB" distinctions.

---

## 5. Use AWS-Reported Costs as Authoritative

**Problem:** Calculating expected cost from quantity × unit price and then using that calculated value instead of the AWS-reported actual cost introduces avoidable errors.

**Example:** Cross-AZ transfer was initially shown as `9.05 GB × $0.01/GB × 2 directions = $0.1811`. The AWS-reported actual cost was $0.0831. The formula was wrong — AWS applies the rate to one direction only in this case, and the exact rate implied from the AWS data is $0.0092/GB, not $0.01/GB.

**Rule:**
- If AWS reports an exact cost, use that as the authoritative value
- If you show a calculated estimate alongside, label it clearly as an estimate
- Show the difference and explain it if they diverge

---

## 6. Conditional Savings ≠ Confirmed Savings

**Problem:** A resource that exists with a list-price cost but is currently credit-offset does not represent a confirmed saving if deleted. The current net cost is $0.00 — deleting it only avoids a future charge if credits expire.

**Example:** EBS volume `vol-008573e93270b1bcd` has a list price of $0.80/month. AWS Cost Explorer reports it at -$0.0000000029 (credit-offset). The saving from deletion is **conditional** on credits expiring.

**Rule:**
- Confirmed saving = current net cost > $0, resource can be removed
- Conditional saving = current net cost = $0 (credit-offset), but list price exists
- Preventive = no current cost and no foreseeable future cost; value is hygiene only
- Label each category separately; do not aggregate them

---

## 7. Orphaned Resources After Lab Teardown

**Observed patterns in this account:**
- EBS volume created with EKS cluster, not deleted after cluster teardown → `vol-008573e93270b1bcd` (us-west-2, 10 GB, created Oct 1)
- CloudWatch log groups from deleted EKS clusters (`/aws/eks/HimCluser/cluster`, `/aws/eks/himanshu-eks-cluster/cluster`) — AWS does not auto-delete log groups when clusters are deleted
- KMS CMKs created for EKS encryption — not deleted after cluster decommission

**Best practices:**
- Set `DeleteOnTermination=true` on all EBS volumes in Terraform/IaC
- Include `aws_cloudwatch_log_group` with `retention_in_days` in all Terraform modules
- Include CMK + log group cleanup in every lab teardown runbook
- Run post-teardown audit: `aws ec2 describe-volumes --filters Name=status,Values=available`

---

## 8. EKS + NAT Gateway Architecture Cost Pattern

**Observed:** A short-lived EKS lab in us-west-2 (September 2026) generated:
- NAT Gateway: 42 hours × $0.045/hr = $1.89 (list price)
- NAT data processing: 7.65 GB × $0.045/GB = $0.34 (list price)
- Cross-AZ traffic: 9.055 GB → $0.0831 (AWS-reported)
- Cross-region traffic: 4.082 GB ap-south-1 → ap-southeast-1 → $0.3511 (AWS-reported)

All fully offset by credits in this case, but the architectural patterns are real.

**Cost-reduction patterns:**
- S3 Gateway Endpoint (free) — eliminates S3 traffic through NAT
- Keep ECR in same region as EKS — eliminates cross-region image pulls
- Pod Topology Spread Constraints — reduces cross-AZ pod traffic
- For short labs: consider single-AZ deployments and public subnets with tight security groups

---

## 9. Report Every Gap Explicitly

A FinOps report that hides its limitations is less trustworthy than one that states them.

In this audit, the following were explicitly disclosed as data gaps:
- KMS key necessity: **40% confidence** — CloudTrail not queried; key usage could not be verified
- S3 bucket sizes: **30% confidence** — CloudWatch S3 metrics not enabled; exact sizes unknown
- Credit nature: **50% confidence** — credit type (promotional vs. educational vs. free tier) could not be determined from Cost Explorer API alone

**Rule:** If a finding cannot be supported by AWS data, state:
> "Resource-level cost could not be determined from the available AWS data."

If a calculation cannot be verified, mark it:
> "UNVERIFIED — requires additional AWS data."

---

## 10. Always Reconcile Before Publishing

The QC pass on this report found 8 errors before publication:

| Error | Impact |
|---|---|
| Resource count: 6 vs actual 10 | Understated inventory |
| CW cost $0.19/mo vs actual $0.00 | Off by ~170× (MB treated as GB) |
| Cross-AZ formula incorrect | Wrong methodology; use AWS-reported value |
| Savings shown as confirmed vs conditional | Misrepresented credit-offset savings |
| Oct MTD gross vs net not distinguished | Misleading headline number |
| EBS creation date wrong | Wrong root-cause explanation |
| Anomaly totals vs CE totals conflated | Incorrect reconciliation |
| KMS labeled as confirmed saving | Overstated; key usage unverified |

**Rule:** Before publishing any FinOps report:
1. Reconcile CE total (no grouping) against sum of service line items → difference must be $0.00
2. Verify every unit (MB vs GB, hours vs days, per-direction vs round-trip)
3. Re-check every "savings" claim: is the current net cost actually > $0?
4. Verify all anomaly dates: are they current or historical?
5. State confidence and data gaps explicitly
