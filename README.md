# HEAVYPOLY for Blender

Custom operators, pie menus, and hotkeys designed for fast hard-surface modeling — built for pen tablet or mouse.

**Requires Blender 5.1+**

---

## Installation

Copy the `scripts/` folder into your Blender user config directory.

### Windows (Installed Blender)

```
C:\Users\YOURUSERNAME\AppData\Roaming\Blender Foundation\Blender\5.1\
```
> `AppData` may be hidden — enable "Show hidden items" in File Explorer, or use `%APPDATA%` in the Windows Run dialog.

### Windows (Portable Blender)

Place the `scripts/` folder inside a `portable/` folder next to `blender.exe`:

```
blender-folder/
  └─ portable/
      └─ scripts/
```

### macOS (Portable Blender)

Place `scripts/` inside `Blender.app/Contents/Resources/`.

---

After copying, open Blender and go to **Edit → Preferences → Add-ons**, search for **HEAVYPOLY**, and enable it.

---

## Addon Preferences

Open **Edit → Preferences → Add-ons → HEAVYPOLY** to configure:

| Setting | Description |
|---|---|
| **Auto-Apply Scale** | Smart Scale automatically applies scale after transform (destructive), a common need for those who set scale/dimensions in Object Mode. Disable for a non-destructive workflow. |
| **Enable Select Through** | Box and lasso smart selection in Edit Mode temporarily enables X-Ray so geometry behind faces is included. |
| **Pie Menu toggles** | Each of the 13 pie menus can be individually enabled or disabled. Changes take effect immediately and persist across restarts. |

---

## Pie Menus

| Hotkey | Menu | Contents |
|---|---|---|
| `Z` | **Shading** | Wireframe / Solid / Material / Rendered, overlays, isolate, bake lighting |
| `Space + Ctrl` | **Selection** | Select similar, linked, border; mode switching (Edit / Sculpt / Paint); parent/hierarchy ops |
| `Shift + A` *(Edit Mode)* | **Add** | Mesh primitives, curves, lights, Grease Pencil — face-aligned |
| `V` | **View** | Orthographic axes, camera view, walk navigation, new camera at view |
| `Shift + X` | **Symmetry** | Mirror on X/Y/Z, live mirror, symmetrize, clipping toggle |
| `Ctrl + B` | **Boolean** | Union, intersect, difference, slice, wrap; live booleans; cutter management |
| `Ctrl + Shift + D` | **Specials** | Radial duplicate, quick pipe, bridge, subdivide, crease, lattice, scatter/array |
| `Ctrl + Shift + Space` | **Pivots** | Individual / Median / Active / Cursor / Custom; normal vs global orientation |
| `Ctrl + S` | **Save** | Save, Save As, Open, New, Link, recent files |
| `Ctrl + Shift + S` | **Import/Export** | Alembic, FBX, OBJ, STL, image planes, append/link |
| `Shift + Tab` | **Areas** | Switch editor type (Timeline, Graph, UV, Shader, Outliner, Properties, Text, Console) |
| `Space + Ctrl + Alt` | **Rotate 90** | 90° rotations and axis-flatten on X/Y/Z |
| `1` | **Modifiers** | Quick access modifier menu |

---

## Smart Operators

Custom operators that replace or extend Blender's defaults with context-sensitive behavior.

**Selection** *(toolbar tools — activate from the left toolbar in Edit Mode)*
- **Select Through Box** — box select that temporarily enables X-Ray so all geometry at any depth is included. Sits in the toolbar after Blender's built-in Select Box. `LMB drag` SET · `Shift` ADD · `Ctrl` SUB
- **Select Through Lasso** — freehand lasso version of the above, same modifier conventions. Sits after Select Through Box in the toolbar.

Both tools are proper WorkspaceTools so they only intercept `LMB drag` when you have them active — the tweak tool is completely unaffected.

**Modeling**
- **Smart Extrude** `Shift + Space` — context-sensitive: extrude region for faces/edges, point extrude for verts, shrink-fatten after face extrude
- **Smart Bevel** `B` — vertex bevel in vert mode, border-to-edge bevel in face mode, standard edge bevel otherwise
- **Smart Delete** `X` — deletes verts in vert/edge mode, faces in face mode; in object mode handles cutters
- **Smart Scale** `S` — scales with auto-apply on single-user mesh objects (toggle in preferences)
- **Smart Shade Smooth** — shades smooth by angle (25°) using Blender 5.1's smooth-by-angle system
- **Push and Slide** `Shift + G` — vert slide in vert mode, edge slide in edge mode, shrink-fatten in face mode

**Origin / Cursor**
- **Smart Snap Cursor** `Ctrl + RMB` — snaps cursor to selection or world center when nothing is selected
- **Smart Snap Origin** `Ctrl + Shift + RMB` — sets origin to selection in edit mode, geometry center in object mode
- **Smart Snap Origin (Collection)** `Ctrl + Shift + Alt + RMB` — sets collection instance offset from cursor

**Object**
- **Separate and Select** `P` — separates selection and immediately selects and enters the new object; works for mesh, curve, and Grease Pencil
- **Subdivision Toggle** `Tab` *(Object Mode)* — toggles a Catmull-Clark Subsurf modifier (adds one at level 3 if none exists)
- **Camera Visibility / Wire** — hide objects from camera render while keeping them as wire guides; select all camera-hidden objects

**Draw**
- **Draw Primitives** `Ctrl + D` — freehand box, circle, or polyline drawing directly onto mesh surfaces with live boolean support

**Quick Pipe** *(from Specials pie)* — converts selected edges into a beveled curve pipe; drag to set depth, scroll wheel to set resolution

---

## Hotkey Philosophy

The keymap replaces Blender's defaults to keep common operations on single keys without modifiers:

- `Space` → Move (translate)
- `C` → Rotate
- `S` → Scale (Smart Scale)
- `X` → Delete (Smart Delete)
- `B` → Bevel
- `V` → View pie
- `Z` → Shading pie
- `Tab` → Subdivision toggle *(3D View / Edit Mode)*
- `D` → Redo last

Navigation uses Middle Mouse: `MMB` rotate, `Shift+MMB` pan, `Ctrl+MMB` zoom, `Ctrl+Shift+MMB` zoom to selected.
