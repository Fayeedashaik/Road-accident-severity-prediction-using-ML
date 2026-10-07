# ============================================================
#   Road Accident Severity Analysis — Research Dashboard
#   Layout : Top tab-based (no sidebar)
#   Theme  : Academic / Research Paper aesthetic
#   New    : Scenario Comparison engine
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AccidentSev — Research Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Google Fonts ─────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,300;0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
:root{
  --paper:#faf9f6;
  --white:#ffffff;
  --ink:#1a1a1a;
  --ink2:#3d3d3d;
  --ink3:#6b6b6b;
  --ink4:#999999;
  --rule:#d4d0c8;
  --rule2:#e8e4dc;
  --accent:#c0392b;
  --accent2:#922b21;
  --blue:#1a5276;
  --blue-l:#d6eaf8;
  --green:#1e8449;
  --green-l:#d5f5e3;
  --amber:#d4ac0d;
  --amber-l:#fef9e7;
  --serif:'Source Serif 4',Georgia,serif;
  --sans:'IBM Plex Sans',system-ui,sans-serif;
  --mono:'IBM Plex Mono',monospace;
  --shadow:0 1px 4px rgba(0,0,0,0.08);
  --shadow2:0 2px 12px rgba(0,0,0,0.1);
}

/* BASE */
.stApp{background:var(--paper)!important;font-family:var(--sans)!important;}
.stApp>header{display:none!important;}
.block-container{padding:0 2.5rem 4rem!important;max-width:1380px!important;}
#MainMenu,footer,header{visibility:hidden!important;}
.stDeployButton{display:none!important;}
section[data-testid="stSidebar"]{display:none!important;}

/* GLOBAL TEXT */
p,span,div,label{font-family:var(--sans)!important;}

/* INPUTS */
label[data-testid="stWidgetLabel"] p{
  font-family:var(--sans)!important;font-size:0.75rem!important;
  font-weight:600!important;color:var(--ink2)!important;
  text-transform:uppercase!important;letter-spacing:0.05em!important;
}
.stSelectbox>div>div{
  background:var(--white)!important;border:1.5px solid var(--rule)!important;
  color:var(--ink)!important;border-radius:4px!important;font-family:var(--sans)!important;
}
.stSelectbox [data-baseweb="select"] span{color:var(--ink)!important;}
.stTextInput input{
  background:var(--white)!important;border:1.5px solid var(--rule)!important;
  color:var(--ink)!important;border-radius:4px!important;font-family:var(--sans)!important;
}
.stSlider [data-baseweb="slider"] div[role="slider"]{
  background:var(--accent)!important;border-color:var(--accent)!important;
}
.stSlider p{color:var(--ink2)!important;}

/* BUTTON */
.stButton>button{
  background:var(--accent)!important;border:none!important;
  color:#fff!important;font-family:var(--sans)!important;
  font-size:0.82rem!important;font-weight:600!important;
  padding:0.55rem 1.5rem!important;border-radius:4px!important;
  width:100%!important;transition:all 0.15s!important;
  letter-spacing:0.03em!important;
}
.stButton>button:hover{background:var(--accent2)!important;transform:translateY(-1px)!important;}
.stButton>button p{color:#fff!important;}

/* TABS — top nav bar style */
.stTabs [data-baseweb="tab-list"]{
  background:var(--ink)!important;
  border-radius:0!important;padding:0 2rem!important;gap:0!important;
  border-bottom:none!important;margin:0 -2.5rem!important;
  position:sticky!important;top:0!important;z-index:999!important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;color:#9ca3af!important;
  font-family:var(--sans)!important;font-size:0.8rem!important;
  font-weight:500!important;letter-spacing:0.04em!important;
  text-transform:uppercase!important;
  padding:14px 22px!important;border:none!important;
  border-bottom:2px solid transparent!important;border-radius:0!important;
  transition:all 0.15s!important;
}
.stTabs [data-baseweb="tab"]:hover{color:#ffffff!important;}
.stTabs [aria-selected="true"]{
  color:#ffffff!important;
  border-bottom:2px solid var(--accent)!important;
  background:transparent!important;
}
.stTabs [data-baseweb="tab"] p{color:inherit!important;font-family:var(--sans)!important;}
.stTabs [data-baseweb="tab-panel"]{padding:2rem 0 0!important;}

/* DATAFRAME */
.stDataFrame{border:1px solid var(--rule)!important;border-radius:4px!important;}
[data-testid="stDataFrame"] th{
  background:#f5f3ef!important;color:var(--ink2)!important;
  font-family:var(--mono)!important;font-size:0.7rem!important;
  border-bottom:2px solid var(--rule)!important;
}
[data-testid="stDataFrame"] td{color:var(--ink)!important;font-size:0.78rem!important;}

/* ALERTS */
.stSuccess{background:var(--green-l)!important;border:1px solid #a9dfbf!important;border-left:4px solid var(--green)!important;border-radius:4px!important;}
.stSuccess p{color:#145a32!important;}
.stWarning{background:var(--amber-l)!important;border:1px solid #f9e79f!important;border-left:4px solid var(--amber)!important;border-radius:4px!important;}
.stWarning p{color:#7d6608!important;}
.stError{background:#fdedec!important;border:1px solid #f5b7b1!important;border-left:4px solid var(--accent)!important;border-radius:4px!important;}
.stError p{color:#922b21!important;}
.stInfo{background:var(--blue-l)!important;border:1px solid #aed6f1!important;border-left:4px solid var(--blue)!important;border-radius:4px!important;}
.stInfo p{color:#1a5276!important;}

/* EXPANDER */
.stExpander{background:var(--white)!important;border:1px solid var(--rule)!important;border-radius:4px!important;}
.stExpander summary p{color:var(--ink)!important;font-weight:600!important;}

/* SCROLLBAR */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--paper);}
::-webkit-scrollbar-thumb{background:var(--rule);border-radius:3px;}

/* ── CUSTOM COMPONENTS ─────────────────────────────────── */

/* Journal header */
.journal-header{
  background:var(--ink);color:#fff;
  padding:2.2rem 2.5rem 1.8rem;
  margin:0 -2.5rem 2rem;
  border-bottom:3px solid var(--accent);
}
.journal-vol{font-family:var(--mono);font-size:0.65rem;color:#9ca3af;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px;}
.journal-title{font-family:var(--serif);font-size:1.9rem;font-weight:700;color:#fff;line-height:1.2;margin-bottom:8px;}
.journal-title em{color:#f1948a;font-style:normal;}
.journal-meta{font-family:var(--sans);font-size:0.75rem;color:#9ca3af;display:flex;gap:24px;flex-wrap:wrap;}
.journal-meta span{display:flex;align-items:center;gap:5px;}

/* Section heading (paper section style) */
.sec-heading{
  font-family:var(--serif);font-size:1.1rem;font-weight:700;
  color:var(--ink);border-bottom:2px solid var(--ink);
  padding-bottom:6px;margin-bottom:1.2rem;
  display:flex;align-items:baseline;gap:12px;
}
.sec-num{font-family:var(--mono);font-size:0.75rem;color:var(--accent);font-weight:600;letter-spacing:0.05em;}

/* Abstract box */
.abstract-box{
  background:var(--white);border:1px solid var(--rule);
  border-left:4px solid var(--accent);
  padding:1.4rem 1.6rem;border-radius:0 4px 4px 0;
  margin-bottom:1.5rem;
}
.abstract-label{font-family:var(--mono);font-size:0.65rem;letter-spacing:0.15em;color:var(--accent);text-transform:uppercase;margin-bottom:8px;font-weight:600;}
.abstract-text{font-family:var(--serif);font-size:0.92rem;color:var(--ink2);line-height:1.8;}

/* Stat table */
.stat-table{width:100%;border-collapse:collapse;font-family:var(--sans);font-size:0.82rem;}
.stat-table th{background:#f5f3ef;color:var(--ink2);font-weight:600;padding:8px 12px;border:1px solid var(--rule);text-align:left;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.04em;}
.stat-table td{padding:8px 12px;border:1px solid var(--rule2);color:var(--ink);vertical-align:middle;}
.stat-table tr:nth-child(even) td{background:#faf8f4;}
.stat-table tr:hover td{background:#f0ece4;}

/* Finding card */
.finding{background:var(--white);border:1px solid var(--rule);border-radius:4px;padding:1rem 1.2rem;margin-bottom:0.7rem;}
.finding-num{font-family:var(--mono);font-size:0.65rem;color:var(--accent);font-weight:600;margin-bottom:4px;}
.finding-text{font-family:var(--serif);font-size:0.88rem;color:var(--ink2);line-height:1.6;}

/* Metric pill */
.metric-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:1.5rem;}
.metric-pill{background:var(--white);border:1px solid var(--rule);border-radius:4px;padding:10px 16px;text-align:center;flex:1;min-width:100px;}
.metric-pill .val{font-family:var(--mono);font-size:1.4rem;font-weight:600;color:var(--ink);}
.metric-pill .val.accent{color:var(--accent);}
.metric-pill .val.blue{color:var(--blue);}
.metric-pill .val.green{color:var(--green);}
.metric-pill .lbl{font-family:var(--sans);font-size:0.65rem;color:var(--ink4);text-transform:uppercase;letter-spacing:0.06em;margin-top:3px;}

/* Scenario comparison */
.scenario-header{
  padding:12px 16px;border-radius:4px 4px 0 0;
  font-family:var(--sans);font-size:0.82rem;font-weight:700;
  letter-spacing:0.03em;text-transform:uppercase;
  border:1px solid;border-bottom:none;
}
.scen-a{background:#1a5276;color:#fff;border-color:#1a5276;}
.scen-b{background:#6d2c0f;color:#fff;border-color:#6d2c0f;}
.scenario-body{border:1px solid var(--rule);border-radius:0 0 4px 4px;padding:1.2rem;background:var(--white);}

/* Result verdict */
.verdict{border-radius:4px;padding:1.2rem;text-align:center;border:1px solid;}
.v-minor{background:#eafaf1;border-color:#a9dfbf;}
.v-serious{background:#fefde7;border-color:#f9e79f;}
.v-fatal{background:#fdedec;border-color:#f5b7b1;}
.verdict-label{font-family:var(--serif);font-size:1.3rem;font-weight:700;}
.v-minor .verdict-label{color:#1e8449;}
.v-serious .verdict-label{color:#9a7d0a;}
.v-fatal .verdict-label{color:#c0392b;}
.verdict-conf{font-family:var(--mono);font-size:0.72rem;color:var(--ink3);margin-top:4px;}

/* Chart wrapper */
.chart-box{background:var(--white);border:1px solid var(--rule);border-radius:4px;padding:1.2rem 1.2rem 0.5rem;margin-bottom:1.2rem;}
.chart-cap{font-family:var(--serif);font-size:0.78rem;color:var(--ink3);margin-top:4px;font-style:italic;padding:0 4px 8px;}

/* Tag / badge */
.tag{display:inline-block;background:#f5f3ef;border:1px solid var(--rule);color:var(--ink2);font-family:var(--mono);font-size:0.65rem;padding:2px 8px;border-radius:2px;margin:2px;}
.tag-red{background:#fdedec;border-color:#f5b7b1;color:#922b21;}
.tag-blue{background:var(--blue-l);border-color:#aed6f1;color:#1a5276;}
.tag-green{background:var(--green-l);border-color:#a9dfbf;color:#1e8449;}

/* Footnote */
.footnote{font-family:var(--serif);font-size:0.75rem;color:var(--ink4);font-style:italic;border-top:1px solid var(--rule);padding-top:8px;margin-top:1rem;}

/* Divider */
.divider{height:1px;background:var(--rule);margin:1.5rem 0;}
</style>
""", unsafe_allow_html=True)

# ── Load Data & Model ─────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("dataset/accident_data.csv")

@st.cache_resource
def load_model():
    return (joblib.load("model/accident_model.pkl"),
            joblib.load("model/label_encoders.pkl"),
            joblib.load("model/feature_names.pkl"))

df_raw = load_data()
model, encoders, feature_names = load_model()

def clean_df():
    df = df_raw.copy()
    for c in df.select_dtypes(include=["object"]).columns:
        df[c] = df[c].fillna(df[c].mode()[0])
    df["Driver_Age"] = df["Driver_Age"].fillna(df["Driver_Age"].median())
    return df

def encode_input(inp):
    return [encoders[f].transform([inp[f]])[0] if f in encoders else inp[f] for f in feature_names]

def predict(inp):
    enc  = encode_input(inp)
    pred = model.predict(np.array(enc).reshape(1,-1))[0]
    prob = model.predict_proba(np.array(enc).reshape(1,-1))[0]
    lbl  = encoders["Accident_Severity"].inverse_transform([pred])[0]
    return lbl, prob, encoders["Accident_Severity"].classes_

df_c  = clean_df()
CMAP  = {"Fatal":"#c0392b","Serious":"#d4ac0d","Minor":"#1e8449"}
THEME = dict(
    template="simple_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Sans,sans-serif",color="#3d3d3d",size=11),
    margin=dict(l=10,r=10,t=44,b=10),
    title_font=dict(family="Source Serif 4,Georgia,serif",size=13,color="#1a1a1a"),
)

# ════════════════════════════════════════════════════════════
#  JOURNAL HEADER (always shown)
# ════════════════════════════════════════════════════════════
vc = df_c["Accident_Severity"].value_counts()
st.markdown(f"""
<div class="journal-header">
  <div class="journal-vol">Research Paper · Road Safety Analytics · v2.0 · 2025</div>
  <div class="journal-title">Road Accident <em>Severity</em> Prediction<br>Using Machine Learning</div>
  <div class="journal-meta">
    <span>📁 n = {len(df_raw):,} records</span>
    <span>🧠 Random Forest Classifier</span>
    <span>🎯 Accuracy: 71.5%</span>
    <span>📊 Features: {len(feature_names)}</span>
    <span>🏷 Classes: Minor · Serious · Fatal</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  TOP TAB NAVIGATION
# ════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "§1  Overview",
    "§2  Data Analysis",
    "§3  Visualizations",
    "§4  Prediction",
    "§5  Scenario Comparison",
])

# ════════════════════════════════════════════════════════════
#  TAB 1 — ABSTRACT & OVERVIEW
# ════════════════════════════════════════════════════════════
with tab1:
    col_main, col_side = st.columns([1.6, 1], gap="large")

    with col_main:
        st.markdown('<div class="sec-heading"><span class="sec-num">§1.1</span> Study Overview</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:1.4rem;">
          <div style="background:#fff;border:1px solid var(--rule);border-left:3px solid var(--accent);border-radius:4px;padding:1rem 1.2rem;">
            <div style="font-family:var(--mono);font-size:0.62rem;color:var(--accent);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;">Objective</div>
            <div style="font-family:var(--serif);font-size:0.88rem;color:var(--ink2);line-height:1.6;">Predict road accident severity class — <strong>Minor</strong>, <strong>Serious</strong>, or <strong>Fatal</strong> — from 7 situational features using a trained Random Forest Classifier.</div>
          </div>
          <div style="background:#fff;border:1px solid var(--rule);border-left:3px solid var(--blue);border-radius:4px;padding:1rem 1.2rem;">
            <div style="font-family:var(--mono);font-size:0.62rem;color:var(--blue);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;">Outcome</div>
            <div style="font-family:var(--serif);font-size:0.88rem;color:var(--ink2);line-height:1.6;">Achieved <strong>71.5% weighted accuracy</strong> and <strong>70.8% F1-score</strong>. Top predictors: driver age, speed limit, and light conditions.</div>
          </div>
          <div style="background:#fff;border:1px solid var(--rule);border-left:3px solid var(--green);border-radius:4px;padding:1rem 1.2rem;">
            <div style="font-family:var(--mono);font-size:0.62rem;color:var(--green);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;">Dataset</div>
            <div style="font-family:var(--serif);font-size:0.88rem;color:var(--ink2);line-height:1.6;">{len(df_raw):,} accident records · 7 input features · 3 target classes · 80/20 stratified train-test split.</div>
          </div>
          <div style="background:#fff;border:1px solid var(--rule);border-left:3px solid var(--amber);border-radius:4px;padding:1rem 1.2rem;">
            <div style="font-family:var(--mono);font-size:0.62rem;color:var(--amber);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;">Applications</div>
            <div style="font-family:var(--serif);font-size:0.88rem;color:var(--ink2);line-height:1.6;">Emergency dispatch prioritization · Road infrastructure planning · Insurance risk modeling · Navigation safety alerts.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sec-heading"><span class="sec-num">§1.2</span> Dataset Overview</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-row">
          <div class="metric-pill"><div class="val accent">2,000</div><div class="lbl">Total Records</div></div>
          <div class="metric-pill"><div class="val blue">{len(feature_names)}</div><div class="lbl">Features</div></div>
          <div class="metric-pill"><div class="val">3</div><div class="lbl">Classes</div></div>
          <div class="metric-pill"><div class="val accent">{int(df_raw.isnull().sum().sum())}</div><div class="lbl">Missing Values</div></div>
          <div class="metric-pill"><div class="val green">71.5%</div><div class="lbl">Model Accuracy</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sec-heading"><span class="sec-num">§1.3</span> Feature Descriptions</div>', unsafe_allow_html=True)
        feat_data = [
            ("Weather_Conditions","Categorical","5","Clear, Rain, Fog, Snow, Windy","Independent"),
            ("Road_Type","Categorical","5","Single/Dual Carriageway, Roundabout, One Way, Slip","Independent"),
            ("Speed_Limit","Numerical","—","20–70 mph (integer)","Independent"),
            ("Light_Conditions","Categorical","4","Daylight, Dark-lit, Dark-unlit, Dawn/Dusk","Independent"),
            ("Time_of_Day","Categorical","4","Morning, Afternoon, Evening, Night","Independent"),
            ("Number_of_Vehicles","Numerical","—","1–5 vehicles","Independent"),
            ("Driver_Age","Numerical","—","17–80 years","Independent"),
            ("Accident_Severity","Categorical","3","Minor, Serious, Fatal","Dependent (Target)"),
        ]
        rows = "".join(f"""<tr>
          <td><strong>{f}</strong></td><td>{t}</td><td>{u}</td>
          <td style="font-size:0.72rem;color:#6b6b6b;">{d}</td>
          <td><span class="tag {'tag-red' if r=='Dependent (Target)' else 'tag-blue'}">{r}</span></td>
        </tr>""" for f,t,u,d,r in feat_data)
        st.markdown(f"""
        <table class="stat-table">
          <tr><th>Feature</th><th>Type</th><th>Classes/Range</th><th>Description</th><th>Role</th></tr>
          {rows}
        </table>
        """, unsafe_allow_html=True)

        st.markdown('<div class="footnote">Table 1. Feature descriptions and types used for model training.</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§1.4</span> Methodology</div>', unsafe_allow_html=True)
        for step, title, body in [
            ("01","Data Collection & Cleaning","Synthetic dataset of 2,000 road accidents generated with realistic class distributions. ~5% missing values introduced in categorical columns, imputed using mode; numerical columns imputed with median."),
            ("02","Feature Engineering","Label encoding applied to categorical variables. No feature scaling required for tree-based models. Target encoded as: Fatal=0, Minor=1, Serious=2."),
            ("03","Model Training","Random Forest Classifier (n_estimators=200, max_depth=15, min_samples_split=5) trained on 80% stratified train split. Evaluated on 20% holdout set."),
            ("04","Evaluation Metrics","Weighted Accuracy, Precision, Recall, and F1-Score computed. Feature importances extracted and ranked."),
        ]:
            st.markdown(f"""
            <div class="finding">
              <div class="finding-num">STEP {step} — {title}</div>
              <div class="finding-text">{body}</div>
            </div>""", unsafe_allow_html=True)

    with col_side:
        st.markdown("""
    <div class="sec-heading">
        <span class="sec-num">§1.5</span> Class Distribution
    </div>
""", unsafe_allow_html=True)

        fig = px.pie(
            names=vc.index,
            values=vc.values,
            color=vc.index,
            color_discrete_map=CMAP,
            hole=0.55
        )

        fig.update_traces(
            name="",
            hovertemplate="%{label}: %{value:,} cases (%{percent})<extra></extra>"
        )

        fig.update_layout(
            **THEME,
            height=240,
            showlegend=False,
            legend_title_text="",
            title="Severity Breakdown"
        )

        fig.update_traces(
            textinfo="label+percent",
            textfont=dict(
                family="IBM Plex Sans",
                size=10
            )
        )
        
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )
        
        st.markdown("""
            <div class="chart-cap">
                Fig 1. Target class distribution across n=2,000 records.
            </div>
        """, unsafe_allow_html=True)
        

        st.markdown('<div class="sec-heading"><span class="sec-num">§1.6</span> Class Frequencies</div>', unsafe_allow_html=True)
        rows2 = "".join(f"""<tr>
          <td><span class="tag {'tag-red' if s=='Fatal' else 'tag-blue' if s=='Serious' else 'tag-green'}">{s}</span></td>
          <td style="font-family:var(--mono)">{c:,}</td>
          <td style="font-family:var(--mono)">{c/len(df_c)*100:.1f}%</td>
        </tr>""" for s,c in vc.items())
        st.markdown(f"""
        <table class="stat-table">
          <tr><th>Class</th><th>Count</th><th>Proportion</th></tr>
          {rows2}
          <tr><td><strong>Total</strong></td><td style="font-family:var(--mono)"><strong>{len(df_c):,}</strong></td><td style="font-family:var(--mono)"><strong>100%</strong></td></tr>
        </table>
        """, unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§1.7</span> Key Findings</div>', unsafe_allow_html=True)
        for i, txt in enumerate([
            "Driver age is the single most predictive feature (importance ≈ 20.8%), suggesting younger and older drivers face elevated severity risk.",
            "Speed limit accounts for ~18.2% of predictive power — higher limits strongly associate with Fatal outcomes.",
            "Fog and Snow conditions double the proportion of Serious/Fatal accidents compared to Clear weather.",
            "Night-time accidents without lighting show a 2.3× higher Fatal rate than Daylight incidents.",
            "Random Forest outperforms a single Decision Tree by ~6 percentage points in weighted F1-score.",
        ], 1):
            st.markdown(f'<div class="finding"><div class="finding-num">FINDING {i:02d}</div><div class="finding-text">{txt}</div></div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§1.8</span> Keywords</div>', unsafe_allow_html=True)
        kws = ["Road Safety","Machine Learning","Random Forest","Severity Prediction","Traffic Analytics","Classification","Feature Importance","Emergency Dispatch"]
        st.markdown("".join(f'<span class="tag">{k}</span>' for k in kws), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  TAB 2 — DATA ANALYSIS
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-heading"><span class="sec-num">§2.1</span> Raw Dataset Sample</div>', unsafe_allow_html=True)

    # Filter controls in a tight row
    fc1, fc2, fc3 = st.columns([1,1,2])
    with fc1:
        sev_filter = st.selectbox("Filter Severity", ["All","Minor","Serious","Fatal"])
    with fc2:
        wea_filter = st.selectbox("Filter Weather", ["All"]+sorted(df_raw["Weather_Conditions"].dropna().unique().tolist()))
    with fc3:
        n_rows = st.slider("Rows to display", 10, 100, 30, step=10)

    filtered = df_raw.copy()
    if sev_filter != "All": filtered = filtered[filtered["Accident_Severity"]==sev_filter]
    if wea_filter != "All": filtered = filtered[filtered["Weather_Conditions"]==wea_filter]

    st.dataframe(filtered.head(n_rows), use_container_width=True, height=280)
    st.markdown(f'<div class="footnote">Showing {min(n_rows,len(filtered)):,} of {len(filtered):,} filtered records. Total dataset: {len(df_raw):,} rows.</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown('<div class="sec-heading"><span class="sec-num">§2.2</span> Descriptive Statistics</div>', unsafe_allow_html=True)
        st.dataframe(df_c.describe().round(2), use_container_width=True, height=240)
        st.markdown('<div class="footnote">Table 2. Descriptive statistics for all numerical features.</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§2.3</span> Missing Value Analysis</div>', unsafe_allow_html=True)
        null_data = pd.DataFrame({
            "Feature": df_raw.columns,
            "Null Count": df_raw.isnull().sum().values,
            "Null %": (df_raw.isnull().mean()*100).round(2).values,
            "Strategy": ["Mode imputation" if df_raw[c].dtype=="object" else "Median imputation" if df_raw[c].isnull().any() else "—" for c in df_raw.columns]
        })
        st.dataframe(null_data, use_container_width=True, hide_index=True, height=220)
        st.markdown('<div class="footnote">Table 3. Missing value counts and imputation strategies applied.</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="sec-heading"><span class="sec-num">§2.4</span> Correlation Matrix</div>', unsafe_allow_html=True)
        df_enc = df_c.copy()
        for col in ["Weather_Conditions","Road_Type","Light_Conditions","Time_of_Day","Accident_Severity"]:
            df_enc[col] = LabelEncoder().fit_transform(df_enc[col])
        corr = df_enc.corr().round(2)

        
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.index,
            colorscale=[[0,"#1a5276"],[0.5,"#fdfcfa"],[1,"#c0392b"]],
            zmid=0, text=corr.values, texttemplate="%{text}",
            textfont={"size":8,"family":"IBM Plex Mono"},
            colorbar=dict(title="r",tickfont=dict(size=8),len=0.9,thickness=10),
            name="Feature Correlation",
            hovertemplate="X: %{x}<br>Y: %{y}<br>Correlation: %{z}<extra>Feature Correlation</extra>"
        ))
        fig.update_layout(**THEME, height=320,
                          title="Feature Correlation",
                          xaxis=dict(tickfont=dict(size=8)),
                          yaxis=dict(tickfont=dict(size=8)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="chart-cap">Fig 2. Pearson correlation matrix. Speed_Limit and Light_Conditions show strongest correlation with target.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-heading"><span class="sec-num">§2.5</span> Categorical Frequency Table</div>', unsafe_allow_html=True)
        cat_sel = st.selectbox("Select variable", ["Weather_Conditions","Road_Type","Light_Conditions","Time_of_Day","Accident_Severity"], key="cat_sel")
        freq = df_raw[cat_sel].value_counts().reset_index()
        freq.columns = ["Category","Count"]
        freq["Proportion"] = (freq["Count"]/len(df_raw)*100).round(1).astype(str) + "%"
        st.dataframe(freq, use_container_width=True, hide_index=True, height=180)

# ════════════════════════════════════════════════════════════
#  TAB 3 — VISUALIZATIONS
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-heading"><span class="sec-num">§3</span> Exploratory Visualizations</div>', unsafe_allow_html=True)

    # Fig 3+4 row
    v1, v2 = st.columns(2, gap="medium")
    with v1:
        
        ws = df_c.groupby(["Weather_Conditions","Accident_Severity"]).size().reset_index(name="n")
        fig = px.bar(ws, x="Weather_Conditions", y="n", color="Accident_Severity",
                     barmode="group", color_discrete_map=CMAP,
                     labels={"n":"Frequency","Weather_Conditions":"Weather"})
        fig.update_layout(**THEME, height=290,
                          title="Fig 3. Accident Frequency by Weather × Severity",
                          legend=dict(orientation="h",y=1.12,font=dict(size=10)),
                          xaxis_tickfont=dict(size=9))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="chart-cap">Fog and Snow show disproportionately higher Serious/Fatal rates.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with v2:
        
        rs = df_c.groupby(["Road_Type","Accident_Severity"]).size().reset_index(name="n")
        fig = px.bar(rs, x="Road_Type", y="n", color="Accident_Severity",
                     barmode="stack", color_discrete_map=CMAP,
                     labels={"n":"Frequency","Road_Type":"Road Type"})
        fig.update_layout(**THEME, height=290,
                          title="Fig 4. Severity by Road Type (Stacked)",
                          legend=dict(orientation="h",y=1.12,font=dict(size=10)),
                          xaxis=dict(tickangle=-15,tickfont=dict(size=9)))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="chart-cap">Single Carriageways account for the largest total accident volume.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Fig 5+6 row
    v3, v4 = st.columns(2, gap="medium")
    with v3:
        
        order = ["Morning","Afternoon","Evening","Night"]
        tod = df_c.groupby(["Time_of_Day","Accident_Severity"]).size().reset_index(name="n")
        tod["Time_of_Day"] = pd.Categorical(tod["Time_of_Day"],categories=order,ordered=True)
        tod = tod.sort_values("Time_of_Day")
        fig = px.line(tod, x="Time_of_Day", y="n", color="Accident_Severity",
                      markers=True, color_discrete_map=CMAP,
                      labels={"n":"Frequency"})
        fig.update_layout(**THEME, height=270,
                          title="Fig 5. Severity Trend Across Time of Day",
                          legend=dict(orientation="h",y=1.12,font=dict(size=10)))
        fig.update_traces(line_width=2, marker_size=7)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="chart-cap">Night-time shows elevated Fatal accident rates relative to Afternoon.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with v4:
        
        fig = px.violin(df_c, x="Accident_Severity", y="Speed_Limit",
                        color="Accident_Severity", box=True, points="outliers",
                        color_discrete_map=CMAP,
                        labels={"Speed_Limit":"Speed Limit (mph)"})
        fig.update_layout(**THEME, height=270,
                          title="Fig 6. Speed Limit Distribution by Severity",
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="chart-cap">Fatal accidents concentrate at higher speed limits (60–70 mph).</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Fig 7 — Driver age histogram full width
    
    fig = px.histogram(df_c, x="Driver_Age", color="Accident_Severity",
                       color_discrete_map=CMAP, barmode="overlay",
                       nbins=35, opacity=0.72,
                       labels={"Driver_Age":"Driver Age (years)","count":"Frequency"})
    fig.update_layout(**THEME, height=250,
                      title="Fig 7. Driver Age Distribution by Accident Severity",
                      legend=dict(orientation="h",y=1.1,font=dict(size=11)))
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="chart-cap">Drivers aged 17–25 and 65+ show elevated Fatal severity proportions — consistent with known road safety risk profiles.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  TAB 4 — PREDICTION
# ════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-heading"><span class="sec-num">§4</span> Accident Severity Prediction</div>', unsafe_allow_html=True)

    p_left, p_right = st.columns([1, 1.2], gap="large")

    with p_left:
        # Input form
        st.markdown('<div class="sec-heading"><span class="sec-num">§4.1</span> Incident Parameters</div>', unsafe_allow_html=True)
        

        p_weather = st.selectbox("Weather Conditions", ["Clear","Rain","Fog","Snow","Windy"], key="p_w")
        p_road    = st.selectbox("Road Type", ["Single Carriageway","Dual Carriageway","Roundabout","One Way","Slip Road"], key="p_r")
        p_light   = st.selectbox("Light Conditions", ["Daylight","Darkness - lights lit","Darkness - no lighting","Dawn/Dusk"], key="p_l")
        p_time    = st.selectbox("Time of Day", ["Morning","Afternoon","Evening","Night"], key="p_t")

        pc1, pc2 = st.columns(2)
        with pc1:
            p_speed = st.slider("Speed Limit (mph)", 20, 70, 40, step=10, key="p_sp")
        with pc2:
            p_veh   = st.slider("No. of Vehicles", 1, 5, 2, key="p_v")

        p_age = st.slider("Driver Age (years)", 17, 80, 35, key="p_a")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1rem;"></div>', unsafe_allow_html=True)
        predict_btn = st.button("▶  Run Prediction Engine")

        # Model spec reference card
        st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§4.2</span> Model Reference</div>', unsafe_allow_html=True)
        spec_rows = "".join(f"<tr><td style='color:var(--ink3);font-size:0.8rem;'>{k}</td><td style='font-family:var(--mono);font-size:0.78rem;font-weight:600;color:var(--ink);'>{v}</td></tr>" for k,v in [
            ("Algorithm","Random Forest Classifier"),
            ("Trees / Depth","200 estimators · max depth 15"),
            ("Training Split","80% train · 20% test (stratified)"),
            ("Weighted Accuracy","71.5%"),
            ("Weighted F1","70.8%"),
            ("Features Used","7 input variables"),
        ])
        st.markdown(f'<table class="stat-table" style="font-size:0.8rem;"><tr><th>Spec</th><th>Value</th></tr>{spec_rows}</table>', unsafe_allow_html=True)

        # Severity legend
        st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§4.3</span> Severity Reference</div>', unsafe_allow_html=True)
        for sev, col, desc in [
            ("MINOR",   "#1e8449", "Slight injuries. Standard emergency response. No escalation needed."),
            ("SERIOUS", "#d4ac0d", "Severe injuries. Priority dispatch. Alert nearby hospitals."),
            ("FATAL",   "#c0392b", "Life-threatening. Full trauma response. Immediate deployment."),
        ]:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid var(--rule2);">
              <div style="width:10px;height:10px;border-radius:50%;background:{col};margin-top:4px;flex-shrink:0;"></div>
              <div>
                <div style="font-family:var(--mono);font-size:0.72rem;font-weight:700;color:{col};letter-spacing:0.06em;">{sev}</div>
                <div style="font-family:var(--serif);font-size:0.8rem;color:var(--ink3);margin-top:2px;">{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    with p_right:
        st.markdown('<div class="sec-heading"><span class="sec-num">§4.4</span> Prediction Result</div>', unsafe_allow_html=True)

        if predict_btn:
            p_inp = {
                "Weather_Conditions": p_weather, "Road_Type": p_road,
                "Speed_Limit": p_speed, "Light_Conditions": p_light,
                "Time_of_Day": p_time, "Number_of_Vehicles": p_veh, "Driver_Age": p_age
            }
            p_lbl, p_prob, p_classes = predict(p_inp)
            p_conf  = max(p_prob) * 100
            p_col   = {"Minor":"#1e8449","Serious":"#d4ac0d","Fatal":"#c0392b"}[p_lbl]
            p_emoji = {"Minor":"🟢","Serious":"🟡","Fatal":"🔴"}[p_lbl]
            p_bg    = {"Minor":"#eafaf1","Serious":"#fefde7","Fatal":"#fdedec"}[p_lbl]
            p_border= {"Minor":"#a9dfbf","Serious":"#f9e79f","Fatal":"#f5b7b1"}[p_lbl]

            # Big verdict card
            st.markdown(f"""
            <div style="background:{p_bg};border:2px solid {p_border};border-radius:6px;padding:2rem;text-align:center;margin-bottom:1.2rem;">
              <div style="font-size:3.5rem;margin-bottom:8px;">{p_emoji}</div>
              <div style="font-family:var(--serif);font-size:2rem;font-weight:700;color:{p_col};letter-spacing:0.02em;">{p_lbl.upper()}</div>
              <div style="font-family:var(--mono);font-size:0.75rem;color:var(--ink3);margin-top:6px;">Model Confidence: {p_conf:.1f}%</div>
              <div style="height:6px;background:rgba(0,0,0,0.08);border-radius:3px;margin:12px auto 0;max-width:200px;">
                <div style="height:100%;width:{p_conf:.0f}%;background:{p_col};border-radius:3px;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

            # Probability chart
            st.markdown('<div class="sec-heading"><span class="sec-num">§4.5</span> Class Probability Breakdown</div>', unsafe_allow_html=True)
           
            bar_cols = [CMAP.get(c,"#999") for c in p_classes]
            fig = go.Figure(go.Bar(
                x=p_classes, y=p_prob*100,
                marker_color=bar_cols, marker_line_width=0,
                text=[f"{v*100:.1f}%" for v in p_prob],
                textposition="outside",
                textfont=dict(family="IBM Plex Mono", size=11, color="#1a1a1a")
            ))
            fig.update_layout(**THEME, height=260,
                              title="Fig 9. Posterior Class Probabilities — Random Forest",
                              yaxis=dict(title="Probability (%)", range=[0, 115], tickfont=dict(size=9)),
                              xaxis=dict(title="Severity Class", tickfont=dict(family="IBM Plex Mono", size=11)))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('<div class="chart-cap">Fig 9. Probability estimates from 200-tree Random Forest vote aggregation.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Input summary table
            st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-heading"><span class="sec-num">§4.6</span> Input Parameter Summary</div>', unsafe_allow_html=True)
            input_rows = "".join(f"<tr><td style='color:var(--ink2);'>{k.replace('_',' ')}</td><td style='font-family:var(--mono);font-weight:600;'>{v}</td></tr>" for k,v in p_inp.items())
            st.markdown(f"""
            <table class="stat-table">
              <tr><th>Parameter</th><th>Value Entered</th></tr>
              {input_rows}
              <tr style="background:#faf8f4;font-weight:700;">
                <td>Predicted Severity</td>
                <td style="font-family:var(--mono);color:{p_col};font-weight:700;">{p_lbl.upper()} ({p_conf:.1f}% confidence)</td>
              </tr>
            </table>""", unsafe_allow_html=True)
            st.markdown('<div class="footnote">Table 7. Input parameters submitted for this prediction run.</div>', unsafe_allow_html=True)

            # Alert
            st.markdown('<div style="margin-top:1rem;"></div>', unsafe_allow_html=True)
            if p_lbl == "Minor":
                st.success("**Low Risk** — Standard emergency response protocols apply. No immediate escalation required.")
            elif p_lbl == "Serious":
                st.warning("**Elevated Risk** — Priority medical dispatch recommended. Alert nearby hospitals and trauma units.")
            else:
                st.error("**Critical Risk** — Full trauma response required. Immediate emergency services deployment activated.")

        else:
            # Placeholder state
            st.markdown("""
            <div style="background:#fff;border:2px dashed var(--rule);border-radius:6px;padding:3rem;text-align:center;">
              <div style="font-size:2.5rem;margin-bottom:12px;">🔬</div>
              <div style="font-family:var(--serif);font-size:1.1rem;color:var(--ink2);margin-bottom:6px;">Awaiting Input Parameters</div>
              <div style="font-family:var(--sans);font-size:0.82rem;color:var(--ink4);">Fill in the incident parameters on the left<br>and click <strong>Run Prediction Engine</strong> to get results.</div>
            </div>

            <div style="margin-top:1.5rem;">
              <div class="sec-heading"><span class="sec-num">§4.5</span> Feature Importance Reference</div>
            </div>""", unsafe_allow_html=True)

            imp = pd.DataFrame({"Feature":feature_names,"Importance":model.feature_importances_}).sort_values("Importance")
            imp_s = imp.sort_values("Importance", ascending=False).reset_index(drop=True)
            imp_s["Pct"] = (imp_s["Importance"]*100).round(1)
            max_i = imp_s["Importance"].max()
            rows_fi = ""
            for i, row in imp_s.iterrows():
                bw = int(row["Importance"]/max_i*100)
                rows_fi += f"""<tr>
                  <td style="font-family:var(--mono);color:var(--ink3);text-align:center;font-size:0.75rem;">#{i+1}</td>
                  <td style="font-family:var(--mono);font-size:0.78rem;">{row['Feature']}</td>
                  <td><div style="display:flex;align-items:center;gap:6px;">
                    <div style="flex:1;height:5px;background:#f0ece4;border-radius:3px;">
                      <div style="height:100%;width:{bw}%;background:#1a5276;border-radius:3px;"></div>
                    </div>
                    <span style="font-family:var(--mono);font-size:0.7rem;color:var(--ink);min-width:34px;">{row['Pct']}%</span>
                  </div></td>
                </tr>"""
            st.markdown(f"""
            <table class="stat-table">
              <tr><th style="text-align:center;">#</th><th>Feature</th><th>Importance</th></tr>
              {rows_fi}
            </table>
            <div class="footnote">Table 6. Feature importance scores — higher = stronger predictor of severity.</div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  TAB 5 — SCENARIO COMPARISON
# ════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-heading"><span class="sec-num">§5</span> Scenario Comparison Engine</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="abstract-box" style="margin-bottom:1.5rem;">
      <div class="abstract-label">About This Tool</div>
      <div class="abstract-text">
        Configure two distinct accident scenarios below and run them simultaneously through the
        trained Random Forest model. The engine computes class probabilities for each scenario
        and renders a side-by-side comparison — useful for understanding how changing a single
        variable (e.g. weather, speed, lighting) alters predicted severity.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Input forms ──────────────────────────────────────────
    s_a, gap_col, s_b = st.columns([1, 0.06, 1])

    with s_a:
        st.markdown('<div class="scenario-header scen-a">⬡ Scenario A</div>', unsafe_allow_html=True)
        
        a_weather = st.selectbox("Weather", ["Clear","Rain","Fog","Snow","Windy"], key="a_w")
        a_road    = st.selectbox("Road Type", ["Single Carriageway","Dual Carriageway","Roundabout","One Way","Slip Road"], key="a_r")
        a_speed   = st.slider("Speed Limit (mph)", 20, 70, 30, step=10, key="a_sp")
        a_light   = st.selectbox("Light Conditions", ["Daylight","Darkness - lights lit","Darkness - no lighting","Dawn/Dusk"], key="a_l")
        a_time    = st.selectbox("Time of Day", ["Morning","Afternoon","Evening","Night"], key="a_t")
        a_veh     = st.slider("Vehicles", 1, 5, 1, key="a_v")
        a_age     = st.slider("Driver Age", 17, 80, 28, key="a_a")
        st.markdown('</div>', unsafe_allow_html=True)

    with gap_col:
        st.markdown('<div style="height:100%;display:flex;align-items:center;justify-content:center;padding-top:80px;"><div style="font-family:var(--serif);font-size:1.4rem;color:var(--rule);font-weight:700;">VS</div></div>', unsafe_allow_html=True)

    with s_b:
        st.markdown('<div class="scenario-header scen-b">⬡ Scenario B</div>', unsafe_allow_html=True)
        
        b_weather = st.selectbox("Weather", ["Clear","Rain","Fog","Snow","Windy"], index=1, key="b_w")
        b_road    = st.selectbox("Road Type", ["Single Carriageway","Dual Carriageway","Roundabout","One Way","Slip Road"], key="b_r")
        b_speed   = st.slider("Speed Limit (mph)", 20, 70, 70, step=10, key="b_sp")
        b_light   = st.selectbox("Light Conditions", ["Daylight","Darkness - lights lit","Darkness - no lighting","Dawn/Dusk"], index=2, key="b_l")
        b_time    = st.selectbox("Time of Day", ["Morning","Afternoon","Evening","Night"], index=3, key="b_t")
        b_veh     = st.slider("Vehicles", 1, 5, 4, key="b_v")
        b_age     = st.slider("Driver Age", 17, 80, 72, key="b_a")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
    run_btn = st.button("⬡  Run Comparative Analysis")

    if run_btn:
        inp_a = {"Weather_Conditions":a_weather,"Road_Type":a_road,"Speed_Limit":a_speed,
                 "Light_Conditions":a_light,"Time_of_Day":a_time,"Number_of_Vehicles":a_veh,"Driver_Age":a_age}
        inp_b = {"Weather_Conditions":b_weather,"Road_Type":b_road,"Speed_Limit":b_speed,
                 "Light_Conditions":b_light,"Time_of_Day":b_time,"Number_of_Vehicles":b_veh,"Driver_Age":b_age}

        lbl_a, prob_a, classes = predict(inp_a)
        lbl_b, prob_b, _       = predict(inp_b)

        st.markdown('<div style="margin-top:1.8rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§5.1</span> Prediction Verdicts</div>', unsafe_allow_html=True)

        v1, vgap, v2 = st.columns([1, 0.06, 1])
        for col, lbl, prob, tag in [(v1, lbl_a, prob_a, "A"), (v2, lbl_b, prob_b, "B")]:
            conf = max(prob)*100
            cls  = lbl.lower()
            emoji= {"Minor":"🟢","Serious":"🟡","Fatal":"🔴"}[lbl]
            with col:
                st.markdown(f"""
                <div class="verdict v-{cls}">
                  <div style="font-family:var(--mono);font-size:0.65rem;color:var(--ink4);margin-bottom:6px;">SCENARIO {tag}</div>
                  <div style="font-size:2rem;margin-bottom:4px;">{emoji}</div>
                  <div class="verdict-label">{lbl.upper()}</div>
                  <div class="verdict-conf">Confidence: {conf:.1f}% · Model: Random Forest</div>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§5.2</span> Probability Distribution Comparison</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        fig = go.Figure()
        bar_colors = [CMAP.get(c,"#999") for c in classes]

        fig.add_trace(go.Bar(
            name="Scenario A", x=classes, y=prob_a*100,
            marker_color=["rgba(26,82,118,0.85)"]*3,
            marker_line_width=0, text=[f"{p*100:.1f}%" for p in prob_a],
            textposition="outside", textfont=dict(family="IBM Plex Mono",size=10)
        ))
        fig.add_trace(go.Bar(
            name="Scenario B", x=classes, y=prob_b*100,
            marker_color=["rgba(109,44,15,0.85)"]*3,
            marker_line_width=0, text=[f"{p*100:.1f}%" for p in prob_b],
            textposition="outside", textfont=dict(family="IBM Plex Mono",size=10)
        ))
        fig.update_layout(**THEME, barmode="group", height=300,
                          title="Fig 9. Class Probability Comparison — Scenario A vs B",
                          yaxis=dict(title="Probability (%)",range=[0,115]),
                          xaxis=dict(title="Severity Class"),
                          legend=dict(orientation="h",y=1.1,font=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="chart-cap">Side-by-side class probabilities from the Random Forest classifier for both scenarios.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Delta table
        st.markdown('<div class="sec-heading"><span class="sec-num">§5.3</span> Parameter Difference Table</div>', unsafe_allow_html=True)
        diff_rows = ""
        for k in inp_a:
            va, vb = inp_a[k], inp_b[k]
            changed = "✦" if va != vb else "—"
            style = "background:#fef9e7;" if va != vb else ""
            diff_rows += f"<tr style='{style}'><td>{k.replace('_',' ')}</td><td style='font-family:var(--mono)'>{va}</td><td style='font-family:var(--mono)'>{vb}</td><td style='text-align:center;color:var(--accent);font-weight:700;'>{changed}</td></tr>"
        st.markdown(f"""
        <table class="stat-table">
          <tr><th>Parameter</th><th>Scenario A</th><th>Scenario B</th><th>Changed?</th></tr>
          {diff_rows}
          <tr style="background:#f0ece4;font-weight:700;">
            <td>Predicted Severity</td>
            <td><span class="tag {'tag-red' if lbl_a=='Fatal' else 'tag-blue' if lbl_a=='Serious' else 'tag-green'}">{lbl_a}</span></td>
            <td><span class="tag {'tag-red' if lbl_b=='Fatal' else 'tag-blue' if lbl_b=='Serious' else 'tag-green'}">{lbl_b}</span></td>
            <td style="text-align:center;">{'✦' if lbl_a!=lbl_b else '—'}</td>
          </tr>
        </table>""", unsafe_allow_html=True)
        st.markdown('<div class="footnote">Table 7. Parameter comparison. ✦ denotes changed values between Scenario A and B.</div>', unsafe_allow_html=True)

        # Risk interpretation
        st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-heading"><span class="sec-num">§5.4</span> Risk Interpretation</div>', unsafe_allow_html=True)
        for tag, lbl, prob in [("A", lbl_a, prob_a), ("B", lbl_b, prob_b)]:
            conf = max(prob)*100
            if lbl=="Minor":
                st.success(f"**Scenario {tag} — {lbl}** ({conf:.1f}% confidence): Low-severity incident. Standard emergency response protocols apply. No immediate escalation required.")
            elif lbl=="Serious":
                st.warning(f"**Scenario {tag} — {lbl}** ({conf:.1f}% confidence): Elevated-severity incident. Priority medical dispatch recommended. Alert nearby trauma centers.")
            else:
                st.error(f"**Scenario {tag} — {lbl}** ({conf:.1f}% confidence): Critical-severity incident. Full emergency services deployment required immediately. Trauma response activated.")