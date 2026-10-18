#!/usr/bin/env python3
"""
See and set when sketches go live.  All times are India time.

  python3 tools/schedule.py                       # show the schedule
  python3 tools/schedule.py 12 "2026-10-25 07:30" # sketch 12 goes live then
  python3 tools/schedule.py 12 now                # sketch 12 goes live on next publish
  python3 tools/schedule.py 12 draft              # take sketch 12 off the schedule
  python3 tools/schedule.py --auto --every 1d --at 07:00 [--from 2026-10-20] [--only-written] [--limit N]
        # give every draft a slot: one per day at 7 am, after the last scheduled one
        # --every accepts e.g. 1d, 2d, 7d, 12h ; --only-written skips sketches with no message yet
"""
import argparse, re, sys
from datetime import datetime, timedelta
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from musings_lib import all_musings, set_publish_on, parse_when, now, IST, MUSINGS

def show():
    n = now(); rows = all_musings()
    live = [m for m in rows if m["when"] and m["when"] <= n]
    sched = [m for m in rows if m["when"] and m["when"] > n]
    draft = [m for m in rows if not m["when"]]
    print(f"Now (India): {n:%a %d %b %Y %H:%M}\n")
    print(f"LIVE ({len(live)})  SCHEDULED ({len(sched)})  DRAFT ({len(draft)})\n")
    for m in sorted(sched, key=lambda m: m["when"]):
        label = m["caption"] or m["caption_en"] or "(no title)"
        msg = "" if m["has_message"] else "  ⚠ no message yet"
        print(f"  {m['order']:>3}  {m['when']:%a %d %b %Y %H:%M}  {label}{msg}")
    if draft:
        print(f"\nDrafts: {', '.join(str(m['order']) for m in draft)}")

def parse_every(s):
    m = re.fullmatch(r"(\d+)\s*([dh])", s.strip())
    if not m: sys.exit("--every looks like 1d, 2d, 7d or 12h")
    k = int(m.group(1)); return timedelta(days=k) if m.group(2) == "d" else timedelta(hours=k)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sketch", nargs="?"); ap.add_argument("when", nargs="?")
    ap.add_argument("--auto", action="store_true"); ap.add_argument("--every", default="1d")
    ap.add_argument("--at", default="07:00"); ap.add_argument("--from", dest="start")
    ap.add_argument("--only-written", action="store_true"); ap.add_argument("--limit", type=int)
    a = ap.parse_args()

    if a.auto:
        step = parse_every(a.every); rows = all_musings()
        hh, mm = map(int, a.at.split(":"))
        if a.start:
            nxt = parse_when(a.start)
            if len(a.start.strip()) == 10: nxt = nxt.replace(hour=hh, minute=mm)
        else:
            last = max([m["when"] for m in rows if m["when"]] + [now()])
            nxt = (last + step) if last > now() else (now() + timedelta(days=1)).replace(hour=hh, minute=mm, second=0, microsecond=0)
        todo = [m for m in rows if not m["when"] and (m["has_message"] or not a.only_written)]
        if a.limit: todo = todo[:a.limit]
        for m in todo:
            set_publish_on(m["path"], nxt); nxt += step
        print(f"Scheduled {len(todo)} sketch(es).\n"); show(); return

    if a.sketch:
        p = MUSINGS / f"{int(a.sketch):03d}.md"
        if not p.exists(): sys.exit(f"No sketch {a.sketch}")
        w = (a.when or "").strip().lower()
        if w == "draft": set_publish_on(p, None)
        elif w == "now": set_publish_on(p, now())
        else:
            when = parse_when(a.when)
            if not when: sys.exit('Use a date like 2026-10-25 or "2026-10-25 07:30"')
            set_publish_on(p, when)
        print(f"Sketch {a.sketch}: {'draft' if w == 'draft' else 'publish_on set'}\n")
    show()

if __name__ == "__main__":
    main()
