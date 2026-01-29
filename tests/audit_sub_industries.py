
import pandas as pd
df = pd.read_parquet('data/metadata.parquet')

def list_sub_industry(sub):
    sub_df = df[df['GICS Sub-Industry'] == sub]
    print(f"\n--- Sub-Industry: {sub} ({len(sub_df)} stocks) ---")
    for _, row in sub_df.iterrows():
        print(f"{row['Symbol']}: {row['Smart Tags']}")

# Social Media candidates
list_sub_industry('Interactive Media & Services')

# Gaming candidates
list_sub_industry('Interactive Home Entertainment')

# E-commerce candidates
list_sub_industry('Broadline Retail')

# EV candidates
list_sub_industry('Automobile Manufacturers')

# Robotics candidates
list_sub_industry('Industrial Machinery & Supplies & Components')
list_sub_industry('Industrial Machinery') # Checking variant
