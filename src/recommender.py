import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes. Required by tests/test_recommender.py"""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences. Required by tests/test_recommender.py"""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_song_obj(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Compute a score and reasons for a Song object against a UserProfile."""
    score = 0.0
    reasons = []

    if song.genre == user.favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.mood == user.favorite_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_points = round(1.0 - abs(song.energy - user.target_energy), 2)
    score += energy_points
    reasons.append(f"energy proximity (+{energy_points})")

    if user.likes_acoustic and song.acousticness > 0.6:
        score += 0.5
        reasons.append("acoustic match (+0.5)")

    return round(score, 2), reasons


def _score_song_dict(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a score and reasons for a song dict against a user prefs dict."""
    score = 0.0
    reasons = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_points = round(1.0 - abs(song.get("energy", 0.5) - user_prefs.get("energy", 0.5)), 2)
    score += energy_points
    reasons.append(f"energy proximity (+{energy_points})")

    return round(score, 2), reasons


class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by weighted score for the given user."""
        scored = [(_score_song_obj(user, song)[0], song) for song in self.songs]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why this song was recommended."""
        _, reasons = _score_song_obj(user, song)
        return ", ".join(reasons) if reasons else "no strong match found"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return them as a list of dicts with numeric types."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score and rank songs against user preferences; return top k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = _score_song_dict(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
