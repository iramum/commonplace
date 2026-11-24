# -*- coding: utf-8 -*-
"""Commonplace — synthetic demo data (portfolio version). “Oops, I wrote it again.”

Fictional writer “Nora Vale”, Medium publication “The Open Studio”.
Topic: contemporary art and curating — how young artists live, open calls, residencies,
prices, galleries. Every number, name, quote and title here is invented. Same JSON shape as the
real morning robot, so the app screens are reused one-to-one; “notes” is new (the commonplace book).

Run: python3 make_demo_data.py  -> data/latest.json
"""
import datetime as dt, json, math, os, random

random.seed(11)
TODAY = dt.date.today()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "latest.json")
PUB = "the-open-studio"


def d(days):
    return (TODAY + dt.timedelta(days=days)).isoformat()


def iso_week(date):
    y, w, _ = date.isocalendar()
    return f"{y}-W{w:02d}"


# ---------------------------------------------------------------- pieces (the “darlings”)
# (slug, title, type, published days ago, target key, shape)
# shape: work = steady with reads, grow = rising, wave = burst then fade, dead = gone quiet, new = just out
ARTS = [
    ("pricing-first-works", "How to Price Your First Artworks Without Underselling", "guide", 150, "how to price artwork", "work"),
    ("open-calls-rejected", "I Applied to 40 Open Calls. Here Is What the Rejections Taught Me", "essay", 132, "open call for artists", "work"),
    ("residency-real-cost", "The Real Cost of an Artist Residency, Line by Line", "data", 118, "artist residency cost", "wave"),
    ("artist-statement", "Writing an Artist Statement People Actually Read", "guide", 110, "artist statement examples", "grow"),
    ("gallery-commission", "Why Galleries Take 50% and What You Get for It", "guide", 104, "gallery commission", "work"),
    ("biennale-notes", "Notes From the Biennale: What Young Curators Look For", "essay", 98, "biennale 2026", "wave"),
    ("side-jobs-artists", "Side Jobs That Fund a Studio Practice", "data", 91, "jobs for artists", "grow"),
    ("art-fair-booth", "What an Art Fair Booth Really Costs a Young Gallery", "data", 85, "art fair booth cost", "wave"),
    ("studio-burnout", "Studio Burnout Looks Like Productivity", "essay", 79, "artist burnout", "dead"),
    ("instagram-artists", "Instagram Is Not Your Portfolio", "essay", 73, "instagram for artists", "dead"),
    ("curator-studio-visit", "How to Prepare for a Curator's Studio Visit", "guide", 67, "studio visit tips", "work"),
    ("grant-applications", "Grant Applications for Artists: A Plain Checklist", "guide", 60, "grants for artists", "grow"),
    ("shipping-artworks", "Shipping Artworks Abroad Without Losing Your Fee", "guide", 54, "shipping artwork internationally", "wave"),
    ("artist-run-spaces", "Artist-Run Spaces Are the New Galleries", "essay", 47, "artist run space", "dead"),
    ("consignment-contract", "The Consignment Contract, Clause by Clause", "guide", 41, "artist consignment agreement", "wave"),
    ("curating-without-institution", "Curating Without an Institution", "essay", 35, "independent curator", "grow"),
    ("portfolio-pdf", "The Portfolio PDF Curators Open to Page Two", "guide", 29, "artist portfolio pdf", "wave"),
    ("ai-images-artists", "AI Images and Young Artists: One Year of Data", "data", 22, "ai art artists income", "grow"),
    ("artist-taxes", "Taxes for Artists Selling Abroad, Plainly", "guide", 16, "artist taxes", "new"),
    ("collectors-2026", "Who Buys Emerging Art in 2026", "data", 11, "emerging art collectors", "new"),
    ("first-solo-show", "Negotiating Your First Solo Show", "guide", 6, "first solo exhibition", "new"),
    ("studio-routine", "My Studio Routine as a Painter With a Day Job", "essay", 2, "artist daily routine", "new"),
]
WEEKS = [TODAY - dt.timedelta(weeks=11 - i) for i in range(12)]


def series(shape, age_days):
    out = []
    for i, wk in enumerate(WEEKS):
        t = (age_days - (TODAY - wk).days) / 7
        if t < 0:
            out.append(0)
            continue
        base = {"work": 260 + 25 * math.sin(i), "wave": 520 * math.exp(-((t - 2.5) ** 2) / 3) + 25,
                "grow": 40 + 38 * t, "new": 120 + 160 * t, "dead": max(6, 300 * math.exp(-t / 1.6))}[shape]
        out.append(max(0, int(base * random.uniform(0.85, 1.15))))
    out[-1] = int(out[-1] * 0.45)   # current week is partial
    return out


articles = []
for slug, title, typ, ago, key, shape in ARTS:
    imp = series(shape, ago)
    rate = {"work": 0.11, "wave": 0.05, "grow": 0.07, "new": 0.06, "dead": 0.02}[shape]
    views, views_prev = sum(imp[-4:]), sum(imp[-8:-4])
    reads, reads_prev = int(views * rate * 3.2), int(views_prev * rate * 3.0)
    pos = round({"work": 4.2, "wave": 9.5, "grow": 7.8, "new": 12.4, "dead": 18.6}[shape] * random.uniform(.85, 1.15), 1)
    follows = max(0, int(reads * {"work": .05, "wave": .02, "grow": .04, "new": .03, "dead": .005}[shape]))
    articles.append({
        "slug": slug, "url": f"https://medium.com/{PUB}/{slug}", "live": True, "title": title, "keyword": key, "type": typ,
        "published": d(-ago), "modified": d(-9) if slug == "gallery-commission" else d(-ago),
        "gsc": {"clicks": reads, "impr": views, "pos": pos, "ctr": round(reads / views * 100, 1) if views else 0},
        "gsc_prev": {"clicks": reads_prev, "impr": views_prev, "pos": round(pos + random.uniform(-1.5, 2), 1)},
        "ga": {"sessions": int(reads * .4), "views": reads, "engaged_sec": int(reads * .4 * random.randint(150, 280)), "apply_clicks": follows},
        "ga_prev": {"sessions": int(reads_prev * .4), "apply_clicks": max(0, follows - random.randint(-3, 6))},
        "weekly": [[iso_week(w), int(v * rate), v] for w, v in zip(WEEKS, imp)], "fading": shape == "dead",
        "on_keyword": {"impr": int(views * .35), "pos": pos},
        "top_queries": [[key, int(reads * .3), int(views * .35), pos], [key + " 2026", int(reads * .08), int(views * .12), round(pos + 2.1, 1)],
                        ["how to " + key, int(reads * .05), int(views * .09), round(pos + 4.3, 1)]],
        "index": {"verdict": "PASS", "coverage": "Submitted and indexed", "last_crawl": d(-random.randint(1, 9))},
        "gsc_inspect_url": "https://search.google.com/search-console",
        "group": {"work": "A", "grow": "B", "wave": "C", "dead": "D", "new": "N"}[shape],
        "earnings": round(reads * .4 * random.uniform(.02, .05), 2),
    })
articles.sort(key=lambda a: (-a["gsc"]["clicks"], -a["gsc"]["impr"]))
A = {a["slug"]: a for a in articles}
A["instagram-artists"]["index"] = {"verdict": "NEUTRAL", "coverage": "Crawled - currently not indexed", "last_crawl": d(-40)}

alerts = [
    {"level": "high", "kind": "not_indexed", "slug": "instagram-artists", "text": "Not in the Google index: crawled, currently not indexed"},
    {"level": "high", "kind": "clicks_drop", "slug": "studio-burnout", "text": f"Views {A['studio-burnout']['gsc_prev']['impr']} → {A['studio-burnout']['gsc']['impr']} (28 days vs the 28 before)"},
    {"level": "mid", "kind": "fading", "slug": "artist-run-spaces", "text": "Fading: the last 2 weeks are under 35% of its peak"},
    {"level": "mid", "kind": "fading", "slug": "art-fair-booth", "text": "Fading after the fair season"},
    {"level": "win", "kind": "taking_off", "slug": "ai-images-artists", "text": f"{A['ai-images-artists']['gsc']['impr']} views in its first 3 weeks, reads up 3× this week"},
    {"level": "win", "kind": "taking_off", "slug": "artist-statement", "text": "Picked up by a Medium publication digest: reads doubled"},
    {"level": "win", "kind": "taking_off", "slug": "curating-without-institution", "text": "Top comment thread with 41 responses: follows up 5×"},
]
plan = [
    {"do": "Ask Google to index it again", "slug": "instagram-artists", "why": "Crawled, currently not indexed for 40 days", "action": "gsc"},
    {"do": "Find out why it dropped", "slug": "studio-burnout", "why": alerts[1]["text"], "action": "article"},
    {"do": "Rewrite the title for a search that already finds you", "slug": "artist-statement", "why": "“artist statement template”: 310 views at position 8, almost no reads", "action": "article"},
    {"do": "Answer the top comment and link a follow-up", "slug": "curating-without-institution", "why": "41 responses, 7 readers ask how to find a first venue", "action": "article"},
]
opportunities = [
    {"slug": "artist-statement", "query": "artist statement template", "impr": 310, "pos": 8.1},
    {"slug": "pricing-first-works", "query": "how much to charge for a painting", "impr": 182, "pos": 9.4},
    {"slug": "grant-applications", "query": "art grants for young artists", "impr": 160, "pos": 11.2},
    {"slug": "residency-real-cost", "query": "free artist residencies", "impr": 141, "pos": 7.7},
    {"slug": "portfolio-pdf", "query": "artist portfolio example", "impr": 96, "pos": 10.5},
]
rising = [
    {"query": "ai art and artists income", "impr": 420, "prev": 90, "pos": 9.6, "clicks": 31},
    {"query": "open call deadline december", "impr": 310, "prev": 40, "pos": 14.2, "clicks": 9},
    {"query": "artist taxes selling abroad", "impr": 180, "prev": 22, "pos": 12.8, "clicks": 6},
    {"query": "independent curator how to start", "impr": 150, "prev": 60, "pos": 6.1, "clicks": 18},
    {"query": "artist statement template", "impr": 310, "prev": 120, "pos": 8.1, "clicks": 4},
]

# ---------------------------------------------------------------- readers
personas = [
    {"id": "graduate", "name": "The fresh art-school graduate", "who": "Left the academy in the last 2 years, shares a studio, sells to friends", "weight": "core",
     "jtbd": "Turn a degree show into a practice that pays the rent", "pain": "No idea what to charge, which open calls are worth the fee",
     "evidence": "Pricing and open-call pieces bring 45% of follows", "loses_us": "Romantic essays with no numbers", "use_case": "Guides"},
    {"id": "daytime", "name": "The artist with a day job", "who": "Works 30 hours elsewhere, paints at night and on weekends", "weight": "core",
     "jtbd": "Keep making work without burning out", "pain": "Always tired, the studio turns into a second job",
     "evidence": "Longest read time; shares in private, rarely comments", "loses_us": "Hustle advice", "use_case": "Essays"},
    {"id": "curator", "name": "The independent curator", "who": "Curates without an institution: pop-ups, artist-run spaces, online shows", "weight": "core",
     "jtbd": "Put on a show with no budget and still pay the artists", "pain": "Venues, money and a CV that institutions take seriously",
     "evidence": "41 responses on one piece, the most saved highlights", "loses_us": "Pieces that ignore curators", "use_case": "Essays"},
    {"id": "gallerist", "name": "The young gallerist", "who": "Runs a small gallery for 1–4 years, weighs every fair", "weight": "occasional",
     "jtbd": "Decide which fair and which artists are worth the risk", "pain": "Booth costs and contracts eat the margin",
     "evidence": "Search waves around fair season, few follows", "loses_us": "Outdated cost lists", "use_case": "Data"},
    {"id": "collector", "name": "The first-time collector", "who": "Buys the first works under €3,000, unsure what is fair", "weight": "growing",
     "jtbd": "Buy without being fooled and support artists directly", "pain": "Prices feel random, galleries feel closed",
     "evidence": "Collector searches tripled in 28 days", "loses_us": "Insider jargon", "use_case": "Data"},
]
confirmed = [
    {"pain": "“How do I price my work?”", "apps": 38, "persona": "graduate", "verdict": "asked in comments under 7 pieces", "en": "price artwork"},
    {"pain": "“Which open calls are worth the entry fee?”", "apps": 29, "persona": "graduate", "verdict": "the most saved highlight on Medium", "en": "open call artists"},
    {"pain": "“How do I keep painting with a full-time job?”", "apps": 22, "persona": "daytime", "verdict": "a new piece just went out", "en": "artist daily routine day job"},
    {"pain": "“How do I curate my first show with no venue?”", "apps": 17, "persona": "curator", "verdict": "41 responses on one piece", "en": "independent curator"},
    {"pain": "“What should a first painting cost me as a buyer?”", "apps": 9, "persona": "collector", "verdict": "new this month", "en": "buy emerging art collectors"},
]
pain_map = [
    {"pain": p, "audience": a, "number": n, "what": "", "why_bank": w, "use_case": u, "rubric": "", "confidence": "High",
     "source_status": s, "status": "New", "source": "demo source", "url": None, "date": "2026"}
    for p, a, n, w, u, s in [
        ("Entry fees for open calls add up", "graduate", "€25–60 per call, 20+ calls a year (demo)", "Fees fund the organisers, not the artists", "Guides", "Verified"),
        ("Pricing by the hour", "graduate", "First prices often below the cost of materials (demo)", "No public price data for emerging artists", "Guides", "Verified"),
        ("Residencies that cost more than rent", "graduate", "Half of listed residencies charge a fee (demo)", "Free ones are oversubscribed", "Data", "Needs-source"),
        ("The second job eats the studio", "daytime", "8–12 studio hours a week (demo)", "No funding model for part-time practice", "Essays", "Verified"),
        ("No venue, no budget", "curator", "Most first shows happen in borrowed spaces (demo)", "Institutions look for a CV first", "Essays", "Verified"),
        ("Paying artists fairly", "curator", "Artist fees missing in many small shows (demo)", "Budgets go to rent and transport", "Guides", "Verified"),
        ("Booth costs", "gallerist", "A small booth costs as much as a year of rent (demo)", "Fairs price for big galleries", "Data", "Needs-source"),
        ("Consignment terms", "gallerist", "50/50 split is the default, little else is (demo)", "Contracts copied, not negotiated", "Guides", "Verified"),
        ("Prices feel random", "collector", "Same size, same year, 5× price gap (demo)", "Few public price lists", "Data", "Verified"),
    ]]

# ---------------------------------------------------------------- feeds (newsletters and open-call digests)
feeds = [
    {"id": "n1", "url": "https://example.com/digest/1", "date": d(-3), "text": "", "headlines": [
        "Survey: what emerging artists earned from sales in 2026", "Three city grants open for artists under 35",
        "A major fair cuts booth prices for galleries under five years old"]},
    {"id": "n2", "url": "https://example.com/digest/2", "date": d(-10), "text": "", "headlines": [
        "New residency map: 120 programmes without a fee", "Museums start paying exhibition fees to living artists"]},
]

# ---------------------------------------------------------------- notes (the commonplace book)
notes = [
    {"id": "n-01", "date": d(0), "source": "Studio visit", "text": "A curator spent 4 minutes on the walls and 20 on the sketchbooks. Show the process, not only the finished works.",
     "tags": ["studio visit", "portfolio"], "status": "seed", "link": None},
    {"id": "n-02", "date": d(-1), "source": "Overheard at an opening", "text": "“I priced it by what I would be sad to sell it for.” Best pricing rule I have heard this year.",
     "tags": ["pricing", "quote"], "status": "seed", "link": None},
    {"id": "n-03", "date": d(-2), "source": "Reading", "text": "Hyde's “The Gift”: art lives in two economies at once, the gift and the market. Every young artist is translating between them.",
     "tags": ["book", "money"], "status": "used", "link": "studio-routine"},
    {"id": "n-04", "date": d(-4), "source": "Comments", "text": "Seven readers asked the same thing under the curating piece: where do you find a first venue? That is the next piece.",
     "tags": ["curating", "readers"], "status": "idea", "link": "curating-without-institution"},
    {"id": "n-05", "date": d(-6), "source": "Exhibition", "text": "The best show this month had no wall texts at all. People talked to each other instead of reading.",
     "tags": ["exhibition", "curating"], "status": "seed", "link": None},
    {"id": "n-06", "date": d(-8), "source": "My numbers", "text": "Open calls this year: 40 sent, 3 accepted, €1,140 in fees. Half the fees went to calls I was never right for.",
     "tags": ["open calls", "money"], "status": "used", "link": "open-calls-rejected"},
    {"id": "n-07", "date": d(-11), "source": "Conversation", "text": "A gallerist: “We take 50% because we carry the risk of the next five shows, not this one.” Worth a follow-up.",
     "tags": ["gallery", "quote"], "status": "idea", "link": "gallery-commission"},
    {"id": "n-08", "date": d(-15), "source": "Idea", "text": "A piece written as a price list: what a first solo show actually costs, line by line, paid by whom.",
     "tags": ["solo show", "money"], "status": "used", "link": "first-solo-show"},
    {"id": "n-09", "date": d(-19), "source": "Walk", "text": "Artist-run spaces close because the founder burns out, not because nobody comes.",
     "tags": ["artist-run", "burnout"], "status": "seed", "link": None},
]

# ---------------------------------------------------------------- ideas
ideas = [
    {"source": "pain", "keyword": "price artwork", "cluster": "“How do I price my work?”", "audience": "graduate", "covered_by": "pricing-first-works",
     "why": "Asked 38 times in comments. A piece exists, so a new angle: when and how to raise prices", "score": 22},
    {"source": "pain", "keyword": "open call artists", "cluster": "“Which open calls are worth the entry fee?”", "audience": "graduate", "covered_by": "open-calls-rejected",
     "why": "29 questions. Follow-up: a short list of open calls with no fee, checked monthly", "score": 18},
    {"source": "pain", "keyword": "independent curator venue", "cluster": "“How do I curate my first show with no venue?”", "audience": "curator", "covered_by": None,
     "why": "17 questions and a note from the comments. No piece yet", "score": 17},
    {"source": "gsc", "keyword": "open call deadline december", "cluster": None, "audience": None, "why": "310 views in 28 days at position 14, no exact piece", "score": 15},
    {"source": "gsc", "keyword": "artist taxes selling abroad", "cluster": None, "audience": None, "why": "180 views, was 22. The new guide ranks 12th", "score": 9},
    {"source": "keys", "keyword": "artist statement template", "variants": ["artist statement examples for painters", "short artist statement"], "cluster": "Writing", "audience": "graduate",
     "why": "Search suggests 10 versions of this query; your piece explains, but gives no template", "score": 10},
    {"source": "keys", "keyword": "how to approach a gallery", "variants": ["email to a gallery template"], "cluster": "Galleries", "audience": "graduate",
     "why": "Search suggests 9 versions; no piece of yours answers it", "score": 9},
    {"source": "keys", "keyword": "how to start collecting art", "variants": ["buying art for the first time"], "cluster": "Collecting", "audience": "collector",
     "why": "Search suggests 7 versions; the collectors piece is data, not a how-to", "score": 7},
    {"source": "telegram", "keyword": None, "cluster": "Survey: what emerging artists earned from sales in 2026", "audience": None,
     "why": f"Digest, {d(-3)}", "url": "https://example.com/digest/1", "score": 3},
    {"source": "telegram", "keyword": None, "cluster": "Museums start paying exhibition fees to living artists", "audience": None,
     "why": f"Digest, {d(-10)}", "url": "https://example.com/digest/2", "score": 3},
    {"source": "painmap", "keyword": None, "cluster": "Paying artists fairly", "audience": "curator", "why": "Artist fees missing in many small shows (demo)", "use_case": "Guides", "score": 4},
    {"source": "painmap", "keyword": None, "cluster": "The second job eats the studio", "audience": "daytime", "why": "8–12 studio hours a week (demo)", "use_case": "Essays", "score": 4},
]

# ---------------------------------------------------------------- calendar
calendar = []
for a in articles:
    calendar.append({"date": a["published"], "kind": "article", "title": a["title"], "slug": a["slug"], "status": "Published"})
    if a["modified"] != a["published"]:
        calendar.append({"date": a["modified"], "kind": "article_upd", "title": a["title"], "slug": a["slug"], "status": "Updated"})
for off, t in [(3, "Where to Find a First Venue When You Curate Alone"), (8, "Raising Your Prices: The Email I Send to Collectors"), (15, "Open Calls With No Entry Fee, Checked Monthly")]:
    calendar.append({"date": d(off), "kind": "plan", "title": t, "status": "Planned", "overdue": False, "source": "workspace", "id": f"p{off}"})
calendar.append({"date": d(-2), "kind": "plan", "title": "What a Studio Visit Costs the Artist", "status": "Draft", "overdue": True, "source": "workspace", "id": "p-late"})
for off in range(-27, 15, 3):
    live = off <= 0
    calendar.append({"date": d(off), "kind": "ig_live" if live else "ig", "format": random.choice(["instagram", "threads", "linkedin"]),
                     "title": random.choice(["Carousel from", "Studio photo and quote from", "Thread from"]) + " " + random.choice(articles)["title"][:40],
                     "status": "Posted" if live else "Scheduled", "url": None})
calendar.sort(key=lambda e: e["date"])

# ---------------------------------------------------------------- keywords, research, queue, done
heads = ["artist residency", "open call", "artist statement", "art grants", "gallery commission", "art pricing", "independent curator",
         "art fair", "artist portfolio", "emerging art", "artist taxes", "studio visit"]
mods = ["", " 2026", " for young artists", " examples", " template", " tips", " cost", " europe", " application", " how to"]
keywords = []
for h in heads:
    for m in mods:
        q = (h + m).strip()
        art = next((a["slug"] for a in articles if a["keyword"] == q), None)
        im = random.choice([0, 0, 0, random.randint(10, 400)])
        keywords.append({"q": q, "cluster": h.title(), "intent": "Informational", "icp": random.choice([p["id"] for p in personas]),
                         "status": "Used" if art else "New", "suggest": str(random.randint(2, 10)), "verdict": "",
                         "impr": im, "clicks": int(im * .06), "pos": round(random.uniform(4, 30), 1) if im else None, "article": art})
research_docs = [
    {"title": "Readers' questions this quarter: what the comments ask", "date": d(-12), "author": "Nora Vale", "file": "research/readers-questions.md"},
    {"title": "Open calls 2026: fees, odds and who actually gets in", "date": d(-26), "author": "Nora Vale", "file": "research/open-calls-2026.md"},
]
reddit = [{"file": f"research/forums/{s}.md", "slug": s, "date": d(-random.randint(3, 60)), "questions": random.randint(9, 40), "failed": False}
          for s in ["pricing-art", "open-calls", "artist-residencies", "day-job-artists", "first-solo-show"]]
ai = [{"file": f"research/ai-questions/{s}.md", "slug": s, "date": d(-random.randint(3, 60)), "questions": random.randint(8, 30), "failed": False}
      for s in ["ai-and-artists", "artist-taxes", "independent-curating", "collecting-art"]]
audits = [{"file": "research/audits/monthly-review.md", "title": "Monthly review: which darlings live and which to let go", "date": d(-5)},
          {"file": "research/audits/search-check.md", "title": "Search check: titles that rank but nobody opens", "date": d(-19)}]
queue = [{"n": 23, "slug": "first-venue-curating", "status": "Draft ready, cover in review", "next": "Pick one of 3 covers, then publish to The Open Studio", "live": False}]
done = [{"date": d(-k), "msg": m} for k, m in [(0, "Published: My Studio Routine as a Painter With a Day Job"), (1, "Updated the gallery commission piece with a contract checklist"),
                                               (2, "Answered 14 comments on Curating Without an Institution"), (4, "Brief ready: where to find a first venue"),
                                               (5, "Monthly review: 3 darlings to refresh, 1 to let go")]]

groups = {}
for a in articles:
    groups[a["group"]] = groups.get(a["group"], 0) + 1
totals = {"live": len(articles),
          "clicks": sum(a["gsc"]["clicks"] for a in articles), "clicks_prev": sum(a["gsc_prev"]["clicks"] for a in articles),
          "impr": sum(a["gsc"]["impr"] for a in articles), "impr_prev": sum(a["gsc_prev"]["impr"] for a in articles),
          "sessions": sum(a["ga"]["sessions"] for a in articles), "sessions_prev": sum(a["ga_prev"]["sessions"] for a in articles),
          "apply_clicks": sum(a["ga"]["apply_clicks"] for a in articles), "apply_clicks_prev": sum(a["ga_prev"]["apply_clicks"] for a in articles),
          "earnings": round(sum(a["earnings"] for a in articles), 2), "groups": groups}

data = {
    "demo": True, "app": "Commonplace", "tagline": "Oops, I wrote it again.", "writer": "Nora Vale", "publication": "The Open Studio",
    "generated_at": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z", "gsc_last_day": d(-2), "site_last_published": d(-2),
    "totals": totals, "alerts": alerts, "plan": plan, "articles": articles, "opportunities": opportunities, "rising_queries": rising,
    "keywords": keywords, "queue": queue, "reddit": reddit, "ai": ai, "audits": audits, "done": done, "errors": [],
    "audiences": {"rule": "Write for the people who already read and follow: art-school graduates, artists with a day job and independent curators. Young gallerists and first-time collectors read occasionally, and collectors are growing.",
                  "personas": personas, "confirmed_pains": confirmed,
                  "content_not_offer": "Asked about, but not worth a piece yet: which brushes, which camera for artwork photos, studio lighting."},
    "pain_map": pain_map, "research_extra": {"docs": research_docs, "sections": [], "pains": [], "ideas": []},
    "telegram": feeds, "ideas": ideas, "notes": notes, "calendar": calendar,
    "calendar_notion": True, "calendar_ig": True, "stale_notion": 0,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(data, open(OUT, "w"), ensure_ascii=False, indent=1)
print("written", OUT, len(articles), "pieces,", len(notes), "notes,", len(calendar), "calendar events,", len(keywords), "keys")
