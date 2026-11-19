"""Approximate local scorer for sanity checks only (not the real scorer).

Builds approximate answers for the practice cases by interpolating each
trophy's earned-player count (in log space) between the two real snapshots:
  - launch night: 638 players, rates from p00.in history (epoch h ~ 0.17)
  - 21:20Z fetch: 14,028 players, rates read live (h = 21.33)
then computes the contest's pinball loss on the logit scale.
Approximate: real answers come from the house's recorded reads.
"""

import json
import math

KIT = "/tmp/forecast-kit/gta6-trophy-rarity-forecast-01-kit"

# live fetch 2026-11-19T21:20Z (rates in trophy id order, id 1..55)
LIVE_P = 14028
LIVE_H = 21.33
LIVE_RATES = [
    0.03, 99.99, 0.73, 0.14, 0.06, 0.06, 0.06, 0.24, 0.06, 0.06, 0.06, 0.06,
    0.06, 0.03, 0.03, 0.04, 0.04, 0.03, 0.04, 1.89, 0.41, 0.04, 0.04, 0.04,
    0.03, 0.03, 0.04, 0.03, 0.04, 0.03, 0.03, 0.03, 0.09, 0.05, 0.24, 0.06,
    0.14, 0.14, 0.06, 0.04, 0.04, 0.04, 0.04, 0.08, 0.04, 0.09, 0.04, 0.05,
    0.04, 0.11, 0.06, 0.04, 0.05, 0.04, 0.04,
]
LAUNCH_H = 0.17  # the 638-player epoch, ~23:50Z Nov 18


def hours(iso):
    date, time = iso.rstrip("Z").split("T")
    y, mo, d = (int(x) for x in date.split("-"))
    hh, mm = int(time[:2]), int(time[3:5])
    ss = float(time[6:8]) if len(time) > 8 else 0.0
    return 24 * ((y - 2026) * 365 + (mo - 11) * 30 + (d - 19)
                 + (hh * 3600 + mm * 60 + ss) / 86400.0)


def logit(p):
    p = min(99.99, max(0.01, p))
    return math.log(p / (100 - p))


def approx_answer(case):
    h = hours(case["target"])
    # interpolate earned counts in log space between launch and live epochs
    ans = []
    for i in range(len(case["trophies"])):
        r_launch = case["history"][0]["rates"][i]
        e_launch = r_launch * 638 / 100.0
        e_live = LIVE_RATES[i] * LIVE_P / 100.0
        t = (math.log(1 + h) - math.log(1 + LAUNCH_H)) / (
            math.log(1 + LIVE_H) - math.log(1 + LAUNCH_H))
        t = min(max(t, 0.0), 1.0)
        if e_launch > 0 and e_live > 0:
            e = math.exp((1 - t) * math.log(e_launch) + t * math.log(e_live))
        else:
            e = 0.0
        # rate as the page would print it, 2 decimals; the 3,868-player refresh
        # held through the 05:00Z read (NOTICE.txt), the 14k live snapshot is later
        ans.append(round(100 * e / 3868, 2) if h < 5.5 else round(100 * e / LIVE_P, 2))
    return ans


def score(out_path, case, answer):
    out = json.load(open(out_path))
    total = 0.0
    items = 0
    for row, y in zip(out["trophies"], answer):
        for tau, q in zip(case["levels"], row["q"]):
            d = logit(y) - logit(q)
            total += 2 * max(tau * d, (tau - 1) * d)
            items += 1
    return total / items


def main():
    for cid in ["p00", "p01"]:
        case = json.load(open(f"{KIT}/input/{cid}.in"))
        ans = approx_answer(case)
        mine = score(f"out/{cid}.out", case, ans)
        import subprocess
        subprocess.run(["mkdir", "-p", "out-starter"], check=True)
        subprocess.run(
            ["python3", f"{KIT}/starter/main.py"],
            env={"MAKEFUN_INPUT_DIR": f"{KIT}/input",
                 "MAKEFUN_OUTPUT_DIR": "out-starter", "PATH": "/usr/bin:/bin"},
            check=True)
        base = score(f"out-starter/{cid}.out", case, ans)
        print(f"{cid}: mine={mine:.4f} starter={base:.4f}")


if __name__ == "__main__":
    main()
