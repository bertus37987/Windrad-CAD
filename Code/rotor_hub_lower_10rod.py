""" Disclaimer, dieser code wurde generiert von Perplexity AI 2026, und überprüft von einem Python Developer"""
#!/usr/bin/env python3
"""
Rotor Hub — Lower Disc 10-Rod
pip install cadquery  →  python rotor_hub_lower_10rod.py
"""
import cadquery as cq
from cadquery import Vector
import math, os

os.makedirs("output", exist_ok=True)

# ── Parameters ──────────────────────────────────────────────
N    = 10        # number of rods
D    = 50.0       # disc diameter mm
H    =  8.0       # disc height mm
Rg   =  2.5       # groove radius mm
Rs   = 12.0       # groove inner start radius mm
Re   = 25.0       # groove outer end radius mm
Rscr = 18.0       # screw radial position mm
Dscr =  3.4       # M3 screw clearance Ø mm
theta  = 360.0 / N          # angular pitch between grooves
offset = theta / 2.0        # screw offset (between grooves)

def groove_cutter(angle_deg, at_z):
    L = Re - Rs
    cyl = (cq.Workplane("YZ").workplane(offset=Rs)
           .circle(Rg).extrude(L))
    s = cyl.val()
    s = s.translate(Vector(0.0, 0.0, at_z))
    s = s.rotate(Vector(0, 0, 0), Vector(0, 0, 1), angle_deg)
    return s

SW = 13.0; Hn = 6.0          # octagon nut recess

disc = cq.Workplane("XY").circle(D/2).extrude(H)

# 1. Semicircular grooves on TOP face
for i in range(N):
    disc = disc.cut(groove_cutter(i * theta, H))

# 2. Axial M3 screw through-holes (between grooves)
for i in range(N):
    ang = offset + i * theta
    x = Rscr * math.cos(math.radians(ang))
    y = Rscr * math.sin(math.radians(ang))
    disc = (disc.workplane(offset=H).center(x, y)
            .circle(Dscr/2).cutThruAll())

# 3. Octagonal blind recess on BOTTOM face (M8 shaft nut)
oct_d = (SW/2) / math.cos(math.pi/8) * 2
disc = (disc.faces("<Z").workplane()
        .polygon(8, oct_d).cutBlind(Hn))

print("Exporting...")
cq.exporters.export(disc, "output/rotor_hub_lower_10rod.stl")
cq.exporters.export(disc, "output/rotor_hub_lower_10rod.step")

bb  = disc.val().BoundingBox()
vol = disc.val().Volume()
print(f"Size : {bb.xmax-bb.xmin:.0f} x {bb.ymax-bb.ymin:.0f} x {bb.zmax-bb.zmin:.0f} mm")
print(f"Weight: ~{vol*1.24/1000:.1f} g PLA+")
print("Done → output/rotor_hub_lower_10rod.stl + .step")
