import streamlit as st
import pandas as pd
from src.api_history import get_tournaments, get_tournament
from src.parsing import parse_tournaments, parse_tournament

def show():
    st.title("🏆 Historique des nations — Coupe du Monde")

    with st.spinner("Chargement de l'historique..."):
        try:
            raw = get_tournaments()
            tournaments = parse_tournaments(raw)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    st.markdown(f"**{len(tournaments)} éditions disponibles (1930 → 2026)**")
    st.divider()

    # Tableau général
    df = pd.DataFrame(tournaments)
    df.columns = ["Année", "Pays hôte", "Champion", "Finaliste", "3ème place", "Buts", "Matchs", "Équipes"]
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.divider()

    # Détail par édition
    st.markdown("### 🔍 Détail par édition")
    years = [t["year"] for t in tournaments]
    selected_year = st.selectbox("Choisir une année", years)

    if selected_year:
        with st.spinner(f"Chargement de l'édition {selected_year}..."):
            try:
                detail = get_tournament(selected_year)
                t = parse_tournament(detail)
            except RuntimeError as e:
                st.error(str(e))
                st.stop()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Champion 🏆", t["champion"])
        with col2:
            st.metric("Finaliste", t["runner_up"])
        with col3:
            st.metric("3ème place", t["third"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total buts", t["total_goals"])
        with col2:
            st.metric("Total matchs", t["total_matches"])
        with col3:
            st.metric("Équipes", t["total_teams"])
