import bpy
import sys

def rename_action(action):
    """"""
    objects = bpy.data.objects
    for ob in objects:
        if ob.animation_data and ob.animation_data.action:
            if ob.animation_data.action == action:
                name = "CDA:ObIpo:{0}".format(ob.name)
                if action.name != name:
                    old_name = action.name
                    action.name = name
                    print("renamed {0} to {1}".format(old_name, name), file=sys.stderr)
                return

    print("Poorly named action {0}, in file {1}, left unnamed".format(action.name, bpy.path.basename(bpy.data.filepath)), file=sys.stderr)


def update_actions():
    """"""
    for action in bpy.data.actions:

        if action.library:
            continue

        if action.users == 0:
            action.use_fake_user = True

        elif action.users == 1:
            if action.name.startswith('CDA:ObIpo'):
                rename_action(action)


def create_children_action_actuators(ob, actuator):
    """"""

    # list all the objects that will receive a new actuator
    children = ob.children

    if not children:
        return


    # list all the controllers that are linked to
    # this actuator
    controllers = []
    for ob in bpy.data.objects:
        for controller in ob.game.controllers:
            for _actuator in controller.actuators:
                if actuator == _actuator:
                    controllers.append(controller)
                    break

    if not controllers:
        return

    # create the new actuators
    actuators = []
    for child in children:
        if child.animation_data and child.animation_data.action:
            name = "{0} : Child : {1}".format(actuator.name, child.name)

            bpy.ops.logic.actuator_add(type='ACTION', name=name, object=child.name)
            _actuator = child.game.actuators[name]
            _actuator.action = child.animation_data.action

            # copy settings
            #_actuator.blend_mode = actuator.blend_mode
            _actuator.frame_blend_in = actuator.frame_blend_in
            _actuator.frame_end = actuator.frame_end
            _actuator.frame_property = actuator.frame_property #XXX
            _actuator.frame_start = actuator.frame_start
            _actuator.layer = actuator.layer
            _actuator.pin = actuator.pin
            _actuator.play_mode = actuator.play_mode # XXX
            _actuator.priority = actuator.priority
            _actuator.use_additive = actuator.use_additive
            _actuator.use_continue_last_frame = actuator.use_continue_last_frame
            _actuator.use_force = actuator.use_force
            _actuator.use_local = actuator.use_local

            actuators.append(_actuator)

            print("Recreated actuator from {0} into {1}".format(ob.name, child.name))

    # link the new actuators
    for controller in controllers:
        for _actuator in actuators:
            controller.link(actuator=_actuator)


def update_objects():
    for ob in bpy.data.objects:

        if ob.library:
            continue

        for actuator in ob.game.actuators:
            if actuator.type == 'ACTION':
                if actuator.apply_to_children:
                    create_children_action_actuators(ob, actuator)


def main():
    bpy.ops.logic.texface_convert()
    bpy.ops.anim.update_data_paths()

    update_actions()
    update_objects()

    bpy.ops.wm.save_mainfile(filepath=bpy.data.filepath)


main()
print(bpy.data.filepath, file=sys.stderr)
