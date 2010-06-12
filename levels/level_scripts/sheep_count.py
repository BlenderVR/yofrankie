# -*- coding: utf-8 -*-
def main(cont): 
	# own.sheep_ids needs to start as an empty string
    
	own = cont.owner
	
	sens = cont.sensors['type_hit']
	
	if sens.positive:
		count = 0
		for ob in sens.hitObjectList:
			if 'type' in ob and ob['type'] == 'shp': 
				count += 1
		
		if count >= own['sheep_count']:
			# Sheep ground sensor
			act = cont.actuators['sheep_caught']
			# bigStick
			acti = cont.actuators['sheep_caughti']
			# Catapult branch
			actii = cont.actuators['sheep_caughtii']
			# piersheep
			actiii = cont.actuators['sheep_caughtiii']
			# pier littleStick
			activ = cont.actuators['sheep_caughtiv']
			# catapult_rock_door
			actv = cont.actuators['sheep_caughtv']
			# catapult_throw
			actvi = cont.actuators['sheep_caughtvi']
			# rock
			actvii = cont.actuators['sheep_caughtvii']
			cont.activate(act)
			cont.activate(acti)
			cont.activate(actii)
			cont.activate(actiii)
			cont.activate(activ)
			cont.activate(actv)
			cont.activate(actvi)
			cont.activate(actvii)
