#!/usr/bin/env python3
"""Generate a crystallized / shattered-glass banner SVG for FiezDev.
Radial fracture facets (deterministic) behind crisp gold text."""
import math, random

W, H = 1280, 320
IMPACT = (640, 150)          # fracture origin (behind the name)
N = 18                       # radial spokes
RINGS = [0, 64, 140, 245, 405, 720]   # ring radii (outer covers corners)
random.seed(7)               # deterministic

# --- build a shared vertex grid pt[i][j] so facets tessellate w/o gaps ---
pts = []
for i in range(N):
    base_t = i * 2 * math.pi / N
    col = []
    for j, r in enumerate(RINGS):
        if r == 0:
            col.append(IMPACT)
            continue
        band = RINGS[j] - RINGS[j-1]
        tj = base_t + random.uniform(-1, 1) * (math.pi / N) * 0.5
        rj = r + random.uniform(-1, 1) * band * 0.22
        x = IMPACT[0] + rj * math.cos(tj)
        y = IMPACT[1] + rj * math.sin(tj)
        col.append((x, y))
    pts.append(col)

# --- facet fill palette: dark glassy teals, a few brighter "crystal" glints ---
DARK = ['#0d141a', '#101a20', '#142029', '#182530', '#1d2c37', '#0a1014', '#12202a']
GLINT = ['#273a47', '#2f4655', '#35505f']   # rarer, catch the light

def facet_fill(j):
    # inner rings slightly more varied; ~12% chance of a bright glint shard
    if random.random() < 0.12:
        return random.choice(GLINT), round(random.uniform(0.55, 0.8), 2)
    return random.choice(DARK), round(random.uniform(0.82, 1.0), 2)

def fnum(v):
    return f'{v:.1f}'

polys = []
for i in range(N):
    ni = (i + 1) % N
    for j in range(len(RINGS) - 1):
        if j == 0:  # inner triangles from impact
            quad = [pts[i][1], pts[ni][1], IMPACT]
        else:
            quad = [pts[i][j], pts[ni][j], pts[ni][j+1], pts[i][j+1]]
        ptsattr = ' '.join(f'{fnum(x)},{fnum(y)}' for x, y in quad)
        fill, op = facet_fill(j)
        # crack edges: alternate gold + icy, thin & faint
        if random.random() < 0.5:
            stroke, sop = '#fbbf24', round(random.uniform(0.10, 0.22), 2)
        else:
            stroke, sop = '#9fc2d6', round(random.uniform(0.08, 0.16), 2)
        sw = round(random.uniform(0.8, 1.5), 1)
        polys.append(
            f'<polygon points="{ptsattr}" fill="{fill}" fill-opacity="{op}" '
            f'stroke="{stroke}" stroke-opacity="{sop}" stroke-width="{sw}"/>'
        )

# --- a few long dramatic radial cracks from the impact point ---
cracks = []
for k in range(5):
    ang = random.uniform(0, 2 * math.pi)
    length = random.uniform(420, 760)
    ex = IMPACT[0] + length * math.cos(ang)
    ey = IMPACT[1] + length * math.sin(ang)
    col = '#fbbf24' if k % 2 == 0 else '#bcd6e6'
    op = round(random.uniform(0.12, 0.24), 2)
    cracks.append(
        f'<line x1="{IMPACT[0]}" y1="{IMPACT[1]}" x2="{fnum(ex)}" y2="{fnum(ey)}" '
        f'stroke="{col}" stroke-opacity="{op}" stroke-width="1"/>'
    )

FF = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
shatter = '\n    '.join(polys)
crack_lines = '\n    '.join(cracks)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Ittipol Vongapai — FiezDev. Passionate to make the remarkable thing.">
  <defs>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#eab308"/>
      <stop offset="0.5" stop-color="#fbbf24"/>
      <stop offset="1" stop-color="#ca8a04"/>
    </linearGradient>
    <linearGradient id="goldMotto" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ca8a04"/>
      <stop offset="0.5" stop-color="#f59e0b"/>
      <stop offset="1" stop-color="#ca8a04"/>
    </linearGradient>
    <linearGradient id="ridge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ca8a04" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#fbbf24" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#ca8a04" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="impactGlow" cx="{IMPACT[0]/W:.3f}" cy="{IMPACT[1]/H:.3f}" r="0.5">
      <stop offset="0" stop-color="#3a5566" stop-opacity="0.55"/>
      <stop offset="0.5" stop-color="#1b2832" stop-opacity="0.15"/>
      <stop offset="1" stop-color="#0b1014" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="textVeil" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#0c1216" stop-opacity="0.82"/>
      <stop offset="0.62" stop-color="#0c1216" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#0c1216" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>
  </defs>

  <!-- darkest base so any seam reads as deep glass -->
  <rect width="{W}" height="{H}" fill="#0a0f13"/>

  <!-- shattered / crystallized glass facets -->
  <g clip-path="url(#frame)">
    {shatter}
    <!-- impact glow -->
    <rect width="{W}" height="{H}" fill="url(#impactGlow)"/>
    <!-- long radial cracks -->
    {crack_lines}
  </g>

  <!-- legibility veil behind the text block -->
  <ellipse cx="{IMPACT[0]}" cy="160" rx="470" ry="120" fill="url(#textVeil)"/>

  <!-- crown peak above the name -->
  <path d="M 624 60 L 640 36 L 656 60 L 648 60 L 640 48 L 632 60 Z" fill="url(#gold)" opacity="0.95"/>

  <!-- handle -->
  <text font-family="{FF}" x="640" y="92" text-anchor="middle" font-size="22" font-weight="700"
        letter-spacing="9" fill="url(#gold)" opacity="0.92">F I E Z D E V</text>

  <!-- name -->
  <text font-family="{FF}" x="640" y="170" text-anchor="middle" font-size="68" font-weight="700"
        letter-spacing="3" fill="url(#gold)">ITTIPOL VONGAPAI</text>

  <!-- gold divider -->
  <rect x="455" y="192" width="370" height="2" rx="1" fill="url(#ridge)"/>

  <!-- domains -->
  <text font-family="{FF}" x="640" y="228" text-anchor="middle" font-size="19" font-weight="600"
        letter-spacing="6" fill="#b9c9d4">WEB&#160;&#160;·&#160;&#160;AI&#160;&#160;·&#160;&#160;AGENTS&#160;&#160;·&#160;&#160;AUTOMATION</text>

  <!-- motto -->
  <text font-family="{FF}" x="640" y="276" text-anchor="middle" font-size="16" font-weight="600"
        letter-spacing="5" fill="url(#goldMotto)" opacity="0.95">PASSIONATE TO MAKE THE REMARKABLE THING</text>
</svg>
'''

out = '/Users/fiez/Dev/FiezDev/assets/banner.svg'
open(out, 'w').write(svg)
print(f'wrote {out}  ({len(svg)} bytes, {len(polys)} facets, {len(cracks)} cracks)')
