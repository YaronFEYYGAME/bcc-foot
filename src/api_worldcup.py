import requests
import urllib3
from requests.adapters import HTTPAdapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://worldcup26.ir"

def make_session():
    session = requests.Session()
    session.verify = False
    adapter = HTTPAdapter(max_retries=3)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def safe_request(url: str) -> any:
    try:
        session = make_session()
        response = session.get(url, timeout=30)
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
    data = safe_request(f"{BASE_URL}/get/games")
    return data.get("games", [])

def get_groups() -> list:
    data = safe_request(f"{BASE_URL}/get/groups")
    return data.get("groups", [])

def get_teams() -> list:
    data = safe_request(f"{BASE_URL}/get/teams")
    return data.get("teams", [])

def get_stadiums() -> list:
    data = safe_request(f"{BASE_URL}/get/stadiums")
    return data.get("stadiums", [])
