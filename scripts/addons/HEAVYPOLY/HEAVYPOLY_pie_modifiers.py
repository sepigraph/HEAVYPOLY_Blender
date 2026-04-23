import bpy
from bpy.types import Menu, Operator


class HP_OT_apply_all_modifiers(Operator):
    bl_idname = "object.hp_apply_all_modifiers"
    bl_label = "Apply All Modifiers"
    bl_description = "Apply all modifiers on selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        applied = 0
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            context.view_layer.objects.active = obj
            for mod in list(obj.modifiers):
                try:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                    applied += 1
                except Exception:
                    pass
        self.report({'INFO'}, f"Applied {applied} modifier(s)")
        return {'FINISHED'}


class HP_OT_remove_all_modifiers(Operator):
    bl_idname = "object.hp_remove_all_modifiers"
    bl_label = "Remove All Modifiers"
    bl_description = "Remove all modifiers from selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        for obj in context.selected_objects:
            count += len(obj.modifiers)
            obj.modifiers.clear()
        self.report({'INFO'}, f"Removed {count} modifier(s)")
        return {'FINISHED'}


class HP_MT_pie_modifiers(Menu):
    bl_label = "Modifiers"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # Left — Mirror
        pie.operator("object.modifier_add", text="Mirror", icon='MOD_MIRROR').type = 'MIRROR'

        # Right — Subdivision
        pie.operator("object.modifier_add", text="Subdivision", icon='MOD_SUBSURF').type = 'SUBSURF'

        # Bottom — Apply / Remove
        split = pie.split()
        col = split.column(align=True)
        col.scale_y = 1.4
        col.operator("object.hp_apply_all_modifiers", text="Apply All", icon='CHECKMARK')
        col.operator("object.hp_remove_all_modifiers", text="Remove All", icon='X')

        # Top — Bevel / Solidify
        split = pie.split()
        col = split.column(align=True)
        col.scale_y = 1.4
        col.operator("object.modifier_add", text="Bevel", icon='MOD_BEVEL').type = 'BEVEL'
        col.operator("object.modifier_add", text="Solidify", icon='MOD_SOLIDIFY').type = 'SOLIDIFY'

        # Top-Left — Array / Screw
        split = pie.split()
        col = split.column(align=True)
        col.scale_y = 1.4
        col.operator("object.modifier_add", text="Array", icon='MOD_ARRAY').type = 'ARRAY'
        col.operator("object.modifier_add", text="Screw", icon='MOD_SCREW').type = 'SCREW'

        # Top-Right — Shrinkwrap / Lattice
        split = pie.split()
        col = split.column(align=True)
        col.scale_y = 1.4
        col.operator("object.modifier_add", text="Shrinkwrap", icon='MOD_SHRINKWRAP').type = 'SHRINKWRAP'
        col.operator("object.modifier_add", text="Lattice", icon='MOD_LATTICE').type = 'LATTICE'

        # Bottom-Left — Weld / Decimate
        split = pie.split()
        col = split.column(align=True)
        col.scale_y = 1.4
        col.operator("object.modifier_add", text="Weld", icon='AUTOMERGE_OFF').type = 'WELD'
        col.operator("object.modifier_add", text="Decimate", icon='MOD_DECIM').type = 'DECIMATE'

        # Bottom-Right — Weighted Normal / Triangulate
        split = pie.split()
        col = split.column(align=True)
        col.scale_y = 1.4
        col.operator("object.modifier_add", text="Weighted Normal", icon='MOD_NORMALEDIT').type = 'WEIGHTED_NORMAL'
        col.operator("object.modifier_add", text="Triangulate", icon='MOD_TRIANGULATE').type = 'TRIANGULATE'


classes = (
    HP_OT_apply_all_modifiers,
    HP_OT_remove_all_modifiers,
    HP_MT_pie_modifiers,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
