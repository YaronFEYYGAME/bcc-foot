import streamlit as st
from src.api_players import search_player, get_player
from src.parsing import parse_player, parse_players

def show():
    st.title("👤 Comparaison de joueurs")
    st.markdown("Recherche deux joueurs et compare leurs stats côte à côte.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Joueur 1")
        query1 = st.text_input("Rechercher", placeholder="ex: Mbappe", key="p1")
        player1 = None
        if query1:
            results1 = parse_players(search_player(query1))
            if results1:
                names1 = [p["name"] for p in results1]
                choice1 = st.selectbox("Sélectionner", names1, key="sel1")
                player1 = next(p for p in results1 if p["name"] == choice1)

    with col2:
        st.markdown("### Joueur 2")
        query2 = st.text_input("Rechercher", placeholder="ex: Vinicius", key="p2")
        player2 = None
        if query2:
            results2 = parse_players(search_player(query2))
            if results2:
                names2 = [p["name"] for p in results2]
                choice2 = st.selectbox("Sélectionner", names2, key="sel2")
                player2 = next(p for p in results2 if p["name"] == choice2)

    if player1 and player2:
        st.divider()
        st.markdown("### 📊 Comparaison")

        stats = [
            ("Nationalité", "nationality"),
            ("Âge", "age"),
            ("Position", "specific_position"),
            ("Taille (cm)", "height"),
            ("Pied préféré", "preferred_foot"),
            ("Rating", "rating"),
            ("Valeur marchande (€)", "market_value"),
            ("Risque blessure", "injury_risk"),
            ("Contrat jusqu'au", "contract_until"),
        ]

        for label, key in stats:
            col1, col2, col3 = st.columns([2, 2, 2])
            v1 = player1.get(key, "—") or "—"
            v2 = player2.get(key, "—") or "—"
            with col1:
                st.markdown(f"**{v1}**")
            with col2:
                st.markdown(f"*{label}*")
            with col3:
                st.markdown(f"**{v2}**")
