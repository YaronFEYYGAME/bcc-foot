import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://worldcup26.ir"

def safe_request(url: str) -> any:
    """Effectue un GET sécurisé et retourne le JSON."""
    try:
        response = requests.get(url, timeout=30, verify=False)
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


def get_games() -> list:
    """Récupère tous les matchs de la CdM 2026."""
    data = safe_request(f"{BASE_URL}/get/games")
    return data.get("games", [])


def get_groups() -> list:
    """Récupère les classements par groupe."""
    data = safe_request(f"{BASE_URL}/get/groups")
    return data.get("groups", [])


def get_teams() -> list:
    """Récupère les 48 équipes."""
    data = safe_request(f"{BASE_URL}/get/teams")
    return data.get("teams", [])


def get_stadiums() -> list:
    """Récupère les 16 stades."""
    data = safe_request(f"{BASE_URL}/get/stadiums")
    return data.get("stadiums", [])
