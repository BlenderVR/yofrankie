# Parent any touching object that has the 'carried'
# property and run any actuator attached

import GameLogic
def main(cont):
	own = cont.getOwner()
	
	carry_sens= cont.getSensor('carry_touch')
	carry_done= False
	if carry_sens.isPositive():
		for ob in carry_sens.getHitObjectList():
			if hasattr(ob, 'carried') and ob.carried==0:
				ob.carried= 1
				
				ob.setParent(own)
				carry_done= True
		
		if carry_done:
			play_carry_act= cont.getActuators()[0]
			GameLogic.addActiveActuator(play_carry_act, True)
