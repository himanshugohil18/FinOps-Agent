# Required IAM Permissions

The FinOps agent requires a read-only IAM user or role. No write permissions are needed.

## Minimum IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "FinOpsReadOnly",
      "Effect": "Allow",
      "Action": [
        "sts:GetCallerIdentity",
        "ce:GetCostAndUsage",
        "ce:GetAnomalies",
        "ce:GetAnomalyMonitors",
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeSnapshots",
        "ec2:DescribeImages",
        "ec2:DescribeNatGateways",
        "ec2:DescribeVpcEndpoints",
        "ec2:DescribeRegions",
        "elasticloadbalancing:DescribeLoadBalancers",
        "eks:ListClusters",
        "eks:DescribeCluster",
        "ecs:ListClusters",
        "ecs:DescribeClusters",
        "ecs:ListServices",
        "lambda:ListFunctions",
        "rds:DescribeDBInstances",
        "rds:DescribeDBClusters",
        "s3:ListAllMyBuckets",
        "s3:GetBucketLocation",
        "s3:GetBucketVersioning",
        "s3:GetLifecycleConfiguration",
        "ecr:DescribeRepositories",
        "kms:ListKeys",
        "kms:DescribeKey",
        "kms:ListAliases",
        "logs:DescribeLogGroups",
        "cloudwatch:GetMetricStatistics",
        "iam:ListAccountAliases",
        "backup:ListBackupPlans",
        "backup:ListRecoveryPointsByBackupVault"
      ],
      "Resource": "*"
    }
  ]
}
```

## AWS Managed Policies (Alternative)

You can also attach these AWS managed policies:
- `ReadOnlyAccess` — covers all services above
- `AWSCostAndUsageReportAutomationPolicy` — for Cost Explorer access

## Notes

- **No write permissions** are required or used
- The agent never modifies, deletes, stops, or provisions any resources
- All remediation actions require explicit human approval outside of this tool
- Credentials should be configured via `aws configure` or IAM role (for EC2/EKS)
- Never commit credentials, `.pem` files, or access keys to this repository
