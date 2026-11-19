# trophy-forecast-01

Forecasts, for every Grand Theft Auto VI PlayStation 5 trophy, its earn rate on
[Exophase](https://www.exophase.com/game/grand-theft-auto-vi-psn/trophies/) at
2026-11-26T00:00Z as five quantiles, from the earn rates the house recorded
before 2026-11-21T11:30Z. Entry for the make.fun competition
[gta6-trophy-rarity-forecast-01](https://make.fun/c/gta6-trophy-rarity-forecast-01).

## How it works

`main.py` (Python 3.13, standard library only, no network) models what the
Exophase page prints — rate = earned players / players tracked:

1. **Players tracked** `P(t)`: a power law in time since launch,
   `log P = a + b·log(1+h)`, fit by least squares over the distinct refresh
   epochs of the case's history, extrapolated to the target. Slopes are
   anchored on observed launch-night growth (638 → 3,868 → 14,028 tracked
   players over the first 21 hours, Exophase).
2. **Earned players per trophy** `e_i(t)`: the implied earner count
   `rate_i·P/100` at each distinct-rate epoch, fit with the same power law
   where there is signal; near-automatic trophies (≥90%) are made to track the
   denominator; low-signal trophies grow with a prior slope.
3. **Forecast**: `100·e_i/P` at the target, quantiles at [0.05, 0.25, 0.5,
   0.75, 0.95] on the logit scale, spread from the fits' residuals plus a
   horizon term, floored so the forecast is never overconfident.

Local sanity scoring on approximate answers built from public snapshots halves
the starter (persistence) baseline's loss.

## License

MIT
