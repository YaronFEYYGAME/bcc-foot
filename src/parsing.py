def parse_game(raw: dict) -> dict:
    """Nettoie un match brut de worldcup26.ir."""
    return {
        "id": raw.get("id", ""),
        "home_team": raw.get("home_team_name_en", "?"),
        "away_team": raw.get("away_team_name_en", "?"),
        "home_score": raw.get("home_score"),
        "away_score": raw.get("away_score"),
        "group": raw.get("group", ""),
        "stage": raw.get("type", "group"),
        "matchday": raw.get("matchday", ""),
        "date": raw.get("local_date", "")[:10] if raw.get("local_date") else "?",
        "time": raw.get("local_date", "")[-5:] if raw.get("local_date") else "?",
        "stadium_id": raw.get("stadium_id", ""),
        "finished": raw.get("finished", False),
        "home_scorers": raw.get("home_scorers", ""),
        "away_scorers": raw.get("away_scorers", ""),
    }


def parse_games(raw_list: list) -> list:
    """Parse une liste de matchs."""
    return [parse_game(g) for g in raw_list]


def parse_group_standing(raw: dict) -> dict:
    """Nettoie une entrée de classement de groupe."""
    return {
        "group": raw.get("group", ""),
        "team": raw.get("team_name_en", raw.get("team", "?")),
        "played": raw.get("mp", raw.get("played", 0)),
        "won": raw.get("w", raw.get("won", 0)),
        "drawn": raw.get("d", raw.get("drawn", 0)),
        "lost": raw.get("l", raw.get("lost", 0)),
        "goals_for": raw.get("gf", raw.get("goals_for", 0)),
        "goals_against": raw.get("ga", raw.get("goals_against", 0)),
        "goal_diff": raw.get("gd", raw.get("goal_difference", 0)),
        "points": raw.get("pts", raw.get("points", 0)),
    }


def parse_standings(raw_list: list) -> list:
    """Parse une liste de classements."""
    return [parse_group_standing(g) for g in raw_list]


def parse_player(raw: dict) -> dict:
    """Nettoie un joueur brut de BSD."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", "Inconnu"),
        "short_name": raw.get("short_name", ""),
        "nationality": raw.get("nationality", "Non renseigné"),
        "position": raw.get("position", "Non renseigné"),
        "specific_position": raw.get("specific_position", ""),
        "age": _calc_age(raw.get("date_of_birth")),
        "height": raw.get("height_cm"),
        "preferred_foot": raw.get("preferred_foot", ""),
        "market_value": raw.get("market_value_eur"),
        "rating": raw.get("rating"),
        "potential": raw.get("potential"),
        "injury_risk": raw.get("injury_risk", ""),
        "contract_until": raw.get("contract_until", ""),
    }


def _calc_age(dob: str) -> int | None:
    """Calcule l'âge à partir de la date de naissance."""
    if not dob:
        return None
    try:
        from datetime import date
        birth = date.fromisoformat(dob)
        today = date.today()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except Exception:
        return None


def parse_players(raw_list: list) -> list:
    """Parse une liste de joueurs."""
    return [parse_player(p) for p in raw_list]


def parse_tournament(raw: dict) -> dict:
    """Nettoie un tournoi historique de Zafronix."""
    hosts = raw.get("host", [])
    if isinstance(hosts, list):
        host_str = ", ".join(hosts)
    else:
        host_str = str(hosts)

    return {
        "year": raw.get("year"),
        "host": host_str,
        "champion": raw.get("champion", "Non renseigné"),
        "runner_up": raw.get("runner_up", "Non renseigné"),
        "third": raw.get("third_place", "Non renseigné"),
        "total_goals": raw.get("total_goals"),
        "total_matches": raw.get("total_matches"),
        "total_teams": raw.get("total_teams"),
    }


def parse_tournaments(raw_list: list) -> list:
    """Parse une liste de tournois."""
    return [parse_tournament(t) for t in raw_list]
