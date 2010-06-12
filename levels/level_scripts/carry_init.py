# -*- coding: utf-8 -*-
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# Parent any touching object that has the 'carried'
# property and run any actuator attached
def main(cont):
	own = cont.owner
	
	carry_sens= cont.sensors['carry_touch']
	carry_done= False
	if carry_sens.positive:
		for ob in carry_sens.hitObjectList:
			print("shit")
			if 'carried' in ob  and ob['carried']==0:
				ob['carried']= 1
				
				ob.setParent(own)
				carry_done= True
		
		if carry_done:
			play_carry_act= cont.actuators[0]
			cont.activate(play_carry_act)
