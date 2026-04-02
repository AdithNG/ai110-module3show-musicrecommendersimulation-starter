# Music Recommender Simulation

## Project Summary

This project simulates how a content-based music recommendation system works. Given a user's taste profile (preferred genre, mood, and energy level), the system scores every song in a catalog and returns the top matches with plain-language explanations.

The recommender uses a weighted scoring formula: genre similarity is worth the most (+2.0), followed by mood (+1.0), then energy proximity (up to +1.0 based on closeness). Songs are ranked by total score and the top k results are returned with a reason string explaining each recommendation.

---

## How The System Works

### Song Features

Each song in `data/songs.csv` has the following attributes:

| Feature | Type | Description |
|---|---|---|
| genre | string | Musical category (e.g. pop, rock, lofi) |
| mood | string | Emotional tone (e.g. happy, chill, intense) |
| energy | float (0–1) | Intensity level — 1.0 is maximum energy |
| tempo_bpm | float | Beats per minute |
| valence | float (0–1) | Musical positivity — higher = more upbeat |
| danceability | float (0–1) | How suitable for dancing |
| acousticness | float (0–1) | How acoustic (vs. electronic) the track is |

### User Profile

The system uses two interfaces:

- **Functional** (used by `main.py`): a dict with keys `genre`, `mood`, and `energy`
- **OOP** (used by tests): a `UserProfile` dataclass with `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`

### Algorithm Recipe

For each song, the system computes:

```
score = 0

if song.genre == user.genre:    score += 2.0   # genre match
if song.mood == user.mood:      score += 1.0   # mood match
score += 1.0 - |song.energy - user.energy|     # energy proximity (0–1)
if user.likes_acoustic and song.acousticness > 0.6:
    score += 0.5                               # acoustic bonus
```

Songs are then ranked with `sorted(..., reverse=True)` by score, and the top `k` are returned.

### Data Flow

```
User preferences dict
        ↓
recommend_songs(user_prefs, songs, k=5)
        ↓
  for each song → _score_song_dict() → (score, reasons)
        ↓
  sorted by score descending
        ↓
Top k results: (song_dict, score, explanation string)
        ↓
main.py prints: title, score, "Because: ..."
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

```bash
pytest
```

---

## Experiments

### Profile 1 — High-Energy Pop (default)
`{"genre": "pop", "mood": "happy", "energy": 0.8}`

Top results: "Sunrise City" and "Gym Hero" dominate because they match genre + mood. "Rooftop Lights" (indie pop, happy) scores slightly lower — it gets the mood and energy match but not the genre.

### Profile 2 — Chill Lofi
`{"genre": "lofi", "mood": "chill", "energy": 0.4}`

Top results: "Library Rain" and "Midnight Coding" score highest (+3.9 each). Songs in other genres with low energy still score reasonably on energy proximity alone.

### Profile 3 — Intense Rock
`{"genre": "rock", "mood": "intense", "energy": 0.9}`

Top result: "Storm Runner" gets genre + mood + near-perfect energy proximity. "Gym Hero" and "Iron Curtain" get energy credit but miss genre.

### Weight Shift Experiment
When energy weight was doubled (2× the energy distance term), songs with very different energy but matching genre started dropping noticeably. The ranking became more sensitive to energy closeness and less stable for genre-first users. Overall, the default weights felt more balanced.

### Mood-Only Experiment
Temporarily commenting out the genre check caused "Midnight Coding" and "Library Rain" to tie with "Sunrise City" for a happy/pop profile — because all three matched on mood proximity after genre was removed. This showed how much genre dominates the default ranking.

---

## Limitations and Risks

- **Small catalog**: Only 20 songs. A real system has millions. Rankings are highly influenced by which genres happen to be overrepresented.
- **Exact string matching**: Genre and mood are matched exactly. A user who types "Hip Hop" instead of "hip-hop" gets zero genre points.
- **No user history**: The system treats every user identically given the same profile. There's no learning from skips, likes, or replays.
- **Energy is the only continuous feature scored**: Valence, danceability, and tempo_bpm are stored but not used in scoring, so two songs with very different "vibe" can score identically.
- **Filter bubble risk**: A user who loves pop will always get pop at the top. The system never introduces variety or serendipity.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender made it clear that "AI recommendations" are not magic — they are just math applied to data. The system doesn't understand music; it computes distances between numbers and returns the smallest ones. This is obvious from the inside, but invisible to a listener using an app.

The most surprising thing was how much the genre weight dominated. With +2.0 for genre vs. +1.0 for mood and up to +1.0 for energy, a genre mismatch is nearly impossible to overcome. A sad classical piano piece will never surface for a "happy pop" user, even if its valence and energy are actually close — because the genre string doesn't match. Real systems use embedding models that understand that "indie pop" and "pop" are adjacent, or that "chill" and "relaxed" overlap. This project revealed exactly where that gap is.
