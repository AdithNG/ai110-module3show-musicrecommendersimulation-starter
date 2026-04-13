# Reflection: Comparing User Profile Outputs

## Profile Comparisons

### High-Energy Pop vs. Chill Lofi

**High-Energy Pop** (`genre: pop, mood: happy, energy: 0.8`)
Top results: Sunrise City (3.98), Gym Hero (2.87), Rooftop Lights (1.96)

**Chill Lofi** (`genre: lofi, mood: chill, energy: 0.4`)
Top results: Midnight Coding (3.98), Library Rain (3.95), Focus Flow (3.00)

**What changed and why:** The top scores are nearly identical (3.98 each), but the songs are completely different. Both profiles benefited from having multiple catalog songs in their preferred genre - pop has 2 exact matches, lofi has 3. The lofi profile actually produces tighter top results (3.98 and 3.95) because two lofi/chill songs match almost perfectly on energy, while the pop profile's #2 result (Gym Hero) only matches genre - not mood - because Gym Hero is tagged as "intense" rather than "happy." This shows how much mood alignment matters within a matching genre.

---

### Chill Lofi vs. Deep Intense Rock

**Chill Lofi** (`genre: lofi, mood: chill, energy: 0.4`)
Top results: Midnight Coding (3.98), Library Rain (3.95), Focus Flow (3.00)

**Deep Intense Rock** (`genre: rock, mood: intense, energy: 0.9`)
Top results: Storm Runner (3.99), Gym Hero (1.97), City Cipher (0.95)

**What changed and why:** The rock profile reveals a major limitation - there is only one rock song in the catalog (Storm Runner), so it dominates at 3.99 while #2 and beyond drop sharply to under 2.0. The lofi profile had 3 matching songs, giving it a rich and coherent top-3. The rock user's #2 pick (Gym Hero) is a pop/intense song - it matches on mood and energy but not genre, earning less than half the score of #1. This illustrates how catalog size per genre directly determines recommendation quality. A rock fan using this system gets worse recommendations not because the algorithm is wrong, but because the data doesn't support them.

---

### High-Energy Pop vs. Deep Intense Rock

**High-Energy Pop** (`genre: pop, mood: happy, energy: 0.8`)
Top results: Sunrise City (3.98), Gym Hero (2.87), Rooftop Lights (1.96)

**Deep Intense Rock** (`genre: rock, mood: intense, energy: 0.9`)
Top results: Storm Runner (3.99), Gym Hero (1.97), City Cipher (0.95)

**What changed and why:** Interestingly, "Gym Hero" appears in both top-5 lists but for different reasons. For the pop profile it ranks #2 because of genre match; for the rock profile it ranks #2 because of mood + energy match. This is the same song surfacing for very different users - which in a real system could be a sign that the song is a useful "bridge" between audiences, or it could signal that the scoring is too coarse to distinguish between them. The energy levels are both high (0.8 vs 0.9), which means energy proximity rewards both profiles similarly for high-energy songs regardless of genre.

---

### High-Energy Pop vs. Adversarial - Sad but High Energy Classical

**High-Energy Pop** (`genre: pop, mood: happy, energy: 0.8`)
Top results: Sunrise City (3.98), Gym Hero (2.87), Rooftop Lights (1.96)

**Sad but High Energy Classical** (`genre: classical, mood: sad, energy: 0.9`)
Top results: Moonlight Sonata Redux (3.32), Requiem for a Tuesday (3.28), Storm Runner (0.99)

**What changed and why:** The high-energy pop profile gets songs that sound energetic and upbeat - which is exactly what you would expect. The classical/sad/high-energy profile is the interesting one. Even though the user asked for energy 0.9 (very high intensity), the system recommended two very slow, quiet piano pieces with energy values of 0.22 and 0.18. Why? Because genre and mood together award up to 3.0 points, but energy can only ever contribute 1.0 point at most. The math makes it impossible for a high-energy song to beat a genre/mood match, no matter how wrong the energy feels. Think of it like this: if you ask a music store clerk for "classical sad music," they will hand you quiet piano pieces - even if you specifically said you wanted something intense. The genre instruction overrides everything else.

---

### Chill Lofi vs. Adversarial - Underrepresented Genre (Jazz)

**Chill Lofi** (`genre: lofi, mood: chill, energy: 0.4`)
Top results: Midnight Coding (3.98), Library Rain (3.95), Focus Flow (3.00)

**Jazz / relaxed / energy 0.5** (`genre: jazz, mood: relaxed, energy: 0.5`)
Top results: Coffee Shop Stories (3.87), Golden Fields (1.94), Late Night Thoughts (0.98)

**What changed and why:** The lofi profile gets three strong recommendations because there are three lofi songs in the catalog. The jazz profile only gets one strong recommendation because there is only one jazz song. After Coffee Shop Stories, the system has nothing left in that genre, so it falls back to songs that happen to have similar energy levels - a country song, an r&b song, a pop song. From a user's perspective, the lofi fan and the jazz fan are equally specific about what they want. But the lofi fan gets a much better experience simply because the catalog was built with more of their music. This is an example of algorithmic unfairness caused by data imbalance, not bad logic.

---

## Overall Takeaway

The most consistent pattern across all six profiles: **genre match dominates, and catalog coverage determines quality**. A song that matches genre but nothing else still scores 2.0+, while a song that matches mood and has near-perfect energy but misses genre tops out around 1.96. The adversarial profiles made this even clearer - the system is structurally incapable of recommending across genre lines regardless of how conflicting the other preferences are. And when a genre has few songs in the catalog, the user silently gets a worse experience with no explanation. Both of these are real problems in production recommender systems, not just in this simulation.
