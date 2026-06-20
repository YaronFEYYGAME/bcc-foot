import streamlit as st
from src.api_worldcup import get_games
from src.parsing import parse_games

def show():
    st.title("🏟️ Matchs en direct — Coupe du Monde 2026")

    with st.spinner("Chargement des matchs..."):
        try:
            raw = get_games()
            games = parse_games(raw)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        stage_filter = st.selectbox("Phase", ["Tous", "group", "round_of_32", "quarter", "semi", "final"])
    with col2:
        status_filter = st.selectbox("Statut", ["Tous", "Terminés", "À venir"])

    # Filtrage
    filtered = games
    if stage_filter != "Tous":
        filtered = [g for g in filtered if g["stage"] == stage_filter]
    if status_filter == "Terminés":
        filtered = [g for g in filtered if g["finished"]]
    elif status_filter == "À venir":
        filtered = [g for g in filtered if not g["finished"]]

    st.markdown(f"**{len(filtered)} matchs affichés**")
    st.divider()

    for g in filtered:
        col1, col2, col3 = st.columns([3, 1, 3])
        with col1:
            st.markdown(f"### {g['home_team']}")
        with col2:
            if g["finished"]:
                st.markdown(f"## {g['home_score']} — {g['away_score']}")
            else:
                st.markdown("## vs")
        with col3:
            st.markdown(f"### {g['away_team']}")

        st.caption(f"Groupe {g['group']} · Journée {g['matchday']} · {g['date']}")
        st.divider()
