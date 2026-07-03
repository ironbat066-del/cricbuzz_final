"""HTTP client for Cricbuzz Cricket on RapidAPI."""

from __future__ import annotations

from typing import Any

import requests

from config import CRICBUZZ_API_BASE_URL, RAPIDAPI_HOST, RAPIDAPI_KEY


class CricbuzzClient:
    ENDPOINTS = {
        "live_matches": "/matches/v1/live",
        "recent_matches": "/matches/v1/recent",
        "upcoming_matches": "/matches/v1/upcoming",
        "match_info": "/matches/v1/{match_id}/info",
        "match_scorecard": "/matches/v1/{match_id}/scard",
        "match_scorecard_alt": "/matches/v1/{match_id}/scorecard",
        "series_list": "/series/v1/international",
        "series_matches": "/series/v1/{series_id}",
        "player_info": "/stats/v1/player/{player_id}",
        "player_search": "/stats/v1/player/search",
        "venue_info": "/venues/v1/{venue_id}",
        "teams_international": "/teams/v1/international",
    }

    def __init__(self) -> None:
        if not RAPIDAPI_KEY:
            raise ValueError("Set RAPIDAPI_KEY in .env")
        self.base_url = CRICBUZZ_API_BASE_URL.rstrip("/")
        self.headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST,
            "Accept": "application/json",
        }

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        if response.status_code == 429:
            raise RuntimeError(
                "RapidAPI monthly quota exceeded. Upgrade your plan or wait for reset."
            )
        response.raise_for_status()
        return response.json()

    def live_matches(self) -> Any:
        return self.get(self.ENDPOINTS["live_matches"])

    def recent_matches(self) -> Any:
        return self.get(self.ENDPOINTS["recent_matches"])

    def match_info(self, match_id: int) -> Any:
        return self.get(self.ENDPOINTS["match_info"].format(match_id=match_id))

    def match_scorecard(self, match_id: int) -> Any:
        for key in ("match_scorecard", "match_scorecard_alt"):
            try:
                return self.get(self.ENDPOINTS[key].format(match_id=match_id))
            except requests.HTTPError:
                continue
        raise requests.HTTPError(f"No scorecard endpoint for match {match_id}")
