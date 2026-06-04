import streamlit as st
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Bank Churn Analytics", layout="wide", page_icon="🏦")

# ── LOAD & PREPARE DATA ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'churn.csv'))
    df.drop(columns=['CustomerId', 'Surname'], inplace=True)
    df['AgeGroup']       = pd.cut(df['Age'],            bins=[0,30,45,60,100],       labels=['<30','30-45','46-60','60+'])
    df['CreditBand']     = pd.cut(df['CreditScore'],    bins=[0,580,670,850],         labels=['Low','Medium','High'])
    df['TenureGroup']    = pd.cut(df['Tenure'],         bins=[-1,2,5,10],             labels=['New','Mid-term','Long-term'])
    df['BalanceSegment'] = pd.cut(df['Balance'],        bins=[-1,0,50000,250000],     labels=['Zero','Low','High'])
    df['SalaryBand']     = pd.cut(df['EstimatedSalary'],bins=[0,50000,100000,200000], labels=['Low (<50k)','Mid (50-100k)','High (>100k)'])
    return df

df = load_data()

# ── SIDEBAR FILTERS ────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/bank-building.png", width=60)
st.sidebar.title("🔍 Filters")

geo_sel     = st.sidebar.multiselect("Country",        df['Geography'].unique(),                    default=list(df['Geography'].unique()))
gender_sel  = st.sidebar.multiselect("Gender",         df['Gender'].unique(),                       default=list(df['Gender'].unique()))

st.sidebar.markdown("---")
st.sidebar.header("🔎 Drill-Down")
age_sel     = st.sidebar.multiselect("Age Group",      list(df['AgeGroup'].cat.categories),         default=list(df['AgeGroup'].cat.categories))
balance_sel = st.sidebar.multiselect("Balance Segment",list(df['BalanceSegment'].cat.categories),   default=list(df['BalanceSegment'].cat.categories))

filtered = df[
    df['Geography'].isin(geo_sel) &
    df['Gender'].isin(gender_sel) &
    df['AgeGroup'].isin(age_sel) &
    df['BalanceSegment'].isin(balance_sel)
]

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.title("🏦 European Banking — Customer Churn Analytics")
st.caption("Segmentation-driven churn analysis across geography, demographics, and financial profile")
st.markdown("---")

# ── KPI CARDS (5 required KPIs) ───────────────────────────────────────────────
st.subheader("📌 Key Performance Indicators")

total         = len(filtered)
churned       = int(filtered['Exited'].sum())
overall_rate  = filtered['Exited'].mean()*100 if total > 0 else 0

hv_df         = filtered[filtered['Balance'] > 50000]
hv_rate       = hv_df['Exited'].mean()*100 if len(hv_df) > 0 else 0

geo_risk_val  = filtered.groupby('Geography')['Exited'].mean().max()*100 if total > 0 else 0

inactive      = filtered[filtered['IsActiveMember']==0]
active        = filtered[filtered['IsActiveMember']==1]
inactive_rate = inactive['Exited'].mean()*100 if len(inactive) > 0 else 0
active_rate   = active['Exited'].mean()*100   if len(active)   > 0 else 0
engagement_drop = inactive_rate - active_rate

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📉 Overall Churn Rate",     f"{overall_rate:.1f}%",   f"{total:,} customers")
k2.metric("💎 High-Value Churn Ratio", f"{hv_rate:.1f}%",        f"{len(hv_df):,} HV customers")
k3.metric("🌍 Geographic Risk Index",  f"{geo_risk_val:.1f}%",   "Highest country risk")
k4.metric("📊 Segment Churn Rate",     f"{overall_rate:.1f}%",   f"{churned:,} churned")
k5.metric("⚡ Engagement Drop",        f"+{engagement_drop:.1f}%","Inactive vs Active")

st.markdown("---")

# ── ROW 1: Geography & Gender ──────────────────────────────────────────────────
st.subheader("🌍 Geographic & Gender Analysis")
c1, c2 = st.columns(2)

with c1:
    geo_data = filtered.groupby('Geography')['Exited'].mean()*100
    fig = px.bar(geo_data.reset_index(), x='Geography', y='Exited',
                 color='Geography', text_auto='.1f',
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 labels={'Exited':'Churn Rate (%)'}, title="Churn Rate by Country")
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, yaxis_range=[0, geo_data.max()*1.3])
    st.plotly_chart(fig, use_container_width=True)

with c2:
    gen_data = filtered.groupby('Gender')['Exited'].mean()*100
    fig2 = px.pie(gen_data.reset_index(), names='Gender', values='Exited',
                  color_discrete_sequence=['#636EFA','#EF553B'],
                  title="Churn Rate by Gender", hole=0.4)
    fig2.update_traces(textinfo='label+percent')
    st.plotly_chart(fig2, use_container_width=True)

# ── ROW 2: Age & Tenure ────────────────────────────────────────────────────────
st.subheader("🎂 Age & Tenure Churn Patterns")
c3, c4 = st.columns(2)

with c3:
    age_data = filtered.groupby('AgeGroup', observed=True)['Exited'].mean()*100
    fig3 = px.bar(age_data.reset_index(), x='AgeGroup', y='Exited',
                  color='AgeGroup', text_auto='.1f',
                  color_discrete_sequence=px.colors.sequential.RdBu_r,
                  labels={'Exited':'Churn Rate (%)'}, title="Churn Rate by Age Group")
    fig3.update_traces(textposition='outside')
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    ten_data = filtered.groupby('TenureGroup', observed=True)['Exited'].mean()*100
    fig4 = px.bar(ten_data.reset_index(), x='TenureGroup', y='Exited',
                  color='TenureGroup', text_auto='.1f',
                  color_discrete_sequence=px.colors.qualitative.Pastel,
                  labels={'Exited':'Churn Rate (%)'}, title="Churn Rate by Tenure Group")
    fig4.update_traces(textposition='outside')
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# ── ROW 3: Balance & Credit ────────────────────────────────────────────────────
st.subheader("💰 Financial Profile Analysis")
c5, c6 = st.columns(2)

with c5:
    bal_data = filtered.groupby('BalanceSegment', observed=True)['Exited'].mean()*100
    fig5 = px.bar(bal_data.reset_index(), x='BalanceSegment', y='Exited',
                  color='BalanceSegment', text_auto='.1f',
                  labels={'Exited':'Churn Rate (%)'}, title="Churn Rate by Balance Segment")
    fig5.update_traces(textposition='outside')
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with c6:
    cred_data = filtered.groupby('CreditBand', observed=True)['Exited'].mean()*100
    fig6 = px.bar(cred_data.reset_index(), x='CreditBand', y='Exited',
                  color='CreditBand', text_auto='.1f',
                  labels={'Exited':'Churn Rate (%)'}, title="Churn Rate by Credit Score Band")
    fig6.update_traces(textposition='outside')
    fig6.update_layout(showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ── GEOGRAPHY × AGE HEATMAP (KEY REQUIREMENT) ─────────────────────────────────
st.subheader("🔥 Geography × Age Interaction Heatmap")
st.caption("Identifies highest-risk demographic segments — Germany 46–60 is the critical zone")

heat_data = filtered.groupby(['Geography','AgeGroup'], observed=True)['Exited'].mean()*100
heat_pivot = heat_data.unstack().fillna(0)

fig_heat = go.Figure(data=go.Heatmap(
    z=heat_pivot.values,
    x=[str(c) for c in heat_pivot.columns],
    y=heat_pivot.index.tolist(),
    colorscale='RdYlGn_r',
    text=[[f"{v:.1f}%" for v in row] for row in heat_pivot.values],
    texttemplate="%{text}",
    textfont={"size": 14, "color": "white"},
    colorbar=dict(title="Churn Rate %")
))
fig_heat.update_layout(
    xaxis_title="Age Group",
    yaxis_title="Country",
    height=300,
    font=dict(size=13)
)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")

# ── HIGH-VALUE CUSTOMER CHURN EXPLORER ────────────────────────────────────────
st.subheader("💎 High-Value Customer Churn Explorer")

hv_df2 = filtered[filtered['Balance'] > 50000].copy()
if len(hv_df2) > 0:
    h1, h2, h3, h4 = st.columns(4)
    h1.metric("HV Customers",      f"{len(hv_df2):,}")
    h2.metric("HV Churned",        f"{int(hv_df2['Exited'].sum()):,}")
    h3.metric("HV Churn Rate",     f"{hv_df2['Exited'].mean()*100:.1f}%")
    h4.metric("Balance at Risk €", f"{hv_df2[hv_df2['Exited']==1]['Balance'].sum():,.0f}")

    c7, c8 = st.columns(2)
    with c7:
        hv_geo = hv_df2.groupby('Geography')['Exited'].mean()*100
        fig7 = px.bar(hv_geo.reset_index(), x='Geography', y='Exited',
                      color='Geography', text_auto='.1f',
                      labels={'Exited':'Churn Rate (%)'},
                      title="High-Value Churn by Country")
        fig7.update_layout(showlegend=False)
        st.plotly_chart(fig7, use_container_width=True)

    with c8:
        hv_age = hv_df2.groupby('AgeGroup', observed=True)['Exited'].mean()*100
        fig8 = px.bar(hv_age.reset_index(), x='AgeGroup', y='Exited',
                      color='AgeGroup', text_auto='.1f',
                      color_discrete_sequence=px.colors.sequential.Reds,
                      labels={'Exited':'Churn Rate (%)'},
                      title="High-Value Churn by Age Group")
        fig8.update_layout(showlegend=False)
        st.plotly_chart(fig8, use_container_width=True)
else:
    st.warning("No high-value customers match current filters.")

st.markdown("---")

# ── ENGAGEMENT & ACTIVITY ANALYSIS ────────────────────────────────────────────
st.subheader("⚡ Engagement Drop Indicator")
st.caption("Inactive members are nearly 2× more likely to churn")

c9, c10 = st.columns(2)
with c9:
    eng_data = filtered.groupby('IsActiveMember')['Exited'].mean()*100
    eng_df = eng_data.reset_index()
    eng_df['Status'] = eng_df['IsActiveMember'].map({0:'Inactive',1:'Active'})
    fig9 = px.bar(eng_df, x='Status', y='Exited',
                  color='Status', text_auto='.1f',
                  color_discrete_map={'Inactive':'#EF553B','Active':'#00CC96'},
                  labels={'Exited':'Churn Rate (%)'},
                  title="Churn Rate: Active vs Inactive Members")
    fig9.update_layout(showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)

with c10:
    prod_data = filtered.groupby('NumOfProducts')['Exited'].mean()*100
    fig10 = px.bar(prod_data.reset_index(), x='NumOfProducts', y='Exited',
                   color='NumOfProducts', text_auto='.1f',
                   labels={'Exited':'Churn Rate (%)','NumOfProducts':'# Products'},
                   title="Churn Rate by Number of Products")
    fig10.update_layout(showlegend=False)
    st.plotly_chart(fig10, use_container_width=True)

st.markdown("---")

# ── SALARY ANALYSIS ────────────────────────────────────────────────────────────
st.subheader("💼 Salary vs Balance Churn Patterns")
c11, c12 = st.columns(2)

with c11:
    sal_data = filtered.groupby('SalaryBand', observed=True)['Exited'].mean()*100
    fig11 = px.bar(sal_data.reset_index(), x='SalaryBand', y='Exited',
                   color='SalaryBand', text_auto='.1f',
                   labels={'Exited':'Churn Rate (%)'},
                   title="Churn by Salary Band")
    fig11.update_layout(showlegend=False)
    st.plotly_chart(fig11, use_container_width=True)

with c12:
    f2 = filtered.copy()
    f2['Profile'] = 'Other'
    f2.loc[(f2['EstimatedSalary']>100000) & (f2['Balance']==0),      'Profile'] = 'High Salary, Zero Balance'
    f2.loc[(f2['EstimatedSalary']>100000) & (f2['Balance']>50000),   'Profile'] = 'High Salary, High Balance'
    f2.loc[(f2['EstimatedSalary']<50000)  & (f2['Balance']>50000),   'Profile'] = 'Low Salary, High Balance'
    combo = f2.groupby('Profile')['Exited'].mean()*100
    fig12 = px.bar(combo.reset_index(), x='Profile', y='Exited',
                   color='Profile', text_auto='.1f',
                   labels={'Exited':'Churn Rate (%)'},
                   title="Churn by Salary + Balance Profile")
    fig12.update_layout(showlegend=False, xaxis_tickangle=-20)
    st.plotly_chart(fig12, use_container_width=True)

# Revenue risk table
st.markdown("**💰 Revenue Risk — Salary Band Breakdown**")
if len(filtered[filtered['Exited']==1]) > 0:
    risk = filtered[filtered['Exited']==1].groupby('SalaryBand', observed=True).agg(
        Churned_Customers=('Exited','sum'),
        Avg_Balance=('Balance','mean'),
        Total_Balance_Lost=('Balance','sum'),
        Avg_Salary=('EstimatedSalary','mean')
    ).reset_index()
    st.dataframe(risk.style.format({
        'Avg_Balance':'€{:,.0f}',
        'Total_Balance_Lost':'€{:,.0f}',
        'Avg_Salary':'€{:,.0f}'
    }), use_container_width=True)

st.markdown("---")

# ── CHURN EXPLORER TABLE ───────────────────────────────────────────────────────
with st.expander("🔎 Segment Churn Rate Summary Table"):
    summary_rows = []
    for seg, col in [('AgeGroup','AgeGroup'),('Geography','Geography'),('Gender','Gender'),
                     ('TenureGroup','TenureGroup'),('BalanceSegment','BalanceSegment'),('CreditBand','CreditBand')]:
        g = filtered.groupby(col, observed=True)['Exited'].agg(['mean','sum','count']).reset_index()
        g.columns = [seg, 'Churn Rate', 'Churned', 'Total']
        g['Churn Rate'] = (g['Churn Rate']*100).round(2).astype(str) + '%'
        g['Dimension'] = seg
        summary_rows.append(g.rename(columns={seg:'Segment'})[['Dimension','Segment','Total','Churned','Churn Rate']])
    st.dataframe(pd.concat(summary_rows, ignore_index=True), use_container_width=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.caption("Data Source: European Bank Customer Dataset (10,000 records) | Dashboard by Expert Shubh")
st.markdown("<center>Made by <b>Expert Shubh</b> | Customer Segmentation & Churn Pattern Analytics</center>", unsafe_allow_html=True)
