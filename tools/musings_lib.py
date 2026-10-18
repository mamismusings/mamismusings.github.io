"""Shared helpers for reading/writing publish_on in _musings/*.md."""
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
ROOT = Path(__file__).resolve().parent.parent
MUSINGS = ROOT / "_musings"

def front_matter(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""

def field(fm, name):
    m = re.search(rf"^{name}:[ \t]*(.*?)[ \t]*(#.*)?$", fm, re.M)
    if not m: return ""
    return m.group(1).strip().strip('"').strip("'")

def parse_when(s):
    """'2026-10-25' or '2026-10-25 07:30' (India time) -> aware datetime, or None."""
    s = (s or "").strip().strip('"').strip("'")
    if not s: return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try: return datetime.strptime(s, fmt).replace(tzinfo=IST)
        except ValueError: pass
    try:
        d = datetime.fromisoformat(s)
        return d if d.tzinfo else d.replace(tzinfo=IST)
    except ValueError:
        return None

def all_musings():
    out = []
    for p in sorted(MUSINGS.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        fm = front_matter(text)
        body = text.split("---", 2)[2] if text.count("---") >= 2 else ""
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S).strip()
        out.append(dict(path=p, order=int(field(fm, "order") or 0), caption=field(fm, "caption"),
                        caption_en=field(fm, "caption_en"), when=parse_when(field(fm, "publish_on")),
                        raw_when=field(fm, "publish_on"), has_message=bool(body)))
    return sorted(out, key=lambda m: m["order"])

def set_publish_on(path, when):
    text = path.read_text(encoding="utf-8")
    value = f'"{when.strftime("%Y-%m-%d %H:%M")}"' if when else ""
    line = f"publish_on: {value}".rstrip()
    if re.search(r"^publish_on:.*$", text, re.M):
        text = re.sub(r"^publish_on:.*$", line, text, count=1, flags=re.M)
    else:
        text = text.replace("---\n", f"---\n", 1)
        text = re.sub(r"^(order:.*)$", rf"\1\n{line}", text, count=1, flags=re.M)
    path.write_text(text, encoding="utf-8")

def now():
    return datetime.now(IST)
