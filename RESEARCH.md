# Research notes: observed Exophase GTA VI PS5 data points

Sources (named):
- House recorder (RULES.txt / NOTICE.txt): launch night reads.
  - 2026-11-18T23:50Z .. 2026-11-19T04:00Z: 638 players tracked, 943 trophies earned, flat rates.
  - 2026-11-19T04:30Z read (first refresh): 3,868 players tracked, 4,276 trophies earned; every rate but the 100% one lower than before.
- Live fetch of https://www.exophase.com/game/grand-theft-auto-vi-psn/trophies/ by this agent via web_extract, 2026-11-19 ~21:20Z:
  - 14,028 players tracked, 14,882 trophies earned, 4 in Platinum Club / 100% Club (platinum rate 0.03%).
  - Selected rates (percent, 2 decimals as printed):
    - id2 Just Like Paradise (first story beat): 99.99
    - id3 Paradise Lost (Chapter 1): 0.73  -> earned ~= 102
    - id4 Chapter 2: 0.14 -> earned ~= 20
    - id5 Chapter 3: 0.06 -> ~8
    - id6 Chapter 4: 0.06 -> ~8
    - id7 final mission: 0.06 -> ~8
    - id8 Breakfast Run: 0.24 -> ~34
    - id9 Cartel Heist: 0.06
    - id14 A Long Road (100%): 0.03
    - id15 Cunning Stunts (250 stunts): 0.03
    - id20 Baited My Tackle: 1.89 -> ~265
    - id21 Stick Fiddler: 0.41
    - id35 Whip It Good: 0.24
    - id36 Gunslinger: 0.06
  - Launch-night (638 players) rates for the same trophies from p00.in history:
    - id2: 100, id3: 1.25 (8 players), id4: 1.1 (7), id5: 1.1, id7: 1.1, id8: 1.1, id20: 2.04 (13),
      id21: 0.94 (6), id35: 1.25 (8), id36: 0.94, id14: 0.63 (4), id15: 0.63.

Implications for the model:
1. Players tracked grows fast and decelerating: 638 -> 3,868 (4.5h) -> 14,028 (~21.5h post-launch-week-start).
2. Earned counts for early story trophies grow too (ch1: 8 -> 102 players) but slower than the denominator, so the RATE falls: 1.25% -> 0.73%.
3. By 2026-11-26T00:00Z (target), tracked players will likely be a few times the 14k at 21h; the model must fit P(t) growth from the final history and extrapolate ~4.5 days.
4. Exophase refreshes counts in bursts every few hours; between refreshes the page is flat. The final history (10-min cadence through deadline) will show ~several refresh epochs, enough to fit per-trophy earned growth.
5. Rates print to 2 decimals, so at 14k players one earner moves the rate by ~0.007pp; quantization noise is modest.
6. Comparable-game context (public, named): GTA V (PSNProfiles) platinum 0.1% PSN / 2.06% PSNProfiles tracked; RDR2 platinum ~0.1% PSN / 2.58% PSNProfiles. Story-completion rates a week in are single-digit percent of the trophy-tracked population.
