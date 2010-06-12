# Unparent all children and run any actuator attached

import GameLogic
def main(cont):
	own = cont.getOwner()
	
	for ob in own.getChildren():
		if hasattr(ob, 'carried'):
			pos = ob.getPosition()
			
			ob.carried= 0
			ob.removeParent()
			
	play_cart_act= cont.getActuators()[0]
	GameLogic.addActiveActuator(play_cart_act, True)
