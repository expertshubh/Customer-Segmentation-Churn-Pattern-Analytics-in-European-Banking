import pandas as pd

# ── Step 1: Load & Validate ────────────────────────────────────────────────
print("=" * 50)
print("  Nassau Candy — Churn Analysis Script")
print("=" * 50)

df = pd.read_csv('data/churn.csv')
print(f"\n✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"   Null values: {df.isnull().sum().sum()}")
print(f"   Duplicate rows: {df.duplicated().sum()}")
print(f"\n   Binary check — Exited: {sorted(df['Exited'].unique())}")
print(f"   Binary check — IsActiveMember: {sorted(df['IsActiveMember'].unique())}")
print(f"   Binary check — HasCrCard: {sorted(df['HasCrCard'].unique())}")

# ── Step 2: Clean ──────────────────────────────────────────────────────────
df.drop(columns=['CustomerId', 'Surname'], inplace=True)
print("\n✅ Removed non-analytical fields: CustomerId, Surname")

# ── Step 3: Segmentation ──────────────────────────────────────────────────
df['AgeGroup'] = pd.cut(df['Age'], bins=[0,30,45,60,100],
                         labels=['<30','30-45','46-60','60+'])
df['CreditBand'] = pd.cut(df['CreditScore'], bins=[0,580,670,850],
                           labels=['Low','Medium','High'])
df['TenureGroup'] = pd.cut(df['Tenure'], bins=[-1,2,5,10],
                            labels=['New','Mid-term','Long-term'])
df['BalanceSegment'] = pd.cut(df['Balance'], bins=[-1,0,50000,250000],
                               labels=['Zero','Low','High'])
print("\n✅ Segmentation columns created: AgeGroup, CreditBand, TenureGroup, BalanceSegment")

# ── Step 4: KPI Results ───────────────────────────────────────────────────
overall_churn  = df['Exited'].mean() * 100
geo_churn      = df.groupby('Geography')['Exited'].mean() * 100
age_churn      = df.groupby('AgeGroup', observed=True)['Exited'].mean() * 100
gender_churn   = df.groupby('Gender')['Exited'].mean() * 100
tenure_churn   = df.groupby('TenureGroup', observed=True)['Exited'].mean() * 100
balance_churn  = df.groupby('BalanceSegment', observed=True)['Exited'].mean() * 100
credit_churn   = df.groupby('CreditBand', observed=True)['Exited'].mean() * 100
active_churn   = df.groupby('IsActiveMember')['Exited'].mean() * 100
products_churn = df.groupby('NumOfProducts')['Exited'].mean() * 100

geo_risk_index = geo_churn.max() - geo_churn.min()
inactive_churn = active_churn.get(0, 0)
active_churn_r = active_churn.get(1, 0)

print("\n===== CHURN ANALYSIS RESULTS =====")
print(f"\nOverall Churn Rate: {overall_churn:.2f}%")

print("\nChurn Rate by Country:")
print(geo_churn.to_string())
print(f"\n  → Geographic Risk Index: {geo_risk_index:.2f}%")

print("\nChurn Rate by Age Group:")
print(age_churn.to_string())

print("\nChurn Rate by Gender:")
print(gender_churn.to_string())

print("\nChurn Rate by Tenure Group:")
print(tenure_churn.to_string())

print("\nChurn Rate by Balance Segment:")
print(balance_churn.to_string())

print("\nChurn Rate by Credit Band:")
print(credit_churn.to_string())

print("\nEngagement Drop Indicator:")
print(f"  Inactive members churn rate: {inactive_churn:.2f}%")
print(f"  Active members churn rate:   {active_churn_r:.2f}%")
print(f"  Risk multiplier: {inactive_churn/active_churn_r:.1f}x")

print("\nChurn Rate by Number of Products:")
print(products_churn.to_string())

# ── Step 5: Churned vs Retained Profile ───────────────────────────────────
profile = df.groupby('Exited').agg(
    Avg_Age         = ('Age',            'mean'),
    Avg_CreditScore = ('CreditScore',    'mean'),
    Avg_Balance     = ('Balance',        'mean'),
    Avg_Salary      = ('EstimatedSalary','mean'),
    Avg_Tenure      = ('Tenure',         'mean'),
).round(2)
profile.index = ['Retained', 'Churned']

print("\nChurned vs Retained Profile:")
print(profile.to_string())

print("\n✅ Analysis complete!")
