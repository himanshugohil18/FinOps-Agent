#!/usr/bin/env bash
# =============================================================================
# AWS FinOps Audit Script
# =============================================================================
# Collects cost and resource data from AWS using read-only API calls.
# Requires: aws CLI configured with appropriate read-only IAM permissions.
#
# Usage:
#   chmod +x finops_audit.sh
#   ./finops_audit.sh
#
# Output:
#   raw_data/  — JSON dumps of all AWS API responses
#
# Safety:
#   READ-ONLY — This script makes no changes to any AWS resources.
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/../raw_data"
DATE=$(date +%Y-%m-%d)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "================================================="
echo "  AWS FinOps Audit — READ-ONLY"
echo "  Account : ${ACCOUNT_ID}"
echo "  Date    : ${DATE}"
echo "  Output  : ${OUTPUT_DIR}"
echo "================================================="
echo ""

mkdir -p "${OUTPUT_DIR}"

# ── Step 1: Identity ──────────────────────────────────────────────────────
echo "[1/8] Account identity..."
aws sts get-caller-identity \
  > "${OUTPUT_DIR}/identity.json"

# ── Step 2: September costs by service ───────────────────────────────────
echo "[2/8] September cost breakdown..."
PREV_MONTH_START=$(date -d "$(date +%Y-%m-01) -1 month" +%Y-%m-01 2>/dev/null || \
  python3 -c "from datetime import date; d=date.today().replace(day=1); import calendar; print((d.replace(month=d.month-1) if d.month>1 else d.replace(year=d.year-1,month=12)).strftime('%Y-%m-01'))")
PREV_MONTH_END=$(date +%Y-%m-01)

aws ce get-cost-and-usage \
  --time-period Start="${PREV_MONTH_START}",End="${PREV_MONTH_END}" \
  --granularity MONTHLY \
  --metrics UnblendedCost UsageQuantity \
  --group-by Type=DIMENSION,Key=SERVICE \
  > "${OUTPUT_DIR}/cost_by_service_prev_month.json"

# ── Step 3: Current MTD costs ─────────────────────────────────────────────
echo "[3/8] Current MTD cost breakdown..."
MTD_START=$(date +%Y-%m-01)
MTD_END=$(date +%Y-%m-%d)

aws ce get-cost-and-usage \
  --time-period Start="${MTD_START}",End="${MTD_END}" \
  --granularity MONTHLY \
  --metrics UnblendedCost UsageQuantity \
  --group-by Type=DIMENSION,Key=SERVICE \
  > "${OUTPUT_DIR}/cost_by_service_mtd.json"

# CE total (no grouping) for reconciliation
aws ce get-cost-and-usage \
  --time-period Start="${PREV_MONTH_START}",End="${PREV_MONTH_END}" \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  > "${OUTPUT_DIR}/ce_total_prev_month.json"

aws ce get-cost-and-usage \
  --time-period Start="${MTD_START}",End="${MTD_END}" \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  > "${OUTPUT_DIR}/ce_total_mtd.json"

# ── Step 4: Cost anomalies ────────────────────────────────────────────────
echo "[4/8] Cost anomaly detection..."
ANOMALY_START=$(date -d "90 days ago" +%Y-%m-%d 2>/dev/null || \
  python3 -c "from datetime import date, timedelta; print((date.today()-timedelta(days=90)).strftime('%Y-%m-%d'))")

aws ce get-anomalies \
  --date-interval StartDate="${ANOMALY_START}",EndDate="${MTD_END}" \
  --max-results 50 \
  > "${OUTPUT_DIR}/anomalies.json" 2>/dev/null || \
  echo '{"Anomalies":[]}' > "${OUTPUT_DIR}/anomalies.json"

# ── Step 5: EC2-Other usage type breakdown ────────────────────────────────
echo "[5/8] EC2-Other usage type breakdown..."
aws ce get-cost-and-usage \
  --time-period Start="${PREV_MONTH_START}",End="${PREV_MONTH_END}" \
  --granularity MONTHLY \
  --metrics UnblendedCost UsageQuantity \
  --group-by Type=DIMENSION,Key=USAGE_TYPE \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["EC2 - Other"]}}' \
  > "${OUTPUT_DIR}/ec2_other_usage_types.json"

# ── Step 6: Resource inventory ────────────────────────────────────────────
echo "[6/8] Resource inventory (us-east-1, us-west-2, ap-south-1)..."

for REGION in us-east-1 us-west-2 ap-south-1; do
  SAFE="${REGION//-/_}"

  # EBS volumes
  aws ec2 describe-volumes \
    --region "${REGION}" \
    --query 'Volumes[*].{VolumeId:VolumeId,State:State,Size:Size,VolumeType:VolumeType,CreateTime:CreateTime,Attachments:Attachments,AZ:AvailabilityZone}' \
    > "${OUTPUT_DIR}/ebs_volumes_${SAFE}.json"

  # EBS snapshots (self-owned)
  aws ec2 describe-snapshots \
    --owner-ids self \
    --region "${REGION}" \
    --query 'Snapshots[*].{SnapshotId:SnapshotId,VolumeSize:VolumeSize,StartTime:StartTime,State:State}' \
    > "${OUTPUT_DIR}/ebs_snapshots_${SAFE}.json"

  # NAT Gateways
  aws ec2 describe-nat-gateways \
    --region "${REGION}" \
    --query 'NatGateways[*].{NatGatewayId:NatGatewayId,State:State,VpcId:VpcId,CreateTime:CreateTime}' \
    > "${OUTPUT_DIR}/nat_gateways_${SAFE}.json"

  # Load Balancers
  aws elbv2 describe-load-balancers \
    --region "${REGION}" \
    --query 'LoadBalancers[*].{Name:LoadBalancerName,Type:Type,State:State.Code,DNSName:DNSName}' \
    > "${OUTPUT_DIR}/load_balancers_${SAFE}.json"

  # CloudWatch log groups
  aws logs describe-log-groups \
    --region "${REGION}" \
    --query 'logGroups[*].{logGroupName:logGroupName,retentionInDays:retentionInDays,storedBytes:storedBytes}' \
    > "${OUTPUT_DIR}/cloudwatch_log_groups_${SAFE}.json"

  # EKS clusters
  aws eks list-clusters \
    --region "${REGION}" \
    --query 'clusters' \
    > "${OUTPUT_DIR}/eks_clusters_${SAFE}.json"

  # RDS instances
  aws rds describe-db-instances \
    --region "${REGION}" \
    --query 'DBInstances[*].{ID:DBInstanceIdentifier,Class:DBInstanceClass,Engine:Engine,Status:DBInstanceStatus}' \
    > "${OUTPUT_DIR}/rds_instances_${SAFE}.json"
done

# ── Step 7: Global resources ──────────────────────────────────────────────
echo "[7/8] Global resources..."

# S3 buckets
aws s3api list-buckets \
  --query 'Buckets[*].{Name:Name,CreationDate:CreationDate}' \
  > "${OUTPUT_DIR}/s3_buckets.json"

# KMS keys
aws kms list-keys \
  --region us-east-1 \
  --query 'Keys[*].{KeyId:KeyId,KeyArn:KeyArn}' \
  > "${OUTPUT_DIR}/kms_keys.json"

# EC2 instances (all three regions)
for REGION in us-east-1 us-west-2 ap-south-1; do
  SAFE="${REGION//-/_}"
  aws ec2 describe-instances \
    --region "${REGION}" \
    --query 'Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType,State:State.Name,Launch:LaunchTime}' \
    > "${OUTPUT_DIR}/ec2_instances_${SAFE}.json"
done

# ── Step 8: Summary ───────────────────────────────────────────────────────
echo "[8/8] Done."
echo ""
echo "Raw data written to: ${OUTPUT_DIR}/"
echo "Files collected     : $(ls "${OUTPUT_DIR}" | wc -l)"
echo ""
echo "Next step: run finops_report.py to generate the full report"
echo "  python3 scripts/finops_report.py"
