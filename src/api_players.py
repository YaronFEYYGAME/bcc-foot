import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL_V1 = "https://sports.bzzoiro.com/api/v1"
BASE_URL_V2 = "https://sports.bzzoiro.com/api/v2"
API_KEY = os.getenv("BSD_API_KEY")


def safe_request(url: str, params: dict = None) -> any:
    """Effectue un GET sécurisé et retourne le JSON."""
    try:
        headers = {"Authorization": f"Token {API_KEY}"}
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise RuntimeError("L'API ne répond pas (timeout).")
    except requests.ConnectionError:
        raise RuntimeError("Problème réseau.")
    except requests.HTTPError as e:
        raise RuntimeError(f"Erreur HTTP {e.response.status_code}.")
    except ValueError:
        raise RuntimeError("La réponse n'est pas du JSON valide.")


def search_player(name: str) -> list:
    """Recherche un joueur par son nom."""
    data = safe_request(f"{BASE_URL_V2}/players/", {"name": name})
    return data.get("results", [])


def get_player(player_id: int) -> dict:
    """Récupère le profil complet d'un joueur."""
    return safe_request(f"{BASE_URL_V2}/players/{player_id}/")


def get_player_stats(player_id: int) -> dict:
    """Récupère les stats d'un joueur."""
    return safe_request(f"{BASE_URL_V2}/players/{player_id}/stats/")


def get_worldcup_squad(team_code: str) -> list:
    """Récupère le squad CdM 2026 d'une équipe."""
    data = safe_request(f"{BASE_URL_V2}/worldcup/squads/", {"team": team_code})
    return data.get("results", [])


def get_player_aggregated_stats(player_id: int) -> dict:
    """Récupère et agrège les stats par match d'un joueur (totaux + moyennes)."""
    raw = get_player_stats(player_id)

    # L'API peut retourner une liste de matchs ou un dict avec "results"
    matches = raw if isinstance(raw, list) else raw.get("results", [])

    if not matches:
        return {}

    # Champs à cumuler
    sum_fields = [
        "goals", "goal_assist", "total_shots", "shots_on_target",
        "key_pass", "total_pass", "accurate_pass", "total_contest",
        "won_contest", "duel_won", "duel_lost", "aerial_won", "aerial_lost",
        "total_tackle", "won_tackle", "interception", "ball_recovery",
        "was_fouled", "fouls", "yellow_card", "red_card", "minutes_played",
        "touches", "dispossessed", "possession_lost",
    ]
    # Champs à moyenner
    avg_fields = ["rating", "expected_goals", "expected_assists"]

    n = len(matches)
    agg = {"matches_played": n}

    for f in sum_fields:
        agg[f] = sum(m.get(f, 0) or 0 for m in matches)

    for f in avg_fields:
        vals = [m.get(f, 0) or 0 for m in matches]
        agg[f] = round(sum(vals) / n, 2) if n else 0

    # Moyennes par match pour les champs cumulés principaux
    agg["goals_per_match"] = round(agg["goals"] / n, 2) if n else 0
    agg["assists_per_match"] = round(agg["goal_assist"] / n, 2) if n else 0
    agg["shots_per_match"] = round(agg["total_shots"] / n, 2) if n else 0

    # Précision de passes en %
    if agg["total_pass"] > 0:
        agg["pass_accuracy"] = round(100 * agg["accurate_pass"] / agg["total_pass"], 1)
    else:
        agg["pass_accuracy"] = 0

    return agg
