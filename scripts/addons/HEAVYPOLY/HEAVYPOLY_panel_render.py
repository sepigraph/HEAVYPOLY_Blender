import bpy
import random
from bpy.props import *
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
        row = layout.row()
        col = row.column()
        col2 = row.column()
        layout.use_property_split = True
#FIRST COLUMN##############################################################

        scene = context.scene
        rd = scene.render
        props = scene.eevee
        image_settings = rd.image_settings
        col.label(text='RENDER CAMERA')
        col.prop(scene, "camera", text = '')
        row = col.row()
        row.scale_x=.5
        row.prop(rd, "resolution_x", text="X")
        row.prop(rd, "resolution_y", text="Y")
        row.prop(rd, "resolution_percentage", text="%")

        # Resolution presets — 4 columns, 2 rows (video 16:9 then square)
        grid = col.grid_flow(row_major=True, columns=4, align=True)
        for label, x, y in _RESOLUTION_PRESETS:
            op = grid.operator("render.hp_set_resolution", text=label)
            op.x = x
            op.y = y
            op.pct = 100

        row = col.row()
        row.prop(scene, "frame_start", text="F Start")
        row.prop(rd, "fps", text = 'F Rate')
        row = col.row()
        row.prop(scene, "frame_end", text="F End")
        row.prop(scene, "frame_step", text="F Step")
        col.separator()
        row = col.row()

#           col.prop(world, "use_nodes", icon='NODETREE')

        col.label(text='WORLD')
        world = bpy.context.scene.world

        # worldnodes = world.node_tree.nodes
        # actnode = worldnodes.active
        # col.prop(actnode, 'type', text='')
        # for node in worldnodes:
            # for input in node.inputs:
                # col.prop(input, 'default_value', text = input.name)
        # # for x in actnode.inputs:
            # # if x.name != 'Normal' and x.name != 'Clearcoat Normal' and x.name != 'Tangent':
                # # col2.prop(x,'default_value', text = x.name

        if world.use_nodes:
            ntree = world.node_tree
            node = ntree.get_output_node('EEVEE')

            if node:
                input = find_node_input(node, 'Surface')
                inputvol = find_node_input(node, 'Volume')
                if input:
                    col.template_node_view(ntree, node, input)
                if input:
                    col.separator()
                    col.separator()
                    # col.prop(scene.eevee, "use_volumetric", text="Use Volumetric")
                    col.template_node_view(ntree, node, inputvol)
                else:
                    col.label(text="Incompatible output node")
            else:
                col.label(text="No output node")
        else:
            col.prop(world, "color")
        scene = bpy.context.scene
        props = scene.eevee
        # col.label(text='BLOOM')
        # box = col.box().column()
        # box.active = props.use_bloom
        # box.prop(props, "bloom_threshold")
        # box.prop(props, "bloom_knee")
        # box.prop(props, "bloom_radius")
        # box.prop(props, "bloom_color")
        # box.prop(props, "bloom_intensity")
        # box.prop(props, "bloom_clamp")
#SECOND COLUMN##############################################################





        col2.label(text='RENDER SETTINGS')
        col2.prop(scene.view_settings, 'view_transform', text='')
        col2.prop(scene.view_settings, 'look', text='')
        col2.template_curve_mapping(scene.view_settings, "curve_mapping", type='COLOR', levels=True)
        col2.prop(image_settings, "file_format", text = '')

        # Output presets
        row = col2.row(align=True)
        for label, preset in _OUTPUT_PRESETS:
            row.operator("render.hp_set_output_preset", text=label).preset = preset

        row = col2.row()
        row.prop(image_settings, "compression")
        row.prop(rd, "use_overwrite")
        row = col2.row()
        row.scale_x=.2
        row.prop(image_settings, "color_mode", expand=True)
        row = col2.row()
        row.scale_x=.2
        row.prop(image_settings, "color_depth", expand=True)
        col2.prop(rd, "filepath", text="")
        if hasattr(props, "taa_samples"):
            row = col2.row()
            row.prop(props, "taa_samples")
            row.prop(props, "taa_render_samples")

classes = (
    HP_OT_set_resolution,
    HP_OT_set_output_preset,
    HP_PT_render,
)
register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
