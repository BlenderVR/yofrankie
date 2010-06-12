# Unparent all children and run any actuator attached

from bge import logic

def main(cont):
	own = cont.owner
	
	for ob in own.children:
		if 'carried' in ob:
			pos = ob.worldPosition
			
			ob['carried'] = 0
			ob.removeParent()
			
	play_cart_act= cont.actuators[0]
	cont.activate(play_cart_act)
