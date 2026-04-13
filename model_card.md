# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is designed to suggest songs from a small catalog based on a user's preferred genre, mood, and energy level. It is built for classroom exploration - specifically to demonstrate how content-based filtering works by matching song attributes to user preferences.

This system is **not** intended for real users or production deployment. It assumes a single static taste profile per session and has no ability to learn from user behavior over time.

---

## 3. How the Model Works

VibeFinder scores every song in the catalog against a user's preferences and returns the top matches.

For each song, the system asks three questions:

1. **Does the genre match?** If so, the song gets +2.0 points. This is the heaviest signal - genre is treated as the most important filter.
2. **Does the mood match?** A match adds +1.0 point. "Happy" and "intense" are treated as completely separate categories with no overlap.
3. **How close is the energy level?** Energy is measured on a 0-1 scale. A song with energy 0.8 scores 1.0 proximity points when the user wants 0.8, and 0.5 points when the user wants 0.3. Closer = more points.
4. **Acoustic bonus** (OOP interface only): If the user prefers acoustic music and the song is highly acoustic, it gets +0.5 extra points.

Once every song has a total score, the system sorts them from highest to lowest and returns the top five. Each recommendation comes with a plain-language explanation like: "genre match (+2.0), mood match (+1.0), energy proximity (+0.82)."

---

## 4. Data

The catalog is `data/songs.csv`, containing **20 songs**.

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, country, r&b, classical, electronic, metal

**Moods represented:** happy, chill, intense, moody, focused, relaxed, energetic, romantic, sad, aggressive

Songs were generated for this simulation and do not represent real-world releases. The starter set of 10 songs leaned heavily toward pop and lofi. Ten additional songs were added to cover underrepresented genres (hip-hop, classical, electronic, metal, country, r&b) and moods (sad, romantic, energetic, aggressive).

**Limitations of the data:** All songs are fictional. Audio feature values (energy, valence, etc.) were chosen to be plausible but are not derived from actual audio analysis. The catalog is far too small for meaningful diversity in recommendations.

---

## 5. Strengths

- **Transparent and explainable**: Every recommendation includes a specific reason. There is no black box.
- **Deterministic**: The same user profile always produces the same ranking - easy to test and debug.
- **Works well for dominant taste profiles**: A user who strongly prefers one genre and mood (e.g., lofi + chill) will consistently see their preferred songs at the top.
- **Fast**: Scoring 20 songs takes microseconds. The algorithm scales linearly.

---

## 6. Limitations and Bias

- **Genre string matching is brittle**: "indie pop" and "pop" are treated as completely different genres even though they overlap musically. A user who types "Hip Hop" (capital H) gets zero genre points against "hip-hop" in the catalog.
- **Filter bubble**: The genre weight (+2.0) is strong enough that users almost always see their own genre at the top. Songs from other genres are rarely surfaced, even when they closely match on energy and mood.
- **Genre dominates over all other signals**: The adversarial "sad but high energy classical" profile exposed this most clearly. Both classical songs in the catalog scored above 3.0 despite having energy values (0.22, 0.18) nearly opposite to the user's target (0.9). Because genre + mood together award up to +3.0 and energy proximity can only ever add up to +1.0, the system can never recommend a high-energy song over a matching-genre song regardless of how wrong the energy feels. A listener who asked for high-energy classical would get two very slow, quiet pieces.
- **Catalog sparsity silently degrades quality**: Users whose preferred genre has fewer than 3 songs in the catalog get only one strong recommendation. The rest of their top 5 are genre mismatches that scored on energy alone. This is invisible to the user - the system returns 5 results with no indication that 4 of them are poor fits.
- **Only one continuous feature scored**: Valence, danceability, and tempo are stored but ignored by the scoring function. Two songs with very different vibes (e.g., very danceable vs. not) can score identically.
- **No personalization over time**: The system has no memory of skips, replays, or explicit likes. Every session starts fresh.

---

## 7. Evaluation

Six user profiles were tested - three standard and three adversarial:

| Profile | Top Result | Score | Observation |
|---|---|---|---|
| Pop / happy / energy 0.8 | Sunrise City | 3.98 | All three signals matched - felt correct |
| Lofi / chill / energy 0.4 | Midnight Coding | 3.98 | Two lofi/chill songs tied at top - felt correct |
| Rock / intense / energy 0.9 | Storm Runner | 3.99 | Only one rock song exists; rest of list is genre misses |
| Classical / sad / energy 0.9 | Moonlight Sonata Redux | 3.32 | Correct genre/mood but energy is wrong - system recommended quiet songs to someone who wanted high energy |
| Jazz / relaxed / energy 0.5 | Coffee Shop Stories | 3.87 | Only one jazz song; positions 2-5 are energy-proximity filler |
| Ambient / chill / energy 0.5 | Spacewalk Thoughts | 3.78 | Neutral energy target spread points broadly; mood became the only tiebreaker |

**What surprised me:** The classical/sad/high-energy profile was the most revealing. I expected the system to at least try to find high-energy songs, but genre + mood points (+3.0 max) are mathematically impossible to overcome with energy alone (+1.0 max). The system is structurally incapable of recommending across genre boundaries, regardless of how conflicting the other preferences are.

**Weight shift experiment:** Halving genre weight (to +1.0) and doubling energy weight (to 0-2.0) caused "Rooftop Lights" (indie pop) to outrank "Gym Hero" (pop) for a pop profile - a genre miss beating a genre match purely on energy proximity. Rankings changed but did not improve. Original weights were restored.

**Mood-only experiment:** Removing genre scoring made many unrelated songs tie in score, reducing recommendation usefulness significantly. Genre is load-bearing for this system to work at all.

---

## 8. Future Work

- **Fuzzy genre matching**: Use embeddings or a genre taxonomy so that "indie pop" can partially match "pop," and "r&b" can partially match "soul."
- **Score more features**: Add valence and danceability to the scoring function so the system can distinguish between a "happy party song" and a "happy slow ballad."
- **Diversity penalty**: Prevent the top 5 from being dominated by one genre or artist. After selecting the top result, penalize other songs from the same genre slightly to encourage variety.
- **Collaborative signals**: Track which songs users skip or replay and adjust weights over time. Pure content-based filtering misses the "this is technically my genre but I'm tired of it" signal entirely.
- **Larger catalog**: 20 songs is too small to expose real recommendation patterns. A catalog of 500+ songs would better reveal how the scoring behaves across edge cases.

---

## 9. Personal Reflection

Building VibeFinder made the invisible visible: recommendations are math, not intuition. The system doesn't "know" that Midnight Coding sounds good while coding - it just knows that the numbers match. That gap between what the algorithm computes and what a human experiences as a good recommendation is where most of the interesting problems in AI live.

The most surprising discovery was how much the genre weight controlled the entire output. A +2.0 bonus for genre match versus +1.0 for mood means that genre mismatches are nearly unrecoverable. Real platforms like Spotify likely use learned embeddings where "indie pop" and "pop" share 80% of their genre vector - so the gap isn't binary. This project made that design choice feel concrete and necessary, not abstract.

If I kept developing this, I'd start by replacing exact string matching with a small similarity lookup table, then add valence to the score. Those two changes alone would produce noticeably more interesting recommendations without changing the core architecture.
