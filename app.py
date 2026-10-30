import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
import io
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="FAIRSHIFT | Smart Allocation",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. BACKGROUND IMAGE
# ==========================================

def get_background():
    try:
        with open("background.png", "rb") as file:
            encoded = base64.b64encode(file.read()).decode()
        return f"""
        <style>
        .stApp {{
            background-image:
            linear-gradient(rgba(2,10,29,0.76),
                            rgba(2,10,29,0.84)),
            url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
    except FileNotFoundError:
        return """
        <style>
        .stApp {
            background: linear-gradient(135deg,#020817,#05264b,#00152d);
        }
        </style>
        """

st.markdown(get_background(), unsafe_allow_html=True)

# ==========================================
# 3. CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

html, body, [class*="css"] {
    color: #EAF6FF !important;
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    color: #EAF6FF;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3, h4, p, label {
    color: #EAF6FF !important;
}

.hero {
    background: linear-gradient(
        110deg,
        rgba(0,48,95,0.92),
        rgba(1,15,43,0.91)
    );
    border: 1px solid #087DCE;
    border-radius: 22px;
    padding: 35px;
    margin: 20px 0;
    box-shadow: 0 0 25px rgba(0,180,255,0.15);
}

.hero h1 {
    font-size: 55px;
    font-weight: 900;
    letter-spacing: 3px;
}

.cyan {
    color: #00D9FF;
}

.hero p {
    font-size: 17px;
    color: #B8DDF7 !important;
}

.glass {
    background: rgba(3,28,62,0.88);
    border: 1px solid #087DCE;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0 0 15px rgba(0,180,255,0.12);
}

.metric-title {
    color: #B6DFFF;
    font-size: 14px;
}

.metric-value {
    font-size: 29px;
    font-weight: bold;
    color: #00D9FF;
}

.stButton > button {
    background: linear-gradient(90deg,#0077FF,#00D9FF);
    color: white !important;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    min-height: 43px;
    transition: 0.3s;
}

.stButton > button:hover {
    box-shadow: 0 0 20px #00BFFF;
    transform: translateY(-2px);
}

.stDownloadButton > button {
    background: #063C67;
    color: white;
    border: 1px solid #00BFFF;
    border-radius: 10px;
}

[data-testid="stFileUploader"] {
    background: rgba(0,60,110,0.55);
    border: 2px dashed #00CFFF;
    border-radius: 17px;
    padding: 20px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #087DCE;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    color: #C7E9FF;
    font-weight: bold;
}

.stTabs [aria-selected="true"] {
    color: #00D9FF !important;
}

div[data-testid="stMetric"] {
    background: rgba(0,45,85,0.82);
    border: 1px solid #087DCE;
    border-radius: 14px;
    padding: 16px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. SESSION STATE
# ==========================================

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "filename" not in st.session_state:
    st.session_state.filename = ""

if "audit" not in st.session_state:
    st.session_state.audit = []

# ==========================================
# 5. HEADER
# ==========================================

header1, header2 = st.columns([2, 1])

with header1:
    st.markdown("""
    <h2 style='color:#00D9FF !important;'>
    🧠 FAIRSHIFT
    </h2>
    <p style='color:#9DDFFF !important;'>
    AI-POWERED SMART ALLOCATION ENGINE
    </p>
    """, unsafe_allow_html=True)

with header2:
    st.markdown("""
    <p style='text-align:right;color:#00D9FF !important;'>
    ⚡ SMART &nbsp; • &nbsp; FAIR &nbsp; • &nbsp; TRANSPARENT
    </p>
    """, unsafe_allow_html=True)

# ==========================================
# 6. HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">

<h1>
FAIR<span class="cyan">SHIFT</span>
</h1>

<h2>AI-Powered Smart Allocation Engine</h2>

<p>
Upload your dataset, configure your criteria and get
intelligent, transparent and explainable allocation recommendations.
</p>

<p>
🏆 Smart Scoring &nbsp;&nbsp;
🛡️ Fairness Audit &nbsp;&nbsp;
📊 Advanced Analytics &nbsp;&nbsp;
🔍 Explainable Decisions
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. NAVIGATION
# ==========================================

home, demo, analytics, audit = st.tabs([
    "🏠 Home",
    "⚡ AI Demo",
    "📊 Analytics",
    "🛡️ Fairness & Audit"
])

# ==========================================
# 8. HOME - FILE UPLOAD
# ==========================================

with home:

    st.markdown("## 📂 Upload Your Dataset")

    st.markdown("""
    <p style='color:#A8DFFF !important;'>
    Upload CSV or Excel data to begin smart allocation.
    </p>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 3, 1])

    with center:

        uploaded_file = st.file_uploader(
            "Choose your dataset",
            type=["csv", "xlsx", "xls"],
            help="Maximum supported size is 200 MB."
        )

        if uploaded_file:

            try:
                if uploaded_file.name.endswith(".csv"):
                    try:
                        df = pd.read_csv(uploaded_file)
                    except UnicodeDecodeError:
                        uploaded_file.seek(0)
                        df = pd.read_csv(
                            uploaded_file,
                            encoding="latin1"
                        )

                else:
                    df = pd.read_excel(uploaded_file)

                if df.empty:
                    st.error("Your uploaded file is empty.")

                elif len(df.columns) == 0:
                    st.error("No columns found.")

                else:
                    st.session_state.dataset = df
                    st.session_state.filename = uploaded_file.name

                    st.success(
                        f"Successfully uploaded: {uploaded_file.name}"
                    )

            except Exception as e:
                st.error(f"File reading error: {e}")

    if st.session_state.dataset is not None:

        df = st.session_state.dataset

        st.markdown("---")
        st.markdown("### 📋 Dataset Preview")

        st.caption(
            f"File: {st.session_state.filename}"
        )

        st.dataframe(
            df.head(15),
            width="stretch"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Records", len(df))
        c2.metric("Total Columns", len(df.columns))
        c3.metric(
            "Missing Values",
            int(df.isna().sum().sum())
        )

        st.info(
            "Next: Open the AI Demo tab and configure your allocation criteria."
        )

    else:
        st.markdown("""
        <div class="glass" style="text-align:center;padding:35px;">

        <h1 style="font-size:55px;">☁️</h1>

        <h2>Upload Your Dataset</h2>

        <p style="color:#A8DFFF !important;">
        CSV • XLSX • XLS
        </p>

        <p style="color:#A8DFFF !important;">
        Your data is processed locally by this application.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🚀 Platform Features")

    f1, f2, f3, f4, f5 = st.columns(5)

    features = [
        ("🧠", "Smart Scoring"),
        ("🛡️", "Fairness Audit"),
        ("📊", "Analytics"),
        ("🔍", "Explainable AI"),
        ("📜", "Audit Trail")
    ]

    for col, (icon, name) in zip(
        [f1, f2, f3, f4, f5], features
    ):
        with col:
            st.markdown(f"""
            <div class="glass" style="text-align:center;">
            <h2>{icon}</h2>
            <b>{name}</b>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# 9. AI DEMO - CONFIGURATION
# ==========================================

result_df = None

with demo:

    st.markdown("## ⚡ AI Allocation Engine")

    if st.session_state.dataset is None:

        st.warning("Please upload a dataset in the Home tab first.")

    else:

        df = st.session_state.dataset.copy()

        # Find numeric columns
        numeric_cols = df.select_dtypes(
            include=np.number
        ).columns.tolist()

        # Remove likely identifiers
        excluded_words = [
            "id", "phone", "mobile", "roll",
            "index", "serial", "code"
        ]

        numeric_cols = [
            c for c in numeric_cols
            if not any(
                word in str(c).lower()
                for word in excluded_words
            )
        ]

        if not numeric_cols:

            st.error(
                "No suitable numeric columns found. "
                "Your dataset needs numerical criteria."
            )

        else:

            st.markdown("### 🎯 Step 1: Select Criteria")

            selected = st.multiselect(
                "Choose the numerical criteria for scoring",
                options=numeric_cols,
                default=numeric_cols[:min(3, len(numeric_cols))]
            )

            st.markdown("### ⚖️ Step 2: Configure Weights")

            weights = {}
            directions = {}

            if selected:

                st.caption(
                    "Set importance and whether higher or lower values are better."
                )

                for col in selected:

                    with st.expander(
                        f"⚙️ {col}",
                        expanded=True
                    ):

                        a, b = st.columns(2)

                        with a:
                            weights[col] = st.slider(
                                f"Weight for {col}",
                                min_value=0,
                                max_value=100,
                                value=50,
                                key=f"weight_{col}"
                            )

                        with b:
                            directions[col] = st.selectbox(
                                f"Preference for {col}",
                                [
                                    "Higher is better",
                                    "Lower is better"
                                ],
                                key=f"direction_{col}"
                            )

                total_weight = sum(weights.values())

                st.info(
                    f"Total selected weight: {total_weight}"
                )

                st.markdown("### 👥 Step 3: Allocation Settings")

                col1, col2 = st.columns(2)

                with col1:

                    max_slots = st.number_input(
                        "Number of available opportunities",
                        min_value=1,
                        max_value=len(df),
                        value=min(5, len(df)),
                        step=1
                    )

                with col2:

                    name_candidates = [
                        c for c in df.columns
                        if any(
                            x in str(c).lower()
                            for x in ["name", "student", "applicant"]
                        )
                    ]

                    name_col = st.selectbox(
                        "Applicant name column",
                        ["None"] + list(df.columns),
                        index=(
                            list(df.columns).index(name_candidates[0]) + 1
                            if name_candidates else 0
                        )
                    )

                category_candidates = [
                    c for c in df.columns
                    if not pd.api.types.is_numeric_dtype(df[c])
                    and c != name_col
                ]

                group_col = st.selectbox(
                    "Category / Group column (for fairness audit)",
                    ["None"] + category_candidates
                )

                st.markdown("---")

                if st.button(
                    "🚀 GENERATE ALLOCATION RESULTS",
                    use_container_width=True
                ):

                    if not selected:
                        st.error("Please select at least one criterion.")

                    elif total_weight <= 0:
                        st.error("At least one weight must be greater than zero.")

                    else:

                        # ==================================
                        # 10. SCORING ENGINE
                        # ==================================

                        scores = pd.Series(
                            0.0,
                            index=df.index
                        )

                        explanations = []

                        contributions = {}

                        for col in selected:

                            values = pd.to_numeric(
                                df[col],
                                errors="coerce"
                            )

                            values = values.replace(
                                [np.inf, -np.inf],
                                np.nan
                            )

                            median = values.median()

                            if pd.isna(median):
                                median = 0

                            values = values.fillna(median)

                            minimum = values.min()
                            maximum = values.max()

                            if maximum == minimum:

                                normalized = pd.Series(
                                    100.0,
                                    index=df.index
                                )

                            else:

                                normalized = (
                                    (values - minimum)
                                    / (maximum - minimum)
                                ) * 100

                            if directions[col] == "Lower is better":

                                normalized = 100 - normalized

                            normalized = normalized.fillna(0)

                            contribution = (
                                normalized
                                * weights[col]
                                / total_weight
                            )

                            scores += contribution

                            contributions[col] = contribution

                        # ==================================
                        # 11. RANKING
                        # ==================================

                        result_df = df.copy()

                        result_df["FAIRSHIFT_Score"] = (
                            scores.round(2)
                        )

                        result_df = result_df.sort_values(
                            "FAIRSHIFT_Score",
                            ascending=False
                        ).reset_index(drop=True)

                        result_df["Rank"] = (
                            np.arange(len(result_df)) + 1
                        )

                        result_df["Decision"] = np.where(
                            result_df["Rank"] <= max_slots,
                            "Recommended",
                            "Not Recommended"
                        )

                        # ==================================
                        # 12. EXPLANATION
                        # ==================================

                        reasons = []

                        for original_index in result_df.index:

                            # Scores are matched using the original
                            # DataFrame row index.
                            pass

                        original_indices = (
                            df.index.tolist()
                        )

                        for _, row in result_df.iterrows():

                            original_idx = original_indices[
                                int(row["Rank"]) - 1
                            ] if False else None

                            # Recover the row using its unique index
                            # stored temporarily below.
                            pass

                        # Create explanations using sorted row indexes
                        sorted_indices = (
                            scores.sort_values(
                                ascending=False
                            ).index.tolist()
                        )

                        for idx in sorted_indices:

                            ranked_features = sorted(
                                selected,
                                key=lambda x: contributions[x].loc[idx],
                                reverse=True
                            )

                            top_features = ranked_features[:3]

                            reasons.append(
                                ", ".join([
                                    f"{col}: {contributions[col].loc[idx]:.1f} points"
                                    for col in top_features
                                ])
                            )

                        result_df["Decision_Explanation"] = reasons

                        # ==================================
                        # 13. STORE RESULTS
                        # ==================================

                        st.session_state.results = result_df

                        st.session_state.criteria = selected

                        st.session_state.group_col = group_col

                        st.session_state.max_slots = max_slots

                        st.session_state.contributions = contributions

                        st.session_state.audit.append({
                            "Time": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "File": st.session_state.filename,
                            "Records": len(df),
                            "Selected Criteria": ", ".join(selected),
                            "Available Slots": max_slots
                        })

                        st.success(
                            "Allocation generated successfully!"
                        )

                        st.rerun()

# ==========================================
# 14. DISPLAY RESULTS
# ==========================================

if "results" in st.session_state:

    result_df = st.session_state.results

    st.markdown("---")

    st.markdown("## 🏆 Allocation Results")

    m1, m2, m3, m4 = st.columns(4)

    recommended = result_df[
        result_df["Decision"] == "Recommended"
    ]

    m1.metric(
        "Total Applicants",
        len(result_df)
    )

    m2.metric(
        "Recommended",
        len(recommended)
    )

    m3.metric(
        "Average Score",
        f"{result_df['FAIRSHIFT_Score'].mean():.2f}"
    )

    m4.metric(
        "Available Slots",
        st.session_state.max_slots
    )

    st.markdown("### 📋 Student Ranking")

    st.dataframe(
        result_df,
        width="stretch",
        hide_index=True
    )

    csv_data = result_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Results CSV",
        csv_data,
        file_name="FAIRSHIFT_Results.csv",
        mime="text/csv"
    )

    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        result_df.to_excel(
            writer,
            index=False,
            sheet_name="Allocation Results"
        )

    st.download_button(
        "📗 Download Results Excel",
        excel_buffer.getvalue(),
        file_name="FAIRSHIFT_Results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ==========================================
# 15. ANALYTICS
# ==========================================

with analytics:

    st.markdown("## 📊 Advanced Analytics")

    if "results" not in st.session_state:

        st.info("Generate allocation results first.")

    else:

        result_df = st.session_state.results

        c1, c2 = st.columns(2)

        with c1:

            st.markdown("### 📈 Score Distribution")

            fig = px.histogram(
                result_df,
                x="FAIRSHIFT_Score",
                nbins=10,
                color_discrete_sequence=["#00CFFF"],
                title="Applicant Score Distribution"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with c2:

            st.markdown("### 🏆 Allocation Status")

            status = result_df["Decision"].value_counts()

            fig = px.pie(
                values=status.values,
                names=status.index,
                hole=0.55,
                color_discrete_sequence=[
                    "#00D9FF",
                    "#425B88"
                ]
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown("### 📊 Top Applicants")

        top = result_df.head(10)

        label_col = (
            st.session_state.get("name_col", "Rank")
        )

        fig = px.bar(
            top,
            x="FAIRSHIFT_Score",
            y="Rank",
            orientation="h",
            color="FAIRSHIFT_Score",
            color_continuous_scale="blues"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            yaxis=dict(autorange="reversed")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==========================================
# 16. FAIRNESS AUDIT
# ==========================================

with audit:

    st.markdown("## 🛡️ Fairness & Transparency Audit")

    if "results" not in st.session_state:

        st.info("Generate results first to view the fairness audit.")

    else:

        result_df = st.session_state.results

        group_col = st.session_state.group_col

        if group_col != "None":

            st.markdown(
                f"### Group comparison: {group_col}"
            )

            fairness = result_df.groupby(
                group_col,
                dropna=False
            ).agg(
                Total_Applicants=(
                    "Rank", "count"
                ),
                Recommended=(
                    "Decision",
                    lambda x: (x == "Recommended").sum()
                ),
                Average_Score=(
                    "FAIRSHIFT_Score",
                    "mean"
                )
            ).reset_index()

            fairness["Selection_Rate"] = (
                fairness["Recommended"]
                / fairness["Total_Applicants"]
                * 100
            ).round(2)

            fairness["Average_Score"] = (
                fairness["Average_Score"].round(2)
            )

            st.dataframe(
                fairness,
                width="stretch",
                hide_index=True
            )

            rates = fairness["Selection_Rate"]

            gap = rates.max() - rates.min()

            st.metric(
                "Selection Rate Gap",
                f"{gap:.2f}%"
            )

            if gap > 20:

                st.warning(
                    "A selection-rate difference was detected. "
                    "Review the criteria and investigate possible "
                    "unfair outcomes."
                )

            else:

                st.success(
                    "No large selection-rate gap detected. "
                    "This is not proof of complete fairness."
                )

            fig = px.bar(
                fairness,
                x=group_col,
                y="Selection_Rate",
                title="Group-wise Selection Rates",
                color="Selection_Rate",
                color_continuous_scale="blues"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Select a category column in AI Demo to perform "
                "group-wise fairness analysis."
            )

        st.markdown("---")

        st.markdown("### 🔍 Explainable Decisions")

        st.dataframe(
            result_df[
                [
                    "Rank",
                    "FAIRSHIFT_Score",
                    "Decision",
                    "Decision_Explanation"
                ]
            ],
            width="stretch",
            hide_index=True
        )

        st.markdown("### 📜 Audit History")

        if st.session_state.audit:

            st.dataframe(
                pd.DataFrame(st.session_state.audit),
                width="stretch",
                hide_index=True
            )

        else:

            st.info("No audit records available.")

# ==========================================
# 17. FOOTER
# ==========================================

st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:20px;
color:#83CFFF;
">

<h3 style="color:#00D9FF !important;">
🧠 FAIRSHIFT
</h3>

AI-Powered Smart Allocation Engine

<p>
Smart • Fair • Transparent • Explainable
</p>

<p style="font-size:12px;">
College Hackathon Project | Built with Python & Streamlit
</p>

</div>
""", unsafe_allow_html=True)