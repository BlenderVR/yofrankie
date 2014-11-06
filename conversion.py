import bpy
import sys

def rename_action(action):
    print("Poorly named action {0}, in file {1}".format(action.name, bpy.path.basename(bpy.data.filepath)), file=sys.stderr)

    objects = bpy.data.objects
    for ob in objects:
        if ob.animation_data and ob.animation_data.action:
            if ob.animation_data.action == action:
                action.name = "CDA:ObIpo:{0}".format(ob.name)
                print("renamed {0}".format(action.name), file=sys.stderr)
                return


def main():
    bpy.ops.logic.texface_convert()
    bpy.ops.anim.update_data_paths()

    for action in bpy.data.actions:
        if action.users == 0:
            action.use_fake_user = True

        elif action.users == 1:
            if action.name.startswith('CDA:ObIpo'):
                rename_action(action)

    bpy.ops.wm.save_mainfile(filepath=bpy.data.filepath)


main()
print(bpy.data.filepath, file=sys.stderr)
