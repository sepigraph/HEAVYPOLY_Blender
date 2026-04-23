bl_info = {
    "name": "HP Select Through",
    "description": "Box and lasso selection through mesh without occlusion",
    "author": "Vaughan Ling",
    "version": (0, 3, 0),
    "blender": (5, 1, 0),
    "category": "Mesh",
}

import bpy


def _get_prefs():
    addon = bpy.context.preferences.addons.get(__package__ or '')
    return addon.preferences if addon else None


def _xray_enable(context):
    shading = context.space_data.shading
    prev = shading.show_xray
    shading.show_xray = True
    return prev


def _xray_restore(context, prev_state):
    if context.space_data:
        context.space_data.shading.show_xray = prev_state


# ── Operators ─────────────────────────────────────────────────────────────────
# Pattern: enable x-ray → invoke the built-in modal (which sits on top of ours)
# → our modal fires on the first event AFTER the built-in finishes → restore.
# Keyboard events pass through so hotkeys still work during the drag.

class HP_OT_select_through_border(bpy.types.Operator):
    bl_idname = "view3d.select_through_border"
    bl_label = "Select Through (Box)"

    def invoke(self, context, event):
        prefs = _get_prefs()
        if prefs and not prefs.select_through_enabled:
            return {'PASS_THROUGH'}
        self._prev_xray = _xray_enable(context)
        context.window_manager.modal_handler_add(self)
        bpy.ops.view3d.select_box('INVOKE_DEFAULT', mode='SET', wait_for_input=False)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            _xray_restore(context, self._prev_xray)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}


class HP_OT_select_through_border_add(bpy.types.Operator):
    bl_idname = "view3d.select_through_border_add"
    bl_label = "Select Through Add (Box)"

    def invoke(self, context, event):
        prefs = _get_prefs()
        if prefs and not prefs.select_through_enabled:
            return {'PASS_THROUGH'}
        self._prev_xray = _xray_enable(context)
        context.window_manager.modal_handler_add(self)
        bpy.ops.view3d.select_box('INVOKE_DEFAULT', mode='ADD', wait_for_input=False)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            _xray_restore(context, self._prev_xray)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}


class HP_OT_select_through_border_sub(bpy.types.Operator):
    bl_idname = "view3d.select_through_border_sub"
    bl_label = "Select Through Subtract (Box)"

    def invoke(self, context, event):
        prefs = _get_prefs()
        if prefs and not prefs.select_through_enabled:
            return {'PASS_THROUGH'}
        self._prev_xray = _xray_enable(context)
        context.window_manager.modal_handler_add(self)
        bpy.ops.view3d.select_box('INVOKE_DEFAULT', mode='SUB', wait_for_input=False)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            _xray_restore(context, self._prev_xray)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}


class HP_OT_select_through_lasso(bpy.types.Operator):
    bl_idname = "view3d.select_through_lasso"
    bl_label = "Select Through (Lasso)"

    def invoke(self, context, event):
        prefs = _get_prefs()
        if prefs and not prefs.select_through_enabled:
            return {'PASS_THROUGH'}
        self._prev_xray = _xray_enable(context)
        context.window_manager.modal_handler_add(self)
        bpy.ops.view3d.select_lasso('INVOKE_DEFAULT', mode='SET')
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            _xray_restore(context, self._prev_xray)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}


class HP_OT_select_through_lasso_add(bpy.types.Operator):
    bl_idname = "view3d.select_through_lasso_add"
    bl_label = "Select Through Add (Lasso)"

    def invoke(self, context, event):
        prefs = _get_prefs()
        if prefs and not prefs.select_through_enabled:
            return {'PASS_THROUGH'}
        self._prev_xray = _xray_enable(context)
        context.window_manager.modal_handler_add(self)
        bpy.ops.view3d.select_lasso('INVOKE_DEFAULT', mode='ADD')
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            _xray_restore(context, self._prev_xray)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}


class HP_OT_select_through_lasso_sub(bpy.types.Operator):
    bl_idname = "view3d.select_through_lasso_sub"
    bl_label = "Select Through Subtract (Lasso)"

    def invoke(self, context, event):
        prefs = _get_prefs()
        if prefs and not prefs.select_through_enabled:
            return {'PASS_THROUGH'}
        self._prev_xray = _xray_enable(context)
        context.window_manager.modal_handler_add(self)
        bpy.ops.view3d.select_lasso('INVOKE_DEFAULT', mode='SUB')
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type in {'MOUSEMOVE', 'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'}:
            _xray_restore(context, self._prev_xray)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}


# ── WorkspaceTools ────────────────────────────────────────────────────────────
# Registered as proper toolbar tools so they only intercept LMB drag when the
# user has explicitly chosen them — the tweak tool is left completely untouched.

class HP_WT_SelectThroughBox(bpy.types.WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'EDIT_MESH'
    bl_idname = "heavypoly.select_through_box"
    bl_label = "Select Through Box"
    bl_description = (
        "Box select through mesh — temporarily enables X-Ray so geometry "
        "behind faces is included.\n\n"
        "Shift: add  |  Ctrl: subtract"
    )
    bl_icon = "ops.generic.select_box"
    bl_widget = None
    bl_keymap = (
        ("view3d.select_through_border",
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG'},
         {}),
        ("view3d.select_through_border_add",
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": True},
         {}),
        ("view3d.select_through_border_sub",
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "ctrl": True},
         {}),
    )


class HP_WT_SelectThroughLasso(bpy.types.WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'EDIT_MESH'
    bl_idname = "heavypoly.select_through_lasso"
    bl_label = "Select Through Lasso"
    bl_description = (
        "Lasso select through mesh — temporarily enables X-Ray so geometry "
        "behind faces is included.\n\n"
        "Shift: add  |  Ctrl: subtract"
    )
    bl_icon = "ops.generic.select_lasso"
    bl_widget = None
    bl_keymap = (
        ("view3d.select_through_lasso",
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG'},
         {}),
        ("view3d.select_through_lasso_add",
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "shift": True},
         {}),
        ("view3d.select_through_lasso_sub",
         {"type": 'LEFTMOUSE', "value": 'CLICK_DRAG', "ctrl": True},
         {}),
    )


# ── Registration ──────────────────────────────────────────────────────────────

classes = (
    HP_OT_select_through_border,
    HP_OT_select_through_border_add,
    HP_OT_select_through_border_sub,
    HP_OT_select_through_lasso,
    HP_OT_select_through_lasso_add,
    HP_OT_select_through_lasso_sub,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.utils.register_tool(HP_WT_SelectThroughBox, after={"builtin.select_box"}, separator=False)
    bpy.utils.register_tool(HP_WT_SelectThroughLasso, after={"heavypoly.select_through_box"}, separator=False)


def unregister():
    bpy.utils.unregister_tool(HP_WT_SelectThroughLasso)
    bpy.utils.unregister_tool(HP_WT_SelectThroughBox)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
