""" Disclaimer, dieser code wurde generiert von Perplexity AI 2026, und überprüft von einem Python Developer"""
import trimesh
import numpy as np

# ── Parameter ────────────────────────────────────────────────────────────────
qw, qd, qh = 16.0, 10.0, 22.0    # Quader-Maße
rohr_r_i   = 2.6                 # Innen Ø5.2mm (für 5mm Stab)
rohr_r_o   = 5.0                 # Außen Ø10mm
rohr_h     = 16.0                # Rohrlänge
slot_w     = 3.2                 # Blattschlitz-Breite
sr         = 1.6                 # M3-Schraubenradius

# ── Quader mit DURCHGEHENDEM Schlitz (zwei Arme) ─────────────────────────────
# Erstellt einen 16x10x22 Block und schneidet einen 3.2mm Schlitz komplett durch
quader = trimesh.creation.box(extents=[qw, qd, qh])
quader.apply_translation([0, 0, qh / 2])

# Schlitz geht KOMPLETT durch (z: 0 → qh), erzeugt zwei Klemmarme
slot = trimesh.creation.box(extents=[qw + 2, slot_w, qh + 2])
slot.apply_translation([0, 0, qh / 2])

# M3-Schraube Blatt (Y-Richtung, mittig in Z der Arme)
sc_blade = trimesh.creation.cylinder(radius=sr, height=qd + 2, sections=16)
sc_blade.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
sc_blade.apply_translation([0, 0, qh * 0.4])

quader = trimesh.boolean.difference([quader, slot, sc_blade], engine='manifold')

# ── Rohr (hängt unten raus) ───────────────────────────────────────────────────
rohr_out = trimesh.creation.cylinder(radius=rohr_r_o, height=rohr_h, sections=40)
rohr_out.apply_translation([0, 0, -rohr_h / 2])

rohr_in = trimesh.creation.cylinder(radius=rohr_r_i, height=rohr_h + 2, sections=40)
rohr_in.apply_translation([0, 0, -rohr_h / 2])

# M3-Schraube Stab (Y-Richtung)
sc_stab = trimesh.creation.cylinder(radius=sr, height=rohr_r_o * 2 + 2, sections=16)
sc_stab.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
sc_stab.apply_translation([0, 0, -rohr_h * 0.65])

rohr = trimesh.boolean.difference([rohr_out, rohr_in, sc_stab], engine='manifold')

# ── Vereinigen ────────────────────────────────────────────────────────────────
result = trimesh.boolean.union([quader, rohr], engine='manifold')

# Export
result.export("blatthalter_final.stl")
print("STL wurde erstellt: blatthalter_final.stl")
