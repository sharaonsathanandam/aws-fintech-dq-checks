import sys
import pandas as pd
import boto3

# ——— Define configurations ———
input_path   = 's3://fintech-data-lake-2/data/raw/*/data.parquet'
output_path  = 's3://fintech-data-lake-2/data/curated/*/cleaned.parquet'
null_thresh  = 0.01
dup_thresh   = 0.01

# ——— Load data ———
df = pd.read_csv(input_path)

# ——— Perform checks ———
total    = len(df)
nulls    = df['transaction_id'].isnull().sum()
dups     = total - df['transaction_id'].nunique() if total else 0
dup_rate = dups / total if total else 0.0

# ——— Send metrics to CloudWatch ———
cw = boto3.client('cloudwatch')
cw.put_metric_data(
    Namespace='DQ',
    MetricData=[
        {'MetricName': 'NullCount',   'Value': nulls},
        {'MetricName': 'DupRate',     'Value': dup_rate}
    ]
)

# ——— Report & fail on SLA breach ———
print(f"Total rows: {total}, Nulls: {nulls}, DupRate: {dup_rate:.2%}")
if nulls > null_thresh or dup_rate > dup_thresh:
    print('QUALITY CHECK FAILED', file=sys.stderr)
    sys.exit(1)

# ——— Write cleaned output ———
df.to_parquet(output_path, index=False)
print(f"Wrote cleaned data to {output_path}")