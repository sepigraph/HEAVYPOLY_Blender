import bpy
from bpy.props import BoolProperty


# Maps preference attribute → pie menu class name used in keymap properties
PREF_PIE_MAP = {
    'pie_shading':    'HP_MT_pie_shading',
    'pie_selection':  'HP_MT_pie_select',
    'pie_add':        'HP_MT_pie_add',
    'pie_view':       'HP_MT_pie_view',
    'pie_symmetry':   'HP_MT_pie_symmetry',
    'pie_boolean':    'HP_MT_pie_boolean',
    'pie_specials':   'HP_MT_pie_specials',
    'pie_pivots':     'HP_MT_pie_pivots',
    'pie_save':       'HP_MT_pie_save',
    'pie_import':     'HP_MT_pie_importexport',
    'pie_areas':      'HP_MT_pie_areas',
    'pie_rotate90':   'HP_MT_pie_rotate90',
    'pie_modifiers':  'HP_MT_pie_modifiers',
}

# Blender default keymap items that HEAVYPOLY explicitly disables per pie.
# When a pie is toggled off these are re-enabled; toggled on they are disabled.
# Format: (keymap_name, operator_idname, type, value, shift, ctrl, alt)
CONFLICT_MAP = {
    'pie_view': [
        # V in Sculpt (brush_select) was explicitly disabled to free V for the View pie.
        ('Sculpt', 'paint.brush_select', 'V', 'PRESS', False, False, False),
    ],
}


def get_prefs():
    addon = bpy.context.preferences.addons.get(__package__ or '')
    return addon.preferences if addon else None


def _set_blender_kmi_active(km_name, idname, type, value, shift, ctrl, alt, active):
    kc = bpy.context.window_manager.keyconfigs.get('Blender')
    if not kc:
        return
    km = kc.keymaps.get(km_name)
    if not km:
        return
    for kmi in km.keymap_items:
        if (kmi.idname == idname and kmi.type == type and kmi.value == value
                and kmi.shift == shift and kmi.ctrl == ctrl and kmi.alt == alt):
            kmi.active = active
            return


def _set_pie_active(pie_menu_name, active, pref_attr=None):
    kc = bpy.context.window_manager.keyconfigs.addon
    if not kc:
        return
    for km in kc.keymaps:
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu_pie':
                try:
                    if kmi.properties.name == pie_menu_name:
                        kmi.active = active
                except Exception:
                    pass
    # Restore (or suppress) conflicting Blender defaults alongside the pie.
    if pref_attr and pref_attr in CONFLICT_MAP:
        for conflict in CONFLICT_MAP[pref_attr]:
            km_name, idname, type_, value, shift, ctrl, alt = conflict
            _set_blender_kmi_active(km_name, idname, type_, value, shift, ctrl, alt, not active)


def _pie_toggle(pref_attr, menu_name):
    def update(self, context):
        _set_pie_active(menu_name, getattr(self, pref_attr), pref_attr)
    return update


def _set_tab_subsurf_active(active):
    kc = bpy.context.window_manager.keyconfigs.addon
    if not kc:
        return
    for km in kc.keymaps:
        for kmi in km.keymap_items:
            if kmi.idname == 'view3d.subdivision_toggle':
                kmi.active = active


def _tab_subsurf_update(self, context):
    _set_tab_subsurf_active(self.tab_subsurf)


class HP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    # ── Modeling ─────────────────────────────────────────────────────────────
    smart_scale_apply: BoolProperty(
        name="Auto-Apply Scale",
        description=(
            "After Smart Scale, automatically apply scale (destructive). "
            "Disable for a non-destructive workflow"
        ),
        default=True,
    )

    tab_subsurf: BoolProperty(
        name="Tab — Subdivision Toggle",
        description=(
            "Tab toggles a Catmull-Clark Subsurf modifier in Object and Edit Mode. "
            "Disable to restore Blender's default Tab (Edit Mode toggle)"
        ),
        default=True,
        update=_tab_subsurf_update,
    )

    # ── Selection ─────────────────────────────────────────────────────────────
    select_through_enabled: BoolProperty(
        name="Smart Select Through Tools",
        description=(
            "Box and lasso selection in Edit Mode temporarily enables X-Ray "
            "so geometry behind other faces is included"
        ),
        default=True,
    )

    # ── Pie Menus ─────────────────────────────────────────────────────────────
    pie_shading: BoolProperty(
        name="Shading Pie  [Z — 3D View]",
        default=True,
        update=_pie_toggle('pie_shading', 'HP_MT_pie_shading'),
    )
    pie_selection: BoolProperty(
        name="Selection Pie  [Space+Ctrl — 3D View]",
        default=True,
        update=_pie_toggle('pie_selection', 'HP_MT_pie_select'),
    )
    pie_add: BoolProperty(
        name="Add Pie  [Shift+A — Edit Mode]",
        default=True,
        update=_pie_toggle('pie_add', 'HP_MT_pie_add'),
    )
    pie_view: BoolProperty(
        name="View Pie  [V — 3D View + Sculpt]",
        default=True,
        update=_pie_toggle('pie_view', 'HP_MT_pie_view'),
    )
    pie_symmetry: BoolProperty(
        name="Symmetry Pie  [Shift+X — 3D View]",
        default=True,
        update=_pie_toggle('pie_symmetry', 'HP_MT_pie_symmetry'),
    )
    pie_boolean: BoolProperty(
        name="Boolean Pie  [Ctrl+B — 3D View]",
        default=True,
        update=_pie_toggle('pie_boolean', 'HP_MT_pie_boolean'),
    )
    pie_specials: BoolProperty(
        name="Specials Pie  [Ctrl+Shift+D — 3D View]",
        default=True,
        update=_pie_toggle('pie_specials', 'HP_MT_pie_specials'),
    )
    pie_pivots: BoolProperty(
        name="Pivots Pie  [Space+Ctrl+Shift — 3D View]",
        default=True,
        update=_pie_toggle('pie_pivots', 'HP_MT_pie_pivots'),
    )
    pie_save: BoolProperty(
        name="Save Pie  [Ctrl+S — Global]",
        default=True,
        update=_pie_toggle('pie_save', 'HP_MT_pie_save'),
    )
    pie_import: BoolProperty(
        name="Import/Export Pie  [Ctrl+Shift+S — Global]",
        default=True,
        update=_pie_toggle('pie_import', 'HP_MT_pie_importexport'),
    )
    pie_areas: BoolProperty(
        name="Areas Pie  [Shift+Tab — Global]",
        default=True,
        update=_pie_toggle('pie_areas', 'HP_MT_pie_areas'),
    )
    pie_rotate90: BoolProperty(
        name="Rotate 90 Pie  [Space+Ctrl+Alt — 3D View]",
        default=True,
        update=_pie_toggle('pie_rotate90', 'HP_MT_pie_rotate90'),
    )
    pie_modifiers: BoolProperty(
        name="Modifiers Pie  [1 — 3D View]",
        default=True,
        update=_pie_toggle('pie_modifiers', 'HP_MT_pie_modifiers'),
    )

    def draw(self, context):
        layout = self.layout

        # Modeling
        box = layout.box()
        box.label(text="Modeling", icon='MESH_DATA')
        box.prop(self, 'smart_scale_apply')
        box.prop(self, 'tab_subsurf')

        # Selection
        box = layout.box()
        box.label(text="Selection", icon='RESTRICT_SELECT_OFF')
        box.prop(self, 'select_through_enabled')

        # Pie Menus
        box = layout.box()
        box.label(text="Pie Menus", icon='MESH_CIRCLE')
        flow = box.grid_flow(columns=2, even_columns=True, align=True)
        for attr in PREF_PIE_MAP:
            flow.prop(self, attr)


def apply_prefs():
    """Reapply all saved preference states to keymaps after registration."""
    prefs = get_prefs()
    if not prefs:
        return
    for attr, menu_name in PREF_PIE_MAP.items():
        _set_pie_active(menu_name, getattr(prefs, attr), attr)
    _set_tab_subsurf_active(prefs.tab_subsurf)


def register():
    bpy.utils.register_class(HP_AddonPreferences)


def unregister():
    bpy.utils.unregister_class(HP_AddonPreferences)


if __name__ == "__main__":
    register()
