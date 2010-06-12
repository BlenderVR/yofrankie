import GameLogic
def main(cont):
    own = cont.getOwner() 
     
    sens = cont.getSensor('type_hit') 
     
    if sens.isPositive():
        for ob in sens.getHitObjectList(): 
            if ob.type == 'ram': 
                 
                actu = cont.getActuator('ramDetect') 
                GameLogic.addActiveActuator(actu, True) 
