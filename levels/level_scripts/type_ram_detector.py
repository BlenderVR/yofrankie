# -*- coding: utf-8 -*-
def main(cont):
    own = cont.owner
     
    sens = cont.sensors['type_hit']
     
    if sens.positive:
        for ob in sens.hitObjectList:
            if ob['type'] == 'ram':
                 
                actu = cont.actuators['ramDetect']
                cont.activate(actu)
