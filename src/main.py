"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n{'=' * 50}")
    print(f"Profile: {label}")
    print(f"Preferences: {user_prefs}")
    print(f"{'=' * 50}")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Profile 1: High-Energy Pop
    print_recommendations(
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        songs,
    )

    # Profile 2: Chill Lofi
    print_recommendations(
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.4},
        songs,
    )

    # Profile 3: Deep Intense Rock
    print_recommendations(
        "Deep Intense Rock",
        {"genre": "rock", "mood": "intense", "energy": 0.9},
        songs,
    )

    # Adversarial Profile 4: Conflicting mood and energy (sad but high energy)
    # Tests whether the system handles contradictory preferences gracefully
    print_recommendations(
        "Adversarial - Sad but High Energy",
        {"genre": "classical", "mood": "sad", "energy": 0.9},
        songs,
    )

    # Adversarial Profile 5: Genre with almost no catalog coverage
    # Tests what happens when the system has very little to work with
    print_recommendations(
        "Adversarial - Underrepresented Genre (jazz)",
        {"genre": "jazz", "mood": "relaxed", "energy": 0.5},
        songs,
    )

    # Adversarial Profile 6: Middle-of-the-road everything
    # Tests whether neutral preferences produce useful or bland results
    print_recommendations(
        "Adversarial - All Neutral Preferences",
        {"genre": "ambient", "mood": "chill", "energy": 0.5},
        songs,
    )


if __name__ == "__main__":
    main()
