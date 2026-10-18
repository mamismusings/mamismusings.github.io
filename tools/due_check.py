#!/usr/bin/env python3
"""Used by the hourly GitHub Action: prints due=true if a sketch went live recently."""
import sys
from datetime import timedelta
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from musings_lib import all_musings, now

n = now()
due = any(m["when"] and n - timedelta(hours=3) < m["when"] <= n for m in all_musings())
print(f"due={'true' if due else 'false'}")
