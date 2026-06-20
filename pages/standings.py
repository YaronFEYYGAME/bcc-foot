import streamlit as st
import pandas as pd
from src.api_worldcup import get_groups
from src.parsing import parse_standings

def show():
    st.title("📊 Classements par groupe")

    with st.spinner("Chargement des classements..."):
        try:
            raw = get_groups()
            standings = parse_standings(raw)
        except RuntimeError as e:
            st.error(str(e))
            st.stop()

    # Grouper par groupe
    groups = {}
    for s in standings:
        g = s["group"]
        if g not in groups:
            groups[g] = []
        groups[g].append(s)

    # Afficher chaque groupe
    cols = st.columns(2)
    for i, (group_name, teams) in enumerate(sorted(groups.items())):
        with cols[i % 2]:
            st.markdown(f"### Groupe {group_name}")
            df = pd.DataFrame(teams)[["team", "played", "won", "drawn", "lost", "goals_for", "goals_against", "goal_diff", "points"]]
            df.columns = ["Équipe", "J", "V", "N", "D", "BP", "BC", "DB", "Pts"]
            df = df.sort_values("Pts", ascending=False).reset_index(drop=True)
            st.dataframe(df, hide_index=True, use_container_width=True)
