import GameLogic
def main(cont): 
	# own.sheep_ids needs to start as an empty string
    
	own = cont.getOwner() 
	
	sens = cont.getSensor('type_hit') 
	
	if sens.isPositive():
		count = 0
		for ob in sens.getHitObjectList():
			if hasattr(ob, 'type') and ob.type == 'shp': 
				count += 1
		
		if count >= own.sheep_count:
			# Sheep ground sensor
			act = cont.getActuator('sheep_caught')
			# bigStick
			acti = cont.getActuator('sheep_caughti')
			# Catapult branch
			actii = cont.getActuator('sheep_caughtii')
			# piersheep
			actiii = cont.getActuator('sheep_caughtiii')
			# pier littleStick
			activ = cont.getActuator('sheep_caughtiv')
			# catapult_rock_door
			actv = cont.getActuator('sheep_caughtv')
			# catapult_throw
			actvi = cont.getActuator('sheep_caughtvi')
			# rock
			actvii = cont.getActuator('sheep_caughtvii')
			GameLogic.addActiveActuator(act, True)
			GameLogic.addActiveActuator(acti, True)
			GameLogic.addActiveActuator(actii, True)
			GameLogic.addActiveActuator(actiii, True)
			GameLogic.addActiveActuator(activ, True)
			GameLogic.addActiveActuator(actv, True)
			GameLogic.addActiveActuator(actvi, True)
			GameLogic.addActiveActuator(actvii, True)
