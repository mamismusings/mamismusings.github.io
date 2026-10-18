# Mami's Musings · மாமியின் எண்ணங்கள்

Mami's pencil sketches, each with a short Tamil message.
Built with Jekyll and hosted free on GitHub Pages at **https://mamismusings.github.io**.

## How the site is laid out

```
_config.yml              site title (English + Tamil), description, URL
_musings/                ONE FILE PER SKETCH  ← this is where the Tamil text goes
  001.md, 002.md …
assets/images/sketches/  full-size sketches (sketch-001.jpg …)
assets/images/thumbs/    small copies for the gallery (made by the script)
_layouts/
  default.html           page frame: header, footer, Tamil fonts
  home.html              home page gallery grid
  musing.html            one sketch + its message, with previous/next links
_includes/head.html      <head>: title, Google Fonts (Noto Serif/Sans Tamil, Caveat)
assets/css/style.css     the "sketchbook on warm paper" look (light + dark)
about.md                 "மாமி பற்றி" (About Mami) page
tools/add_sketches.py    imports new photos from inbox/
tools/schedule.py        see / set when each sketch goes live
tools/preview.sh         run the site on this Mac
tools/publish.sh         import + commit + push in one go
tools/first_push.sh      one-time: connect this folder to GitHub
_plugins/scheduled_musings.rb   hides sketches whose publish_on hasn't arrived
.github/workflows/publish.yml   builds + deploys; runs hourly to release scheduled sketches
inbox/                   drop new WhatsApp photos here (not published)
```

## Writing a message

Open the sketch's file in `_musings/`, e.g. `_musings/001.md`:

```markdown
---
order: 1
publish_on: "2026-10-25 07:30"      # when it goes live (India time); empty = draft
image: /assets/images/sketches/sketch-001.jpg
thumb: /assets/images/thumbs/sketch-001.jpg
caption: "கடந்த காலத்தின் இசை"      # Tamil title (optional)
caption_en: "Melody From the Past"  # English title (optional)
---
பழைய கிராமபோன் இசை இன்னும் காதில் ஒலிக்கிறது…

ஒரு வெற்று வரி விட்டால் புதிய பத்தி தொடங்கும்.
```

Everything below the second `---` is the message: plain Tamil text, saved as UTF-8.
Leave a blank line between paragraphs. `order` controls the position in the gallery.
Sketches with no caption or message still show up, labelled "ஓவியம் N" (Sketch N).

## When a sketch goes live

Every sketch has a `publish_on:` line (India time):

| `publish_on:`          | Meaning                                   |
|------------------------|-------------------------------------------|
| *(empty)*              | Draft: never published                    |
| `2026-10-25`           | Goes live 25 Oct 2026 at midnight         |
| `"2026-10-25 07:30"`   | Goes live 25 Oct 2026 at 7:30 am          |

GitHub rebuilds the site every hour, so a sketch appears within about an hour of its time.

Edit the line by hand, or use the helper:

```bash
python3 tools/schedule.py                          # what's live, what's coming, what's draft
python3 tools/schedule.py 12 "2026-10-25 07:30"    # schedule sketch 12
python3 tools/schedule.py 12 now                   # publish sketch 12 on the next push
python3 tools/schedule.py 12 draft                 # unschedule it
python3 tools/schedule.py --auto --every 1d --at 07:00 --only-written
      # every draft that has a message gets a slot: one a day at 7 am,
      # continuing after the last scheduled sketch
```

Scheduling only changes the files; run `tools/publish.sh` to push the change to GitHub.

## Adding new sketches

```bash
python3 -m pip install pillow   # once
# copy the new photos into inbox/, then:
python3 tools/add_sketches.py
```

The script numbers them after the last sketch, makes thumbnails, moves exact
duplicates to `_duplicates/`, and creates `_musings/NNN.md` files (as drafts) for you to fill in.

## Preview on your Mac

One-time setup (macOS's built-in Ruby is too old):

```bash
brew install ruby
echo 'export PATH="$(brew --prefix ruby)/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
gem install bundler
```

Then, any time:

```bash
tools/preview.sh          # everything, incl. drafts + scheduled (labelled) → http://localhost:4000
tools/preview.sh --live   # exactly what the public site shows right now
```

The page reloads by itself when you save a file. Press Ctrl-C to stop.

## Publishing

**One time:**

1. In the `mamismusings` GitHub organization, create an **empty public** repository named
   `mamismusings.github.io` (no README, no licence).
2. Run `tools/first_push.sh`.
3. Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Repo → **Actions** tab → *Publish Mami's Musings* → **Run workflow** (or just push again).

**Every time after that:**

```bash
tools/publish.sh "Added 5 new sketches"
```

This imports anything in `inbox/`, shows the schedule, commits and pushes.
Sketches already scheduled go live on their own; you don't need to push again.

> GitHub pauses hourly workflows in a repo with no commits for 60 days. If the schedule
> runs further ahead than that, push any small change now and then, or press
> *Run workflow* → *Enable workflow* in the Actions tab if GitHub has paused it.
