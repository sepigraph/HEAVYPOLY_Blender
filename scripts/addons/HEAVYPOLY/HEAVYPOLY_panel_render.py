import bpy
from bpy.props import IntProperty, StringProperty
from bpy_extras.node_utils import find_node_input

_RESOLUTION_PRESETS = [
    ("720p",    1280,  720),
    ("1080p",   1920, 1080),
    ("1440p",   2560, 1440),
    ("4K UHD",  3840, 2160),
    ("1K",      1024, 1024),
    ("2K",      2048, 2048),
    ("4K",      4096, 4096),
    ("8K",      8192, 8192),
]

_OUTPUT_PRESETS = [
    ("PNG RGBA", 'PNG_RGBA'),
    ("EXR 32",   'EXR'),
    ("WEBP",     'WEBP'),
]


class HP_OT_set_resolution(bpy.types.Operator):
    bl_idname = "render.hp_set_resolution"
    bl_label = "Set Resolution"
    bl_options = {'REGISTER', 'UNDO'}

    x: IntProperty(name="Width",  default=1920)
    y: IntProperty(name="Height", default=1080)
    pct: IntProperty(name="Percentage", default=100)

    def execute(self, context):
        rd = context.scene.render
        rd.resolution_x = self.x
        rd.resolution_y = self.y
        rd.resolution_percentage = self.pct
        return {'FINISHED'}


class HP_OT_set_output_preset(bpy.types.Operator):
    bl_idname = "render.hp_set_output_preset"
    bl_label = "Set Output Preset"
    bl_options = {'REGISTER', 'UNDO'}

    preset: StringProperty(name="Preset")

    def execute(self, context):
        rd = context.scene.render
        img = rd.image_settings
        if self.preset == 'PNG_RGBA':
            img.file_format = 'PNG'
            img.color_mode = 'RGBA'
            img.color_depth = '8'
        elif self.preset == 'EXR':
            img.file_format = 'OPEN_EXR'
            img.color_mode = 'RGBA'
            img.color_depth = '32'
        elif self.preset == 'WEBP':
            img.file_format = 'WEBP'
            img.color_mode = 'RGBA'
        return {'FINISHED'}


class HP_PT_render(bpy.types.Panel):
    bl_label = "HEAVYPOLY RENDER"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'HeavyPoly'

    @classmethod
    def poll(cls, context):
        addon = context.preferences.addons.get(__package__)
        if addon is None:
            return False
        return addon.preferences.hp_render_panel

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rd = scene.render
        props = scene.eevee
        image_settings = rd.image_settings

        # ── Camera ───────────────────────────────────────────────────────────
        layout.label(text="Camera", icon='CAMERA_DATA')
        layout.prop(scene, "camera", text='')

        layout.separator()

        # ── Resolution ───────────────────────────────────────────────────────
        layout.label(text="Resolution", icon='RENDER_RESULT')
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(rd, "resolution_x", text="X")
        row.prop(rd, "resolution_y", text="Y")
        row.prop(rd, "resolution_percentage", text="%")
        grid = col.grid_flow(row_major=True, columns=4, align=True)
        for label, x, y in _RESOLUTION_PRESETS:
            op = grid.operator("render.hp_set_resolution", text=label)
            op.x = x
            op.y = y
            op.pct = 100

        layout.separator()

        # ── Frame Range ───────────────────────────────────────────────────────
        layout.label(text="Frame Range", icon='TIME')
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(scene, "frame_start", text="Start")
        row.prop(scene, "frame_end", text="End")
        row = col.row(align=True)
        row.prop(rd, "fps", text="FPS")
        row.prop(scene, "frame_step", text="Step")

        layout.separator()

        # ── World ─────────────────────────────────────────────────────────────
        layout.label(text="World", icon='WORLD')
        world = scene.world
        if world.use_nodes:
            ntree = world.node_tree
            node = ntree.get_output_node('EEVEE')
            if node:
                input_surf = find_node_input(node, 'Surface')
                input_vol  = find_node_input(node, 'Volume')
                if input_surf:
                    layout.template_node_view(ntree, node, input_surf)
                    layout.separator()
                    layout.template_node_view(ntree, node, input_vol)
                else:
                    layout.label(text="Incompatible output node")
            else:
                layout.label(text="No output node")
        else:
            layout.prop(world, "color")

        layout.separator()

        # ── Color Management ─────────────────────────────────────────────────
        layout.label(text="Color Management", icon='COLOR')
        col = layout.column(align=True)
        col.prop(scene.view_settings, 'view_transform', text='')
        col.prop(scene.view_settings, 'look', text='')
        layout.template_curve_mapping(
            scene.view_settings, "curve_mapping", type='COLOR', levels=True)

        layout.separator()

        # ── Output ────────────────────────────────────────────────────────────
        layout.label(text="Output", icon='OUTPUT')
        col = layout.column(align=True)
        col.prop(image_settings, "file_format", text='')
        row = col.row(align=True)
        for label, preset in _OUTPUT_PRESETS:
            row.operator("render.hp_set_output_preset", text=label).preset = preset

        col.separator(factor=0.5)
        col.prop(image_settings, "color_mode", text="Color")
        col.prop(image_settings, "color_depth", text="Depth")

        col.separator(factor=0.5)
        row = col.row(align=True)
        row.prop(image_settings, "compression", text="Compression")
        row.prop(rd, "use_overwrite", text="Overwrite")
        col.prop(rd, "filepath", text="")

        if hasattr(props, "taa_samples"):
            layout.separator()
            layout.label(text="Sampling", icon='ANTIALIASED')
            col = layout.column(align=True)
            row = col.row(align=True)
            row.prop(props, "taa_samples", text="Viewport")
            row.prop(props, "taa_render_samples", text="Render")


classes = (
    HP_OT_set_resolution,
    HP_OT_set_output_preset,
    HP_PT_render,
)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
