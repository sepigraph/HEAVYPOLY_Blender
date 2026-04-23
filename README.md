# HEAVYPOLY for Blender 5.1

A comprehensive modeling addon built around a single principle: keep your hands on the mouse (or pen) and off the keyboard as much as possible. Designed for hard-surface work, it replaces Blender's default keymap with single-key shortcuts, adds a full suite of context-sensitive pie menus, and provides a set of smart operators that do the right thing based on what's selected.

**Requires Blender 5.1+**

---

## Installation

1. Copy the `scripts/` folder into your Blender user config directory.

   **Windows**
   ```
   C:\Users\<username>\AppData\Roaming\Blender Foundation\Blender\5.1\
   ```
   > `AppData` is hidden by default — use `%APPDATA%` in the Windows Run dialog (`Win+R`).

   **macOS**
   ```
   ~/Library/Application Support/Blender/5.1/
   ```

   **Portable Blender** — place the `scripts/` folder inside a `portable/` folder next to `blender.exe`.

2. Launch Blender, go to **Edit → Preferences → Add-ons**, search for **HEAVYPOLY**, and enable it.

---

## Preferences

**Edit → Preferences → Add-ons → HEAVYPOLY**

### Modeling
| Option | Description |
|---|---|
| Auto-Apply Scale | Smart Scale automatically applies scale after transforming a single-user mesh object. Disable for non-destructive workflows. |
| Tab — Subdivision Toggle | Tab toggles a Catmull-Clark Subsurf modifier instead of switching Edit Mode. Disable to restore Blender's default Tab behavior. |

### Selection
| Option | Description |
|---|---|
| Smart Select Through Tools | Box and lasso select in Edit Mode temporarily enable X-Ray so hidden geometry is included. |

### Panels
| Option | Description |
|---|---|
| HP Render Panel | Shows the HeavyPoly Render panel in the 3D View sidebar (N-panel → HeavyPoly tab). |

### Hotkeys
Each of these remapped keys can be disabled individually to restore Blender's defaults:

| Toggle | Key(s) | What it does |
|---|---|---|
| Double-Click Linked / Loop / Ring | LMB double-click, Alt+double-click | Select linked island, edge ring, or all loops |
| Scroll Select More / Less / Next / Prev | Shift+Wheel, Ctrl+Shift+Wheel | Grow/shrink selection or step to next/prev item |
| Alt-Click Loop Select | Alt+LMB, Alt+Shift+LMB | Select or extend an edge loop |
| Space = Move | Space | Translate in all contexts |
| C = Rotate | C | Rotate in all contexts |
| S = Smart Scale | S | Smart Scale in 3D View |
| D = Redo Last | D | Open Adjust Last Operation panel |

### Pie Menus
Each of the 13 pie menus can be individually toggled. Changes take effect immediately and persist across restarts.

---

## Pie Menus

| Hotkey | Menu | Contents |
|---|---|---|
| `Z` | **Shading** | Wireframe / Solid / Material / Rendered, overlays, isolate, render controls |
| `Ctrl+Space` | **Selection** | Select similar / linked / border; mode switching (Edit / Sculpt / Paint / GP); parent, join, hierarchy |
| `Shift+A` *(Edit Mode)* | **Add** | Mesh primitives, curves, lights, Grease Pencil — placed on the face under the cursor |
| `V` | **View** | Orthographic axes, camera, walk navigation, new camera from view |
| `Shift+X` | **Symmetry** | Mirror X/Y/Z, live mirror, symmetrize, bisect, clipping toggle |
| `Ctrl+B` | **Boolean** | Union, intersect, difference, slice, wrap; live booleans; cutter show/hide |
| `Ctrl+Shift+D` | **Specials** | Radial duplicate, Quick Pipe, bridge smooth, subdivide, crease, randomize, lattice, geo-node arrays, scatter |
| `Ctrl+Shift+Space` | **Pivots** | Individual Origins / Median / Active / Cursor / Custom; normal vs global orientation |
| `Ctrl+S` | **Save** | Save, Save As, Open, New, recent files |
| `Ctrl+Shift+S` | **Import/Export** | FBX, OBJ, STL, Alembic, USD, image plane, append/link |
| `Shift+Tab` | **Areas** | Switch editor type (Timeline, Graph Editor, UV, Shader, Outliner, Properties, Text, Console) |
| `Ctrl+Alt+Space` | **Rotate 90** | 90° rotations and axis-flatten on X/Y/Z |
| `1` | **Modifiers** | Mirror, Subdivision, Bevel, Solidify, Array, Screw, Shrinkwrap, Lattice, Weld, Decimate, Weighted Normal, Triangulate — plus Apply All and Remove All |

---

## Smart Operators

Context-sensitive operators that replace Blender's defaults with smarter behavior.

### Selection Tools *(left toolbar in Edit Mode)*
- **Select Through Box** `LMB drag` — box select with temporary X-Ray; hidden geometry is always included. `Shift` adds, `Ctrl` subtracts.
- **Select Through Lasso** — freehand version of the above.

### Modeling
| Operator | Hotkey | Behavior |
|---|---|---|
| Smart Extrude | `Shift+Space` | Extrude region for faces/edges; point-extrude for verts; shrink-fatten after face extrude |
| Smart Bevel | `B` | Vertex bevel in vert mode; border-to-edge bevel in face mode; edge bevel otherwise |
| Smart Delete | `X` | Deletes verts in vert/edge mode, faces in face mode; handles cutter objects in Object Mode |
| Smart Scale | `S` | Scales with auto-apply on single-user mesh objects |
| Smart Shade Smooth | *(Shading pie)* | Applies Smooth by Angle (25°) using Blender 5.1's node-based system |
| Push and Slide | `Shift+G` | Vert slide in vert mode; edge slide in edge mode; shrink-fatten in face mode |
| Subdivide Cylinder | *(Specials pie)* | Selects all edges and bevels at 25% offset to add loops to a cylinder |
| Randomize | *(Specials pie)* | Modal — drag mouse X to set intensity; click to confirm, Esc to cancel |

### Origin and Cursor
| Operator | Hotkey | Behavior |
|---|---|---|
| Smart Snap Cursor | `Ctrl+RMB` | Cursor to selection, or world center when nothing is selected |
| Smart Snap Origin | `Ctrl+Shift+RMB` | Origin to selection in Edit Mode; origin to geometry center in Object Mode |
| Smart Snap Origin (Collection) | `Ctrl+Shift+Alt+RMB` | Sets collection instance offset from the cursor |

### Object
| Operator | Hotkey | Behavior |
|---|---|---|
| Separate and Select | `P` | Separates selected geometry and immediately enters and selects the new object |
| Subdivision Toggle | `Tab` *(Object Mode)* | Toggles a Catmull-Clark Subsurf modifier; adds one at level 3 if none exists |
| Unhide and Keep Selection | `Ctrl+Shift+H` | Reveals hidden geometry without losing the current selection |

### Draw Primitives `Ctrl+D`
Freehand drawing mode that places mesh shapes directly onto surface geometry:
- `LMB drag` — draw shape
- `S` — cycle shape (Box / Circle / Polyline)
- `B` — cycle boolean mode (None / Subtract / Add / Wrap)
- `Shift` — thicken (Solidify)
- `Alt` — rotate
- `X` — toggle live boolean update
- `Space` — finish

---

## Object Utilities *(right-click context menu)*

Available in the 3D View right-click menu when objects are selected:

| Operator | Description |
|---|---|
| Hide From Camera (Wire Display) | Sets selected objects invisible to camera render and displays them as wireframe guides |
| Show in Camera (Textured Display) | Restores camera visibility and textured display |
| Select Hidden From Camera | Selects all geometry objects currently hidden from camera |
| Clean Unused Material Slots | Removes material slots not assigned to any faces on selected objects |
| Remove All Materials | Clears all material slots from selected objects |
| Backface Culling — All Materials | Enables backface culling on every material across all selected objects |
| Remove All Custom Properties | Deletes all custom properties from selected objects |

---

## HP Render Panel *(N-panel → HeavyPoly tab)*

A compact render control panel accessible in the 3D View sidebar. Can be toggled in preferences.

**Left column — Camera & Resolution**
- Active camera picker
- Resolution X / Y / %
- Resolution presets: `720p` `1080p` `1440p` `4K UHD` / `1K` `2K` `4K` `8K`
- Frame range and frame rate

**Right column — Output**
- View transform and color curve
- File format, color mode, bit depth
- Output format presets: `PNG RGBA` `EXR 32` `WEBP`
- Output path

---

## Hotkey Reference

| Key | Action |
|---|---|
| `Space` | Move (translate) |
| `C` | Rotate |
| `S` | Smart Scale |
| `X` | Smart Delete |
| `B` | Smart Bevel |
| `Tab` | Subdivision toggle *(3D View)* |
| `D` | Redo Last (Adjust Last Operation) |
| `V` | View pie |
| `Z` | Shading pie |
| `1` | Modifiers pie |
| `Shift+A` | Add pie *(Edit Mode)* |
| `Ctrl+B` | Boolean pie |
| `Ctrl+S` | Save pie |
| `Ctrl+Shift+S` | Import/Export pie |
| `Ctrl+Shift+D` | Specials pie |
| `Ctrl+Space` | Selection pie |
| `Ctrl+Shift+Space` | Pivots pie |
| `Shift+X` | Symmetry pie |
| `Shift+Tab` | Areas pie |
| `Ctrl+Alt+Space` | Rotate 90 pie |
| `Alt+LMB` | Loop select |
| `LMB double-click` | Select linked |
| `Alt+double-click` | Select ring |
| `Shift+Wheel` | Next / prev selection item |
| `Ctrl+Shift+Wheel` | Grow / shrink selection |
| `MMB` | Orbit |
| `Shift+MMB` | Pan |
| `Ctrl+MMB` | Zoom |
| `Ctrl+Shift+MMB` | Zoom to selected |
| `Ctrl+RMB` | Snap cursor |
| `Ctrl+Shift+RMB` | Snap origin |
