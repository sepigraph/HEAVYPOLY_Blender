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

    x:   IntProperty(name="Width",      default=1920)
    y:   IntProperty(name="Height",     default=1080)
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
            img.color_mode  = 'RGBA'
            img.color_depth = '8'
        elif self.preset == 'EXR':
            img.file_format = 'OPEN_EXR'
            img.color_mode  = 'RGBA'
            img.color_depth = '32'
        elif self.preset == 'WEBP':
            img.file_format = 'WEBP'
            img.color_mode  = 'RGBA'
        return {'FINISHED'}


def _poll(context):
    addon = context.preferences.addons.get(__package__)
    return addon is not None and addon.preferences.hp_render_panel


# ─────────────────────────────────────────────────────────────────────────────
# Main panel
# ─────────────────────────────────────────────────────────────────────────────

class HP_PT_render(bpy.types.Panel):
    bl_label       = "HEAVYPOLY RENDER"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category    = 'HeavyPoly'

    @classmethod
    def poll(cls, context):
        return _poll(context)

    def draw(self, context):
        layout = self.layout
        scene  = context.scene
        rd     = scene.render
        img    = rd.image_settings

        split = layout.split(factor=0.5, align=False)
        left  = split.column()
        right = split.column()

        # ── Left: Camera + Resolution ─────────────────────────────────────
        box = left.box()
        box.label(text="Camera", icon='CAMERA_DATA')
        box.prop(scene, "camera", text='')

        box.separator(factor=0.3)
        box.label(text="Resolution", icon='RENDER_RESULT')
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(rd, "resolution_x",          text="X")
        row.prop(rd, "resolution_y",          text="Y")
        row.prop(rd, "resolution_percentage", text="%")
        grid = col.grid_flow(row_major=True, columns=2, align=True)
        for label, x, y in _RESOLUTION_PRESETS:
            op = grid.operator("render.hp_set_resolution", text=label)
            op.x = x
            op.y = y
            op.pct = 100

        # ── Right: Output ─────────────────────────────────────────────────
        box = right.box()
        box.label(text="Output", icon='OUTPUT')
        col = box.column(align=True)
        col.prop(img, "file_format", text='')
        row = col.row(align=True)
        row.scale_y = 1.1
        for label, preset in _OUTPUT_PRESETS:
            row.operator("render.hp_set_output_preset", text=label).preset = preset

        col.separator(factor=0.5)
        col.prop(img, "color_mode", text="Color")
        col.prop(img, "color_depth", text="Depth")

        col.separator(factor=0.5)
        row = col.row(align=True)
        row.prop(img, "compression", text="Comp")
        row.prop(rd,  "use_overwrite", text="Overwrite")

        # Filepath — full width below the split
        layout.separator(factor=0.5)
        layout.prop(rd, "filepath", text="")


# ─────────────────────────────────────────────────────────────────────────────
# Collapsible sub-panels
# ─────────────────────────────────────────────────────────────────────────────

class HP_PT_render_frame(bpy.types.Panel):
    bl_label       = "Frame Range"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category    = 'HeavyPoly'
    bl_parent_id   = 'HP_PT_render'
    bl_options     = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return _poll(context)

    def draw(self, context):
        layout = self.layout
        scene  = context.scene
        rd     = scene.render
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(scene, "frame_start", text="Start")
        row.prop(scene, "frame_end",   text="End")
        row = col.row(align=True)
        row.prop(rd,    "fps",         text="FPS")
        row.prop(scene, "frame_step",  text="Step")


class HP_PT_render_world(bpy.types.Panel):
    bl_label       = "World"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category    = 'HeavyPoly'
    bl_parent_id   = 'HP_PT_render'
    bl_options     = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return _poll(context)

    def draw(self, context):
        layout = self.layout
        world  = context.scene.world
        if not world.use_nodes:
            layout.prop(world, "color")
            return
        ntree = world.node_tree
        node  = ntree.get_output_node('EEVEE')
        if not node:
            layout.label(text="No output node")
            return
        input_surf = find_node_input(node, 'Surface')
        input_vol  = find_node_input(node, 'Volume')
        if not input_surf:
            layout.label(text="Incompatible output node")
            return
        layout.template_node_view(ntree, node, input_surf)
        layout.separator()
        layout.template_node_view(ntree, node, input_vol)


class HP_PT_render_color(bpy.types.Panel):
    bl_label       = "Color Management"
    bl_space_type  = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category    = 'HeavyPoly'
    bl_parent_id   = 'HP_PT_render'
    bl_options     = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return _poll(context)

    def draw(self, context):
        layout = self.layout
        vs     = context.scene.view_settings
        col = layout.column(align=True)
        col.prop(vs, 'view_transform', text='')
        col.prop(vs, 'look',           text='')
        layout.template_curve_mapping(vs, "curve_mapping", type='COLOR', levels=True)


# ─────────────────────────────────────────────────────────────────────────────

classes = (
    HP_OT_set_resolution,
    HP_OT_set_output_preset,
    HP_PT_render,
    HP_PT_render_frame,
    HP_PT_render_world,
    HP_PT_render_color,
)
register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
