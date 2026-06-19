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
