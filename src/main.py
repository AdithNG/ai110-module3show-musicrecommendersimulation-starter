"""
Command line runner for the Music Recommender Simulation.

Runs standard profiles, adversarial profiles, and optional challenge demos:
- Challenge 1: Extended song features (popularity, liveness, speechiness)
- Challenge 2: Scoring mode comparison across four weight presets
- Challenge 3: Diverse recommendations with genre/artist penalties
- Challenge 4: Tabulate-formatted output tables
"""

from src.recommender import load_songs, recommend_songs, recommend_diverse, SCORING_MODES
from tabulate import tabulate


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Plain text output - used for standard and adversarial profiles."""
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"\n{'=' * 50}")
    print(f"Profile: {label}")
    print(f"Preferences: {user_prefs}")
    print(f"{'=' * 50}")
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


def print_table(label: str, user_prefs: dict, results: list) -> None:
    """Challenge 4: tabulate-formatted output table."""
    print(f"\n{'=' * 50}")
    print(f"Profile: {label}")
    print(f"Preferences: {user_prefs}")
    print(f"{'=' * 50}")
    rows = [
        [i + 1, song["title"], song["artist"], song["genre"], f"{score:.2f}", explanation]
        for i, (song, score, explanation) in enumerate(results)
    ]
    print(tabulate(rows, headers=["Rank", "Title", "Artist", "Genre", "Score", "Why"], tablefmt="github"))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # --- Standard profiles ---

    print_recommendations(
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        songs,
    )

    print_recommendations(
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.4},
        songs,
    )

    print_recommendations(
        "Deep Intense Rock",
        {"genre": "rock", "mood": "intense", "energy": 0.9},
        songs,
    )

    # --- Adversarial profiles ---

    print_recommendations(
        "Adversarial - Sad but High Energy",
        {"genre": "classical", "mood": "sad", "energy": 0.9},
        songs,
    )

    print_recommendations(
        "Adversarial - Underrepresented Genre (jazz)",
        {"genre": "jazz", "mood": "relaxed", "energy": 0.5},
        songs,
    )

    print_recommendations(
        "Adversarial - All Neutral Preferences",
        {"genre": "ambient", "mood": "chill", "energy": 0.5},
        songs,
    )

    # --- Challenge 2: Scoring mode comparison ---

    print(f"\n{'#' * 50}")
    print("CHALLENGE 2 - Scoring Mode Comparison")
    print(f"Profile: Chill Lofi  |  genre=lofi, mood=chill, energy=0.4")
    print(f"{'#' * 50}")
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.4}
    for mode_name in SCORING_MODES:
        results = recommend_songs(prefs, songs, k=3, mode=mode_name)
        rows = [
            [song["title"], song["genre"], f"{score:.2f}"]
            for song, score, _ in results
        ]
        print(f"\nMode: {mode_name}  (weights: {SCORING_MODES[mode_name]})")
        print(tabulate(rows, headers=["Title", "Genre", "Score"], tablefmt="github"))

    # --- Challenge 3: Diverse recommendations ---

    print(f"\n{'#' * 50}")
    print("CHALLENGE 3 - Diverse Recommendations")
    print(f"{'#' * 50}")
    pop_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    standard_results = recommend_songs(pop_prefs, songs, k=5)
    diverse_results = recommend_diverse(pop_prefs, songs, k=5)

    print("\nStandard top-5 (High-Energy Pop):")
    rows = [[s["title"], s["genre"], f"{sc:.2f}"] for s, sc, _ in standard_results]
    print(tabulate(rows, headers=["Title", "Genre", "Score"], tablefmt="github"))

    print("\nDiverse top-5 (High-Energy Pop):")
    rows = [[s["title"], s["genre"], f"{sc:.2f}"] for s, sc, _ in diverse_results]
    print(tabulate(rows, headers=["Title", "Genre", "Score"], tablefmt="github"))

    # --- Challenge 4: Tabulate full output for one profile ---

    print(f"\n{'#' * 50}")
    print("CHALLENGE 4 - Tabulate Full Output")
    print(f"{'#' * 50}")
    print_table(
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        recommend_songs({"genre": "pop", "mood": "happy", "energy": 0.8}, songs, k=5),
    )
    print_table(
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.4},
        recommend_songs({"genre": "lofi", "mood": "chill", "energy": 0.4}, songs, k=5),
    )


if __name__ == "__main__":
    main()
