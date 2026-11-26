# -*- coding: utf-8 -*-
"""Builds system.html, the Commonplace design system page, from the app itself.

The page reuses the exact <style> block and icon set of index.html, so every
token and component shown is the one the product runs on. Re-run after any
change to index.html:  python3 build_system.py
"""
import os, re

APP = open('index.html', encoding='utf-8').read()
STYLE = re.search(r'<style>(.*?)</style>', APP, re.S).group(1)
FONTS = re.search(r'<link href="(https://fonts\.googleapis\.com/css2[^"]+)"', APP).group(1)
ROOT = re.search(r':root\{(.*?)\}', STYLE, re.S).group(1)
VARS = dict(re.findall(r'--([\w-]+):\s*([^;]+);', ROOT))
ICONS = dict(re.findall(r"\n\s*(\w+):'(<[^']+)'", re.search(r'const ICON=\{(.*?)\};', APP, re.S).group(1)))
CAM = re.search(r"const CAM='(<svg[^']+)'", APP).group(1)

def ico(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[k]}</svg>'

COLOURS = [
    ('ink', 'Text, primary buttons'), ('ink2', 'Buttons, today, active chip'), ('body', 'Secondary text'),
    ('muted', 'Labels, hints'), ('line2', 'Borders'), ('line', 'Hairlines'), ('soft', 'Tiles, quiet fills'),
    ('yellow', 'Hers: published, badges, the comma'), ('yellow-pale', 'Her notes, planned'),
    ('green', 'Growth, links'), ('green-pale', 'Up, posted'), ('red', 'Only where she must act'), ('red-pale', 'Now'),
]
sw = ''.join(
    f'<div class="sw"><span class="chipc" style="background:{VARS[k].strip()}"></span><b>{k}</b><code>{VARS[k].strip()}</code><span>{role}</span></div>'
    for k, role in COLOURS)

NAMES = [('today', 'Today'), ('notes', 'Notes'), ('calendar', 'Calendar'), ('ideas', 'Ideas'), ('darlings', 'Darlings'), ('more', 'More')]
icons = ''.join(f'<div class="ic1">{ico(k)}<span>{l}</span></div>' for k, l in NAMES)
icons += f'<div class="ic1">{CAM.replace("<svg ", "<svg ")}<span>Add photo</span></div>'

days = ''.join(f'<button class="md {c}">{n}</button>' for n, c in
               [(23, 'miss'), (24, ''), (25, 'pub'), (26, 'today'), (27, ''), (28, 'plan'), (29, 'out')])

PAGE = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Commonplace, design system</title>
<link rel="icon" type="image/svg+xml" href="icon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{FONTS}" rel="stylesheet">
<style>
/* ---- the app's own stylesheet, copied verbatim by build_system.py ---- */
{STYLE}
/* ---- this page ---- */
body{{background:#fff}}
.sys{{max-width:1120px;margin:0 auto;padding:40px 24px 80px}}
.sys header{{display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid var(--line2);padding-bottom:24px;margin-bottom:8px}}
.sys header a.back{{font-size:13px;color:var(--body)}}
.sys section{{display:grid;grid-template-columns:220px minmax(0,1fr);gap:24px 40px;padding:40px 0;border-bottom:1px solid var(--line)}}
.sys section>h2{{font-size:26px}}
.sys section>h2 small{{display:block;font:400 13px var(--sans);color:var(--body);margin-top:8px;letter-spacing:0;line-height:1.5}}
.sys .bigh{{font-family:var(--display);font-size:64px;line-height:1;letter-spacing:-.03em;margin:28px 0 12px}}
.sys .intro{{font-size:17px;color:var(--body);max-width:680px;line-height:1.55;margin:0 0 8px}}
.pr{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}}
.pr div{{background:var(--soft);border-radius:4px;padding:16px 18px}}
.pr b{{display:block;font-family:var(--display);font-weight:500;font-size:19px;margin-bottom:4px}}
.pr span{{color:var(--body);font-size:13.5px}}
.sws{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}}
.sw{{display:grid;grid-template-columns:44px 1fr;column-gap:12px;align-items:center}}
.sw .chipc{{grid-row:span 3;width:44px;height:44px;border-radius:8px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}}
.sw b{{font-weight:600;font-size:13px}} .sw code{{font-size:12px;color:var(--body)}} .sw span{{font-size:12px;color:var(--muted)}}
.ty>div{{display:grid;grid-template-columns:170px minmax(0,1fr);gap:16px;align-items:baseline;padding:12px 0;border-bottom:1px solid var(--line)}}
.ty .k{{font-size:12px;color:var(--muted)}}
.spec{{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:18px}}
.spec+.cap,.cap{{font-size:12px;color:var(--muted);margin:-6px 0 22px}}
.icons{{display:flex;flex-wrap:wrap;gap:12px}}
.ic1{{width:96px;height:84px;border:1px solid var(--line2);border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;font-size:11px;color:var(--body)}}
.ic1 svg{{width:24px;height:24px;fill:none;stroke:var(--ink);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.barx{{display:flex;max-width:390px;border:1px solid var(--line2);border-radius:8px;padding:6px 4px}}
.barx button{{flex:1;border:0;background:none;padding:9px 2px 7px;color:var(--muted);display:flex;justify-content:center}}
.barx button.on{{color:var(--ink)}}
.barx .ic{{position:relative;display:block;width:24px;height:24px}}
.barx .ic svg{{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.barx button.on .ic svg{{stroke-width:2.1}}
.barx button.on .ic::after{{content:"";position:absolute;left:50%;bottom:-7px;width:4px;height:4px;margin-left:-2px;border-radius:50%;background:var(--ink)}}
.barx .b{{position:absolute;top:-5px;right:-9px;min-width:15px;height:15px;line-height:15px;padding:0 4px;font-size:9.5px;text-align:center;background:var(--yellow);border-radius:999px;font-weight:600;color:var(--ink)}}
.mini{{display:grid;grid-template-columns:repeat(7,40px);gap:4px}}
.toastx{{display:inline-block;background:var(--ink2);color:#fff;border-radius:999px;padding:10px 18px;font-size:13px}}
.dlgx{{background:rgba(25,25,25,.5);border-radius:8px;padding:28px;max-width:560px}}
.dlgx .dlg{{box-shadow:0 12px 48px rgba(0,0,0,.35)}}
.mark{{display:flex;gap:28px;align-items:center;flex-wrap:wrap}}
.mark img{{width:88px;height:88px;border-radius:20px}}
@media (max-width:760px){{.sys section{{grid-template-columns:1fr}}.pr{{grid-template-columns:1fr}}.ty>div{{grid-template-columns:1fr}}.sys .bigh{{font-size:44px}}}}
</style>
</head>
<body>
<main class="sys">
<header><a class="logo" href="index.html" aria-label="Commonplace"><span class="w">Common<span style="color:#FFC017">,</span>place</span><span class="t">Oops, I wrote it again.</span></a><a class="back" href="day.html">Back to the case</a></header>

<div class="bigh">Design system</div>
<p class="intro">Every colour, type style and component on this page is taken from the working prototype. The page is built from the app's own stylesheet, so nothing here is drawn separately.</p>

<section><h2>Principles</h2><div class="pr">
 <div><b>Calm like a reading app</b><span>White, hairlines, black pill buttons. The base is borrowed from Medium, where writers already feel at home.</span></div>
 <div><b>Yellow means hers</b><span>Her notes, her published pieces, her badges and the comma. Yellow is never a warning.</span></div>
 <div><b>Red only where she must act</b><span>A red number, never a red block. Green only where something grows.</span></div>
 <div><b>A count before a chart</b><span>Large serif numbers answer first. Detail sits one tap deeper.</span></div>
</div></section>

<section><h2>Colour<small>13 tokens, defined once in :root.</small></h2><div class="sws">{sw}</div></section>

<section><h2>Type<small>Free look-alikes of Medium's faces.</small></h2><div class="ty">
 <div><span class="k">Display, Newsreader 44</span><h1 style="margin:0">Good morning, Nora.</h1></div>
 <div><span class="k">Section, Newsreader 24</span><h2>Needs attention</h2></div>
 <div><span class="k">Number, Newsreader 52</span><div class="bn"><div class="v">3,114</div></div></div>
 <div><span class="k">Note, Source Serif 4, 21</span><p class="qnote" style="margin:0">“A curator spent 4 minutes on the walls and 20 on the sketchbooks.”</p></div>
 <div><span class="k">Interface, Inter 14</span><div>4 things on today’s list. 2 need you first.</div></div>
 <div><span class="k">Label, Inter 12</span><div style="font-size:12px;color:var(--body)">Reads, 28 days</div></div>
</div></section>

<section><h2>Buttons and links</h2><div>
 <div class="spec"><button class="btn">Save note</button><button class="btn o">Plan it</button><button class="btn sm">Write a piece</button><button class="btn sm o photo-btn">{CAM}Add photo</button><button class="btn g">Publish</button><button class="link">Related piece →</button><button class="corner">↗</button></div>
 <p class="cap">Pills, 36 px and 30 px. One filled button per group.</p>
</div></section>

<section><h2>Status pills and chips</h2><div>
 <div class="spec"><span class="pill r">Now</span><span class="pill yp">Today</span><span class="pill g">Up</span><span class="pill">Watch</span><span class="pill y">2</span><span class="pill k">Draft</span></div>
 <div class="spec"><button class="chip on">All (11)</button><button class="chip">Seeds (5)</button><button class="chip">Ideas (3)</button><button class="chip tg on">Pieces</button></div>
 <div class="spec"><div class="seg"><button class="on">All</button><button>Pieces</button><button>Social</button></div></div>
</div></section>

<section><h2>Numbers and tiles</h2><div>
 <div class="spec" style="gap:40px"><div class="bn"><div class="v">3,114</div><div class="l">Reads, 28 days</div><div class="d" style="color:var(--green)">+625</div></div><div class="bn"><div class="v">117</div><div class="l">New followers</div><div class="d" style="color:var(--green)">+15</div></div></div>
 <div class="t2" style="max-width:340px"><button><div class="k"><i></i>Needs you now</div><div class="v">2</div></button><button><div class="k"><i></i>Due this week</div><div class="v">1</div></button><button><div class="k"><i></i>Seeds to grow</div><div class="v">4</div></button><button class="miss"><div class="k"><i></i>Missed the date</div><div class="v">1</div></button></div>
 <p class="cap" style="margin-top:10px">The missed tile keeps the same grey as its neighbours. Only the number and the marker are red.</p>
</div></section>

<section><h2>Calendar days</h2><div>
 <div class="mini">{days}</div>
 <div class="mleg" style="margin-top:12px"><span><b style="background:#191919"></b>Today</span><span><b style="background:#FFC017"></b>Published</span><span><b style="box-shadow:inset 0 0 0 1.5px #FFC017"></b>Planned</span><span><b style="box-shadow:inset 0 0 0 1.5px #C94A4A"></b>Missed</span></div>
</div></section>

<section><h2>Cards</h2><div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px">
 <div class="c3"><div class="ch"><h3>To do</h3><button class="corner">↗</button></div><div class="todo" style="margin:0;border:0"><button class="row"><div class="g"><div class="t" style="font-size:14px">Ask Google to index it again</div><div class="m">Instagram Is Not Your Portfolio</div></div><span class="pill r">Now</span></button><button class="row"><div class="g"><div class="t" style="font-size:14px">Find out why it dropped</div><div class="m">Studio Burnout Looks Like Productivity</div></div><span class="pill yp">Today</span></button></div></div>
 <div class="c3" style="background:var(--yellow-pale);border-color:#F5E3A3"><div class="ch"><h3>Your latest note</h3><button class="corner">↗</button></div><div class="m" style="font-size:12px;color:#7A5A00">25 Nov, Studio visit</div><p class="qnote">“A curator spent 4 minutes on the walls and 20 on the sketchbooks.”</p><div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn sm">Write a piece</button><button class="btn sm o">Plan it</button></div></div>
</div></section>

<section><h2>Inputs</h2><div>
 <div class="composer" style="max-width:720px"><textarea placeholder="What did you notice today?"></textarea><div class="bar2"><select><option>Exhibition</option><option>Studio visit</option></select><input type="text" placeholder="tags, comma separated" style="flex:1;min-width:160px"><button class="btn sm o photo-btn">{CAM}Add photo</button><button class="btn sm">Save note</button></div></div>
 <p class="cap">One field, no title, no folder. Controls share one height and the pill shape. 16 px on phones so the page does not zoom.</p>
</div></section>

<section><h2>Icons<small>One line weight, 1.6, round joins. On the phone they replace text labels.</small></h2><div>
 <div class="icons">{icons}</div>
 <div class="barx" style="margin-top:20px"><button class="on"><span class="ic">{ico('today')}<span class="b">2</span></span></button><button><span class="ic">{ico('notes')}<span class="b">4</span></span></button><button><span class="ic">{ico('calendar')}</span></button><button><span class="ic">{ico('ideas')}</span></button><button><span class="ic">{ico('darlings')}</span></button><button><span class="ic">{ico('more')}</span></button></div>
 <p class="cap" style="margin-top:10px">Phone tab bar: badge on the icon, a dot under the open tab.</p>
</div></section>

<section><h2>Feedback</h2><div>
 <div class="spec"><span class="toastx">Saved to your notes</span><span class="toastx">Photo added to the note</span></div>
 <div class="dlgx"><div class="dlg" style="max-width:none"><h2 style="margin:0 0 4px">Plan a piece</h2><label>Title</label><input type="text" value="Which open calls are worth the entry fee?"><label>Publish on</label><input type="date" value="2026-11-28"><div style="display:flex;gap:8px;margin-top:16px"><button class="btn">Save</button><button class="btn o">Cancel</button></div></div></div>
 <p class="cap" style="margin-top:10px">Dialogs sit on a dark veil, so it is clear the page behind is paused.</p>
</div></section>

<section><h2>Logo</h2><div class="mark"><span class="logo"><span class="w" style="font-size:44px">Common<span style="color:#FFC017">,</span>place</span><span class="t" style="font-size:26px">Oops, I wrote it again.</span></span><img src="icon-180.png" alt="App icon: a yellow comma on black"></div></section>
</main>
</body>
</html>
'''
open('system.html.tmp', 'w', encoding='utf-8').write(PAGE)
os.replace('system.html.tmp', 'system.html')
print('system.html', len(PAGE), 'bytes,', len(VARS), 'tokens,', len(ICONS), 'icons')
