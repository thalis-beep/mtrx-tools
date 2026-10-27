#!/usr/bin/env python3
"""Estimate production credits from a storyboard JSON and recommend Plan A / Hybrid / B.

Usage:
  python3 estimate_credits.py plan.json [--balance 13187.72]

plan.json:
{
  "balance": 13187.72,                       # optional; --balance overrides
  "unit_costs": {                            # QUOTED costs (get_cost:true), never guessed
    "still": 0.5, "lock": 0.5,
    "clip": {"kling3_0_std_5": 6.25, "kling3_0_pro_5": 7.5}
  },
  "attempts": {"lock": 2.0, "still": 1.5, "simple": 1.5, "complex": 2.5},  # optional
  "locks": 6,                                # style tests + sheets + hero refs + product check
  "scenes": [
    {"id": "S01", "stills": 1, "clip": "kling3_0_pro_5", "complexity": "simple", "hero": true},
    {"id": "S02", "stills": 1, "clip": "kling3_0_std_5", "complexity": "complex"}
  ],
  "finishing": 0                             # upscales etc., quoted total
}
"""
import argparse
import json
import sys

DEFAULT_ATTEMPTS = {"lock": 2.0, "still": 1.5, "simple": 1.5, "complex": 2.5}


def estimate(plan):
    costs = plan["unit_costs"]
    attempts = {**DEFAULT_ATTEMPTS, **plan.get("attempts", {})}

    locks = plan.get("locks", 0) * costs.get("lock", costs["still"]) * attempts["lock"]
    stills = clips = hero = 0.0
    rows = []
    for s in plan["scenes"]:
        still_cost = s.get("stills", 1) * costs["still"] * attempts["still"]
        clip_cost = 0.0
        if s.get("clip"):
            if s["clip"] not in costs["clip"]:
                sys.exit(f"{s['id']}: no quoted cost for clip config '{s['clip']}'")
            clip_cost = costs["clip"][s["clip"]] * attempts[s.get("complexity", "simple")]
        stills += still_cost
        clips += clip_cost
        if s.get("hero"):
            hero += still_cost + clip_cost
        rows.append((s["id"], still_cost, clip_cost))

    finishing = plan.get("finishing", 0.0)
    total = locks + stills + clips + finishing
    return {"rows": rows, "locks": locks, "stills": stills, "clips": clips,
            "finishing": finishing, "hero": hero, "total": total}


def recommend(balance, r):
    if balance is None:
        return "UNKNOWN: read the balance (Higgsfield `balance`) or ask the user"
    if balance >= r["total"] * 1.2:
        return "Plan A"
    if balance >= r["total"]:
        return "Plan A (thin margin: use draft tiers, tell the user)"
    if balance >= r["locks"] + r["hero"]:
        return "Hybrid (Higgsfield for locks + hero/hard shots, external for the rest)"
    return "Plan B (or request a top-up)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--balance", type=float)
    args = ap.parse_args()

    with open(args.plan) as f:
        plan = json.load(f)
    balance = args.balance if args.balance is not None else plan.get("balance")
    r = estimate(plan)

    print(f"{'Scene':<8}{'Stills':>10}{'Clip':>10}")
    for sid, st, cl in r["rows"]:
        print(f"{sid:<8}{st:>10.2f}{cl:>10.2f}")
    print("-" * 28)
    for k in ("locks", "stills", "clips", "finishing"):
        print(f"{k.capitalize():<12}{r[k]:>10.2f}")
    print(f"{'TOTAL':<12}{r['total']:>10.2f}   (hero subset {r['hero']:.2f})")
    if balance is not None:
        print(f"Balance     {balance:>10.2f}   headroom x{balance / r['total']:.1f}"
              if r["total"] else f"Balance     {balance:>10.2f}")
    print(f"Recommendation: {recommend(balance, r)}")


if __name__ == "__main__":
    main()
