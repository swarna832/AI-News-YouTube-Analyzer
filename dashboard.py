import streamlit as st
st.markdown("""
<style>

/* Main App */
.main {
    background-color: #f5f7fb;
}

/* Metric Cards */
div[data-testid="metric-container"] {
            div[data-testid="metric-container"] {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border-left: 6px solid #4F8BF9;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
    transition: all .3s ease;
}

div[data-testid="metric-container"]:hover{
    transform: translateY(-4px);
    box-shadow: 0px 12px 25px rgba(0,0,0,0.15);
}
    background-color: white;
    border: 1px solid #E6EAF2;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* Headings */
h1 {
    color: #1F3C88;
    font-size:42px;
    font-weight:800;
}

h2 {
    color:#355C7D;
    font-size:30px;
}
}

h3 {
    color: #355C7D;
}

</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="AI Sentiment Analysis Dashboard",
    layout="wide"
)

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "🏠 Home",
        "📰 News Dashboard",
        "🎥 YouTube Dashboard"
    ]
)

# ---------------- HOME ----------------

if page == "🏠 Home":

    st.title("🤖 AI Sentiment Analysis & Fake News Detection")
    st.markdown("""
<div style="
background: linear-gradient(90deg,#1F3C88,#4F8BF9);
padding:25px;
border-radius:18px;
color:white;
margin-bottom:20px;
">

<h2 style="color:white;margin-bottom:10px;">
🚀 AI Intelligence Dashboard
</h2>

<p style="font-size:18px;">
Analyze News Articles and YouTube Comments using Artificial Intelligence.
</p>

✔ Sentiment Analysis<br>
✔ Fake News Detection<br>
✔ AI Insights<br>
✔ Interactive Charts<br>
✔ Download Reports

</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
# 👋 Welcome!

This AI-powered dashboard provides two intelligent analysis modules.

### 📰 News Dashboard
- Fake News Detection
- Sentiment Analysis
- Interactive Charts
- News Search

---

### 🎥 YouTube Dashboard
- Search Videos
- Fetch Comments
- AI Sentiment Analysis
- Charts & Statistics
- Comment Filtering
- CSV Download

---

### 🛠️ Technologies Used

- Python
- Streamlit
- Hugging Face Transformers
- YouTube Data API v3
- Pandas
- Matplotlib
st.markdown("---")
st.subheader("📈 Project Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("📰 News Articles", "500+")
col2.metric("🎥 Videos Analyzed", "10+")
col3.metric("💬 Comments Processed", "1000+")
col4.metric("🤖 AI Models", "2")

---

### 👩‍💻 Developed By

**Swarna Mishra**
    """)

# ---------------- NEWS ----------------

elif page == "📰 News Dashboard":

    exec(open("src/news_dashboard.py", encoding="utf-8").read())

# ---------------- YOUTUBE ----------------

elif page == "🎥 YouTube Dashboard":

    exec(open("src/youtube_dashboard.py", encoding="utf-8").read())
    st.markdown("---")

st.caption(
    "🚀 Developed by Swarna Mishra | AI Sentiment Analysis & Fake News Detection | Streamlit + Hugging Face + YouTube API"
)
