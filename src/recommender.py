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


# Challenge 2: scoring mode presets
# Each mode adjusts the weights used for genre, mood, and energy scoring.
# "balanced" is the default and matches the original algorithm.
SCORING_MODES = {
    "balanced": {"genre": 2.0, "mood": 1.0, "energy_max": 1.0},
    "genre_first": {"genre": 3.0, "mood": 0.5, "energy_max": 0.5},
    "mood_first": {"genre": 1.0, "mood": 2.0, "energy_max": 1.0},
    "energy_focused": {"genre": 1.0, "mood": 0.5, "energy_max": 2.0},
}


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score a single song dict against user preference dict; return (score, reasons).

    Challenge 1: also scores popularity, liveness, and speechiness if present.
    Challenge 2: accepts a mode string that controls genre/mood/energy weights.
    """
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    score = 0.0
    reasons = []

    if song.get("genre") == user_prefs.get("genre"):
        pts = weights["genre"]
        score += pts
        reasons.append(f"genre match (+{pts})")

    if song.get("mood") == user_prefs.get("mood"):
        pts = weights["mood"]
        score += pts
        reasons.append(f"mood match (+{pts})")

    energy_max = weights["energy_max"]
    energy_points = round(energy_max * (1.0 - abs(song.get("energy", 0.5) - user_prefs.get("energy", 0.5))), 2)
    score += energy_points
    reasons.append(f"energy proximity (+{energy_points})")

    # Challenge 1: popularity bonus (normalized 0-1 from 0-100 scale, worth up to +0.5)
    if "popularity" in song and song["popularity"] is not None:
        pop_score = round(float(song["popularity"]) / 100 * 0.5, 2)
        score += pop_score
        reasons.append(f"popularity (+{pop_score})")

    # Challenge 1: liveness penalty (live recordings feel less polished for studio listeners)
    if "liveness" in song and song["liveness"] is not None:
        liveness_val = float(song["liveness"])
        if liveness_val > 0.5:
            penalty = round((liveness_val - 0.5) * 0.4, 2)
            score -= penalty
            reasons.append(f"liveness penalty (-{penalty})")

    # Challenge 1: speechiness penalty (high spoken-word content reduces music feel)
    if "speechiness" in song and song["speechiness"] is not None:
        speech_val = float(song["speechiness"])
        if speech_val > 0.33:
            penalty = round((speech_val - 0.33) * 0.5, 2)
            score -= penalty
            reasons.append(f"speechiness penalty (-{penalty})")

    return round(score, 2), reasons


def _score_song_obj(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Score a Song dataclass against a UserProfile; return (score, reasons)."""
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


class Recommender:
    """OOP implementation of the recommendation logic. Required by tests/test_recommender.py"""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by weighted score for the given user."""
        scored = sorted(
            self.songs,
            key=lambda song: _score_song_obj(user, song)[0],
            reverse=True,
        )
        return scored[:k]

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
            # Challenge 1 columns (present when using extended CSV)
            if "popularity" in row:
                row["popularity"] = float(row["popularity"])
            if "liveness" in row:
                row["liveness"] = float(row["liveness"])
            if "speechiness" in row:
                row["speechiness"] = float(row["speechiness"])
            songs.append(row)
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs; return top k as (song, score, explanation) tuples.

    Uses sorted() instead of list.sort() so the original songs list is not mutated.
    sorted() returns a new list, making this function free of side effects.

    Challenge 2: accepts a mode string passed through to score_song().
    """
    scored = [
        (song, *score_song(user_prefs, song, mode=mode))
        for song in songs
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]


def recommend_diverse(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Challenge 3: greedy diverse selection.

    Selects songs one at a time. After each pick, applies a penalty to remaining
    songs that share the same genre or artist as the picked song. This prevents
    the top-k from clustering in one genre corner of the catalog.

    Penalty: -0.8 per genre repeat, -0.6 per artist repeat (applied cumulatively).
    """
    scored = {
        song["id"]: [song, *score_song(user_prefs, song, mode=mode)]
        for song in songs
    }
    # Convert reasons list to str immediately for final output
    penalties: Dict[int, float] = {sid: 0.0 for sid in scored}
    selected = []

    for _ in range(k):
        if not scored:
            break
        # Pick the song with the highest (score - penalty)
        best_id = max(scored.keys(), key=lambda sid: scored[sid][1] - penalties[sid])
        best_song, best_score, best_reasons = scored.pop(best_id)
        effective_score = round(best_score - penalties[best_id], 2)
        selected.append((best_song, effective_score, ", ".join(best_reasons)))

        # Apply diversity penalties to remaining songs
        for sid, entry in scored.items():
            remaining_song = entry[0]
            if remaining_song.get("genre") == best_song.get("genre"):
                penalties[sid] += 0.8
            if remaining_song.get("artist") == best_song.get("artist"):
                penalties[sid] += 0.6

    return selected
