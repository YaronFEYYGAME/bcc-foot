import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://api.zafronix.com/fifa/worldcup/v1"
API_KEY = os.getenv("ZAFRONIX_API_KEY")

def safe_request(url: str) -> any:
    """Effectue un GET sécurisé et retourne le JSON."""
    try:
        headers = {"X-API-Key": API_KEY}
        response = requests.get(url, headers=headers, timeout=15)
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


def get_tournaments() -> list:
    """Récupère tous les tournois CdM depuis 1930."""
    data = safe_request(f"{BASE_URL}/tournaments")
    return data if isinstance(data, list) else data.get("tournaments", [])


def get_tournament(year: int) -> dict:
    """Récupère les détails d'un tournoi par année."""
    return safe_request(f"{BASE_URL}/tournaments/{year}")


def get_team_history(team_code: str) -> dict:
    """Récupère l'historique CdM d'une nation."""
    return safe_request(f"{BASE_URL}/teams/{team_code}")


def get_matches_by_year(year: int) -> list:
    """Récupère tous les matchs d'une édition."""
    data = safe_request(f"{BASE_URL}/matches?year={year}")
    return data.get("matches", [])
