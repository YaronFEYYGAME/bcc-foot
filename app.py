import streamlit as st

st.set_page_config(
    page_title="BCC Foot",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar navigation ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/a/a3/FIFA_World_Cup_2026.svg/200px-FIFA_World_Cup_2026.svg.png", width=150)
st.sidebar.title("⚽ BCC Foot")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏟️ Matchs en direct", "📊 Classements", "👤 Comparaison joueurs", "🏆 Historique nations"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Data : worldcup26.ir · BSD · Zafronix")

# --- Routing ---
if page == "🏟️ Matchs en direct":
    from pages.matches import show
    show()

elif page == "📊 Classements":
    from pages.standings import show
    show()

elif page == "👤 Comparaison joueurs":
    from pages.compare import show
    show()

elif page == "🏆 Historique nations":
    from pages.history import show
    show()
